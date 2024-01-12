import semantic_kernel
import autogen

llm_config = autogen.config_list_from_json(
    env_or_file="src/config/OAI_CONFIG_LIST.json",
    filter_dict={"model": {"gpt-4", "gpt-3.5-turbo-16k", "gpt-4-1106-preview"}}
)

builder_config_path = autogen.config_list_from_json(
    env_or_file="src/config/OAI_CONFIG_LIST.json",
    filter_dict={"model": {"gpt-4-1106-preview"}}
)

kernel = semantic_kernel.Kernel()
kernel.import_skill(BingPlugin(bing_api_key))
kernel.import_skill(WebPagesPlugin())
sk_planner = AutoGenPlanner(kernel, llm_config, builder_config_path)

assistant = sk_planner.create_assistant_agent("Assistant")
def get_response(question, max_auto_reply):
    worker = sk_planner.create_user_agent("Worker", max_auto_reply=max_auto_reply, human_input="NEVER")
    assistant = sk_planner.create_assistant_agent("Assistant")
    worker.initiate_chat(assistant, message=question)
    return worker.get_response()

if __name__ == "__main__":
    question = input("Tonic's EasyAGI builds multi-agent systems that use Semantic-Kernel Plugins to automate your business operations ! Describe your problem in detail, then optionally bullet point a brief step by step way to solve it, then (or optionally) give a clear command or instruction to solve the issues above:")
    max_auto_reply = int(input("Set a maximum number of autoreplies by entering a number with minimum 10: "))
    response = get_response(question, max_auto_reply) 
    print("Response:", response)