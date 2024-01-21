import autogen
from .src.mapper.e5map import E5Mapper
from .src.mapper.scimap import scimap
from src.mapper.parser import MapperParser
from src.memory.imvectorstore import Chroma
from src.teams.agentteam import codingteam, covid19team, financeteam, debateteam, homeworkteam, consultingteam

# Example usage
# codingteam()
# covid19team()
# agents_factory = AgentsFactory()

# e5demo = "7o447"

def VectorStore():
    # Create an instance of Chroma
    chroma_db = Chroma()

    # Create a new collection
    collection_name = "my_collection"
    chroma_db.new_collection(collection_name)

    # Switch to the new collection
    chroma_db.switch_collection(collection_name)

    # Example data to add
    data = {
        "embeddings": [...],  # Replace with actual embeddings
        "contents": [...],    # Replace with actual document contents
        "metadatas": [...],   # Replace with actual metadata
        "ids": [...]          # Replace with actual IDs
    }

    # Add data to the collection
    chroma_db.add_data_to(data)

    # Add more operations as needed...


llm_config = autogen.config_list_from_json(
    env_or_file="./config/OAI_CONFIG_LIST.json",
    filter_dict={"model": {"gpt-4", "gpt-3.5-turbo-16k", "gpt-4-1106-preview"}}
)

# for e5 config we should consider building a complete retriever perhaps  
e5embed_config_list = [
    {
        "model": "e5",
        "api_key": "None",
        "base_url": "https://tonic1-e5.hf.space/--replicas/{e5demo}/compute_embeddings", # includes 'space secret' which has to be changed every time the demo goes to sleep
    }
]

e5retrieve_config_list = [
    {
        "model": "e5",
        "api_key": "None",
        "base_url": "https://tonic1-e5.hf.space/--replicas/{e5demo}/", # includes 'space secret' which has to be changed every time the demo goes to sleep
    }
]

### Tonic User Intention Mapping and e5 embedding selection
   
    taskmapper = E5Mapper(api_key)
    taskmap = taskmapper.get_completion(user_input)
    teammapper = scimap(api_key)
    teammap = teammapper.get_completion(user_input)
    task = MapperParser.parse_taskmapper_response(taskmapper_response)
    team = MapperParser.parse_teammapper_response(teammapper_response)

# 1. create an RetrieveAssistantAgent instance named "assistant"
assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,
    },
)

# 2. create the QdrantRetrieveUserProxyAgent instance named "ragproxyagent"
# By default, the human_input_mode is "ALWAYS", which means the agent will ask for human input at every step. We set it to "NEVER" here.
# `docs_path` is the path to the docs directory. It can also be the path to a single file, or the url to a single file. By default,
# it is set to None, which works only if the collection is already created.
#
# `task` indicates the kind of task we're working on. In this example, it's a `code` task.
# `chunk_token_size` is the chunk token size for the retrieve chat. By default, it is set to `max_tokens * 0.6`, here we set it to 2000.
# We use an in-memory QdrantClient instance here. Not recommended for production.
# Get the installation instructions here: https://qdrant.tech/documentation/guides/installation/
#ragproxyagent = QdrantRetrieveUserProxyAgent(
#    name="ragproxyagent",
#    human_input_mode="NEVER",
#    max_consecutive_auto_reply=10,
#    retrieve_config={
#        "task": "code",
#        "docs_path": "add_your_files_here",
#       "chunk_token_size": 2000,
#       "model": config_list[0]["model"],
#       "client": QdrantClient(":memory:"),             CONNECTOR REQUIRED !!
#       "embedding_model": "BAAI/bge-small-en-v1.5",
#    },
#)

# assistant.reset()
# ragproxyagent.initiate_chat(assistant, problem="What is autogen?")

# from datasets import load_dataset
# from transformers import AutoTokenizer, AutoModel
# import torch
# from src.memory.imvectorstore import Chroma

# def encode_texts(model_name, texts):
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModel.from_pretrained(model_name)

#     # Encoding texts
#     encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
#     with torch.no_grad():
#         model_output = model(**encoded_input)

#     # Mean pooling - Take attention mask into account for correct averaging
#     input_mask_expanded = encoded_input['attention_mask'].unsqueeze(-1).expand(model_output.last_hidden_state.size()).float()
#     sum_embeddings = torch.sum(model_output.last_hidden_state * input_mask_expanded, 1)
#     sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
#     return sum_embeddings / sum_mask

# def load_and_store_dataset(dataset_name, model_name, collection_name):
#     # Load dataset
#     dataset = load_dataset(dataset_name, split='train')

#     # Select a subset for demonstration purposes
#     subset = dataset.select(range(100))

#     # Extract texts and IDs
#     texts = subset['text']  # Adjust field name based on dataset structure
#     ids = subset['id']  # Adjust field name based on dataset structure

#     # Encode texts
#     embeddings = encode_texts(model_name, texts)

#     # Create an instance of Chroma and a new collection
#     chroma_db = Chroma()
#     chroma_db.new_collection(collection_name)
#     chroma_db.switch_collection(collection_name)

#     # Prepare data for storage
#     data = {
#         "embeddings": embeddings.tolist(),
#         "contents": texts,
#         "metadatas": [{} for _ in texts],  # Empty metadata for demonstration
#         "ids": ids
#     }

#     # Add data to the collection
#     chroma_db.add_data_to(data)

# # Example usage
# if __name__ == "__main__":
#     dataset_name = "ag_news"  # Example dataset
#     model_name = "distilbert-base-uncased"  # Example model
#     collection_name = "my_ag_news_collection"
#     load_and_store_dataset(dataset_name, model_name, collection_name)

class UserProxy:
    def interact(self):
        question = input("Sci-Tonic builds multi-agent systems that automate your technical research operations ! Describe your problem in detail, then optionally bullet point a brief step by step way to solve it, then (or optionally) give a clear command or instruction to solve the issues above:")
        max_auto_reply = int(input("Set a maximum number of autoreplies by entering a number with minimum 50: "))
        return question, max_auto_reply

if __name__ == "__main__":
    print("Response:", response)