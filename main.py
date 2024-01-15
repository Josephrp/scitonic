import autogen

llm_config = autogen.config_list_from_json(
    env_or_file="src/config/OAI_CONFIG_LIST.json",
    filter_dict={"model": {"gpt-4", "gpt-3.5-turbo-16k", "gpt-4-1106-preview"}}
)

class UserProxy:
    def interact(self):
        question = input("MultiTonic builds multi-agent systems thatautomate your business operations ! Describe your problem in detail, then optionally bullet point a brief step by step way to solve it, then (or optionally) give a clear command or instruction to solve the issues above:")
        max_auto_reply = int(input("Set a maximum number of autoreplies by entering a number with minimum 10: "))
        return question, max_auto_reply

if __name__ == "__main__":
    print("Response:", response)