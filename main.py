import autogen
from src.mapper.e5map import E5Mapper
from src.mapper.scimap import scimap
from src.mapper.parser import MapperParser
from src.datatonic.dataloader import DataLoader
from src.teams.agentteam import codingteam, covid19team, financeteam, debateteam, homeworkteam, consultingteam

api_key = "OAI_KEY"

# Load config
llm_config = autogen.config_list_from_json(
    env_or_file="./config/OAI_CONFIG_LIST.json",
    filter_dict={"model": {"gpt-4", "gpt-3.5-turbo-16k", "gpt-4-1106-preview"}}
)

# Initialize DataLoader
data_loader = DataLoader()

# UserProxy for interaction
class UserProxy:
    def interact(self):
        question = input("Describe your problem in detail: ")
        max_auto_reply = int(input("Set a maximum number of autoreplies (minimum 50): "))
        return question, max_auto_reply

# Main function
def main():
    user_proxy = UserProxy()
    question, max_auto_reply = user_proxy.interact()

    # Initialize mappers
    taskmapper = E5Mapper(api_key)
    teammapper = scimap(api_key)

    # Get responses from mappers
    taskmap_response = taskmapper.get_completion(question)
    teammap_response = teammapper.get_completion(question)

    # Parse responses
    task = MapperParser.parse_taskmapper_response(taskmap_response)
    team = MapperParser.parse_teammapper_response(teammap_response)

    # Load dataset based on task
    dataset = data_loader.load_and_process(task.lower())

    # Select and initiate team based on team mapping
    if team == "CodingTeam":
        codingteam()
    elif team == "Covid19Team":
        covid19team()
    elif team == "FinanceTeam":
        financeteam()
    elif team == "DebateTeam":
        debateteam()
    elif team == "HomeworkTeam":
        homeworkteam()
    elif team == "ConsultingTeam":
        consultingteam()
    else:
        print("No appropriate team found for the given input.")

    # Further processing can be done here with the dataset and the selected team

if __name__ == "__main__":
    main()


# # 1. create an RetrieveAssistantAgent instance named "assistant"
# assistant = RetrieveAssistantAgent(
#     name="assistant",
#     system_message="You are a helpful assistant.",
#     llm_config={
#         "timeout": 600,
#         "cache_seed": 42,
#         "config_list": config_list,
#     },
# )
# def VectorStore():
#     chroma_db = Chroma()
#     collection_name = "my_collection"
#     chroma_db.new_collection(collection_name)
#     chroma_db.switch_collection(collection_name)
#     data = {
#         "embeddings": [...],  # Replace with actual embeddings
#         "contents": [...],    # Replace with actual document contents
#         "metadatas": [...],   # Replace with actual metadata
#         "ids": [...]          # Replace with actual IDs
#     }
#     chroma_db.add_data_to(data)

#     # Add more operations as needed...

# # from transformers import AutoTokenizer, AutoModel
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


# # for e5 config we should consider building a complete retriever perhaps  
# e5embed_config_list = [
#     {
#         "model": "e5",
#         "api_key": "None",
#         "base_url": "https://tonic1-e5.hf.space/--replicas/{e5demo}/compute_embeddings", # includes 'space secret' which has to be changed every time the demo goes to sleep
#     }
# ]

# e5retrieve_config_list = [
#     {
#         "model": "e5",
#         "api_key": "None",
#         "base_url": "https://tonic1-e5.hf.space/--replicas/{e5demo}/", # includes 'space secret' which has to be changed every time the demo goes to sleep
#     }
# ]
