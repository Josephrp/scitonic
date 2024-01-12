import os
import uuid
import gc
import gradio as gr
import pickle
import torch
import chromadb
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import requests
import mimetypes
import pandas as pd
import langchain
from dotenv import load_dotenv
from datasets import Dataset
from datasets import load_dataset
from langchain.chains import ConversationalRetrievalChain
import chroma_datasets
from chroma_datasets.utils import import_into_chroma
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_community.vectorstores.chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
from threading import Lock

load_dotenv()
unstructured_api_key = os.getenv('UNSTRUCTURED_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

print("Loading tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-mistral-7b-instruct')
model = AutoModel.from_pretrained('intfloat/e5-mistral-7b-instruct')
print("Tokenizer and model loaded.")
collection_name = "tonic_ai_demo"
print("Initializing Chroma vector store...")
vectorstore = Chroma(collection_name=collection_name)
print("Chroma vector store initialized.")

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. You can assume the question about the war in Ukraine. Chat History: {chat_history} Follow Up Input: {question} Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are an AI assistant for answering questions about the war in Ukraine. You are given the following extracted parts of a long document and a question. Provide a conversational answer. If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer. If the question is not about the war in Ukraine, politely inform them that you are tuned to only answer questions about the war in Ukraine. Question: {question} ========= {context} ========= Answer in Markdown:"""
QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])

class ChromaRetriever:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.client = chromadb.Client()

    def retrieve(self, query, top_k=5):
        query_embedding = generate_embeddings([query])[0]
        collection = self.client.get_collection(self.collection_name)
        similar_docs = collection.query(query_embedding, n_results=top_k)
        return similar_docs

def get_chain(collection_name):
    llm = OpenAI(temperature=0, api_key=openai_api_key)
    retriever = ChromaRetriever(collection_name)
    condense_question_prompt = PromptTemplate.from_template(_template)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=retriever, 
        condense_question_prompt=condense_question_prompt
    )
    return qa_chain

def get_detailed_instruct(task_description: str, query: str) -> str:
    return f'Instruct: {task_description}\nQuery: {query}'

def last_token_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

def retrieve_documents(query, collection_name, top_k=5):
    """
    Retrieve top_k documents similar to the query from the specified collection.
    
    :param query: The query string.
    :param collection_name: The name of the collection in Chroma vector store.
    :param top_k: Number of top similar documents to retrieve.
    :return: A list of top_k similar documents.
    """
    # Generate embedding for the query
    query_embedding = generate_embeddings([query])[0]

    # Retrieve similar documents
    chroma_client = chromadb.Client()
    collection = chroma_client.get_collection(collection_name)
    similar_docs = collection.query(query_embedding, n_results=top_k)

    return similar_docs

def generate_and_store_embeddings(texts, collection_name):
    print("Generating and storing embeddings...")
    chroma_client = chromadb.Client()

    # Check if collection exists, if not create one
    try:
        collection = chroma_client.create_collection(collection_name)
        print(f"New collection '{collection_name}' created.")
    except chromadb.db.base.UniqueConstraintError:
        collection = chroma_client.get_collection(collection_name)
        print(f"Using existing collection '{collection_name}'.")

    # Convert texts to a Hugging Face dataset
    df = pd.DataFrame({'text': texts})
    hf_dataset = Dataset.from_pandas(df)

    # Process and add each text to the collection
    for index, row in enumerate(hf_dataset):
        formatted_text = get_detailed_instruct('Given a web search query, retrieve relevant passages that answer the query', row['text'])
        inputs = tokenizer(formatted_text, return_tensors="pt", padding=True, truncation=True, max_length=4096)
        outputs = model(**inputs)
        pooled_output = last_token_pool(outputs.last_hidden_state, inputs['attention_mask'])
        normalized_embeddings = F.normalize(pooled_output, p=2, dim=1).squeeze().tolist()

        # Add to collection
        collection.add(
            ids=[str(index)],
            documents=[row['text']],
            embeddings=[normalized_embeddings],
            metadatas=[{"type": "text"}]
        )

        # Free up memory
        del inputs, outputs, pooled_output, normalized_embeddings
        gc.collect()

    print("Embeddings processed and stored.")
    return "All embeddings processed and stored."


def process_document(file_path):
    print("File path received:", file_path)

    if not file_path.endswith('.docx'):
        return "Error: The uploaded file is not a valid .docx file."

    # Load the document using Chroma's document processing capabilities
    try:
        texts = chroma_datasets.utils.docx_to_text(file_path)
    except Exception as e:
        return f"Error processing file: {e}"

    # Use Chroma's text chunker for splitting text
    texts = chroma_datasets.utils.chunk_text(texts, chunk_size=3200, overlap=120)
    return generate_and_store_embeddings(texts, collection_name)
class ChatWrapper:
    def __init__(self):
        self.lock = Lock()

    def __call__(self, query: str):
        self.lock.acquire()
        try:
            collection_name = "document_embeddings"
            chain = get_chain(collection_name)
            output = chain({"question": query, "chat_history": []})["answer"]
        except Exception as e:
            output = str(e)
        finally:
            self.lock.release()
        return output

chat = ChatWrapper()

block = gr.Blocks()

with block:
    gr.Markdown("# Simple Query Interface")
    
    with gr.Row():
        file_upload = gr.File(label="Upload .docx Document")
        process_button = gr.Button(value="Process Document")
        file_output = gr.Textbox(label="File Processing Output")

    with gr.Row():
        query_input = gr.Textbox(label="Your Query", placeholder="Enter your query here")
        submit_button = gr.Button(value="Submit Query")
        query_output = gr.Textbox(label="Answer")

    process_button.click(process_document, inputs=[file_upload], outputs=file_output)
    submit_button.click(chat, inputs=[query_input], outputs=query_output)

block.launch(debug=True)