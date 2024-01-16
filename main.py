import autogen

llm_config = autogen.config_list_from_json(
    env_or_file="src/config/OAI_CONFIG_LIST.json",
    filter_dict={"model": {"gpt-4", "gpt-3.5-turbo-16k", "gpt-4-1106-preview"}}
)

# for e5 config we should consider building a complete retriever perhaps  
e5mistralretriever_config_list = [
    {
        "model": "e5",
        "api_key": "None",
        "base_url": "https://tonic1-e5.hf.space/--replicas/{e5demo}/", # includes 'space secret' which has to be changed every time the demo goes to sleep
    }
]

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
# Here we generated the documentations from FLAML's docstrings. Not needed if you just want to try this notebook but not to reproduce the
# outputs. Clone the FLAML (https://github.com/microsoft/FLAML) repo and navigate to its website folder. Pip install and run `pydoc-markdown`
# and it will generate folder `reference` under `website/docs`.
#
# `task` indicates the kind of task we're working on. In this example, it's a `code` task.
# `chunk_token_size` is the chunk token size for the retrieve chat. By default, it is set to `max_tokens * 0.6`, here we set it to 2000.
# We use an in-memory QdrantClient instance here. Not recommended for production.
# Get the installation instructions here: https://qdrant.tech/documentation/guides/installation/
ragproxyagent = QdrantRetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "code",
        "docs_path": "add_your_files_here",  # change this to your own path, such as https://raw.githubusercontent.com/microsoft/autogen/main/README.md
        "chunk_token_size": 2000,
        "model": config_list[0]["model"],
        "client": QdrantClient(":memory:"),
        "embedding_model": "BAAI/bge-small-en-v1.5",
    },
)

# assistant.reset()
# ragproxyagent.initiate_chat(assistant, problem="What is autogen?")
class UserProxy:
    def interact(self):
        question = input("MultiTonic builds multi-agent systems thatautomate your business operations ! Describe your problem in detail, then optionally bullet point a brief step by step way to solve it, then (or optionally) give a clear command or instruction to solve the issues above:")
        max_auto_reply = int(input("Set a maximum number of autoreplies by entering a number with minimum 10: "))
        return question, max_auto_reply

if __name__ == "__main__":
    print("Response:", response)