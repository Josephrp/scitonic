# scitonic/src/agentics/agents.py

import autogen
import sqlite3
from autogen.oai.client import OpenAIWrapper
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.conversable_agent import ConversableAgent
import chromadb

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    file_location="./src/config/",
    filter_dict={
        "model": ["gpt-3.5-turbo-preview", "gpt-4-preview", "gpt-4-vision-preview", "dall-e-3"],
    },
)

print("LLM models: ", [config_list[i]["model"] for i in range(len(config_list))])

llm_config = {
         "timeout": 60,
         "cache_seed": 42,
         "config_list": config_list,
         "temperature": 0,
     }

def termination_msg(self, x):
        return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

class AgentsFactory:
    def __init__(self, llm_config, db_path):
        self.llm_config = llm_config
        self.db_path = db_path

    

    def tonic(self) :
        return autogen.UserProxyAgent(
            name="Boss",
            is_termination_msg=termination_msg,
            human_input_mode="NEVER",
            system_message="The boss who asks questions and gives tasks.",
            code_execution_config=False,
            default_auto_reply="Reply `TERMINATE` if the task is done.",
        )

    # Create the RetrieveUserProxyAgent (Boss Assistant)
    def scitonic(self) :
        return RetrieveUserProxyAgent(
            name="Boss_Assistant",
            is_termination_msg=termination_msg,
            system_message="Assistant who has extra content retrieval power for solving difficult problems.",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
            retrieve_config={
                "task": "QuoraRetrieval",
                "docs_path": self.db_path,
                "chunk_token_size": 1000,
                "model": llm_config["config_list"][0]["model"],
                "client": chromadb.PersistentClient(path="/tmp/chromadb"),
                "collection_name": "groupchat",
                "get_or_create": True,
            },
            code_execution_config=False,
        )
    # Placeholder definitions for agents used in team functions
    def coder(self) : 
        return AssistantAgent(
            name="Coder",
            system_message="You are a coder. Help in writing and reviewing code.",
            llm_config=llm_config
        )

    def pm(self) :
        return AssistantAgent(
            name="Project_Manager",
            system_message="You are a project manager. Coordinate tasks and ensure project success.",
            llm_config=llm_config
        )

    def reviewer(self) :
        return AssistantAgent(
            name="Reviewer",
            system_message="You are a code reviewer. Provide feedback on code quality.",
            llm_config=llm_config
        )

    # Define more agents for each team
    def finance_expert(self) :
        return AssistantAgent(
            name="Finance_Expert",
            system_message="You are a finance expert. Provide insights on financial matters.",
            llm_config=llm_config
        )

    def debate_champion(self) :
        return AssistantAgent(
            name="Debate_Champion",
            system_message="You are a debate champion. Contribute to meaningful debates.",
            llm_config=llm_config
        )

    def academic_whiz(self) :
        return AssistantAgent(
        name="Academic_Whiz",
        system_message="You are an academic whiz. Offer solutions to academic challenges.",
        llm_config=llm_config
    )

    def consulting_pro(self) :
            return AssistantAgent(
            name="Consulting_Pro",
            system_message="You are a consulting professional. Offer professional advice and solutions.",
            llm_config=llm_config
        )
    def covid19_scientist(self) : 
        return AssistantAgent(
            name="Covid19_Scientist",
            system_message="You are a scientist studying Covid-19 trends. Provide analysis and insights.",
            llm_config=llm_config
        )

    def healthcare_expert(self) : 
        return AssistantAgent(
            name="Healthcare_Expert",
            system_message="You are a healthcare expert focused on managing and mitigating the impact of Covid-19.",
            llm_config=llm_config
        )

    def finance_analyst(self) :
        return AssistantAgent(
            name="Finance_Analyst",
            system_message="You are a finance analyst. Provide insights on the economic impact of Covid-19.",
            llm_config=llm_config
        )

    def debate_expert(self) :
        return AssistantAgent(
            name="Debate_Expert",
            system_message="You are an expert in debate strategies and communication. Participate in meaningful debates.",
            llm_config=llm_config
        )

    def academic_expert(self) :
        return AssistantAgent(
            name="Academic_Expert",
            system_message="You are an academic expert. Provide assistance and insights for academic challenges.",
            llm_config=llm_config
        )
