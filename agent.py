import os
import requests
from chromadb import chromadb
from dotenv import load_dotenv
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import autogen
import chromadb.utils.embedding_functions as embedding_functions



load_dotenv()



# ------------------ Create functions ------------------ #


# Function for Chromadb
chroma = chromadb.connect("dbname")

# Embeddings model
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="YOUR_API_KEY",
    model_name="intfloat/e5-mistral-7b-instruct"
)


embeddings = huggingface_ef()

# Function to store embeddings  
def store_embeddings(documents):
    embeds = embeddings(documents) 
    chroma.insert({"documents": documents, "embeddings": embeds})

def search_documents(query):
    docs = [] # retrieve documents
    store_embeddings(docs)
    return docs
# ------------------ Create agent ------------------ #

# Create user proxy agent
user_proxy = UserProxyAgent(name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=1
    )

# Create researcher agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "to create"
    }
)


researcher.register_function(search_documents)

# Create research manager agent
research_manager = GPTAssistantAgent(
    name="research_manager",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "to create"
    }
)


# Create director agent
director = GPTAssistantAgent(
    name = "director",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "to create",
    }
)


director.register_function(store_embeddings)


# Create group chat
groupchat = autogen.GroupChat(agents=[user_proxy, researcher, research_manager, director], messages=[], max_round=15)
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


# ------------------ start conversation ------------------ #
message = """
Research the 
"""
user_proxy.initiate_chat(group_chat_manager, message=message)