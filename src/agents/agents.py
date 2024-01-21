import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

# Define your termination message function
def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

# Define your llm_config
config_list = [
    {
        "model": "gpt-4",
        "api_key": "<your OpenAI API key>",
    },
]
llm_config = {
    "timeout": 60,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

# Create the UserProxyAgent (Boss)
boss = autogen.UserProxyAgent(
    name="Boss",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="The boss who asks questions and gives tasks.",
    code_execution_config=False,
    default_auto_reply="Reply `TERMINATE` if the task is done.",
)

# Create the RetrieveUserProxyAgent (Boss Assistant)
boss_aid = RetrieveUserProxyAgent(
    name="Boss_Assistant",
    is_termination_msg=termination_msg,
    system_message="Assistant who has extra content retrieval power for solving difficult problems.",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "QuoraRetrieval",
        "docs_path": "",
        "chunk_token_size": 1000,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "collection_name": "groupchat",
        "get_or_create": True,
    },
    code_execution_config=False,
)

# Create other AssistantAgents for different teams
covid19_scientist = AssistantAgent(
    name="Covid19_Scientist",
    system_message="You are a scientist studying Covid-19 trends. Provide analysis and insights.",
    llm_config=llm_config
)

healthcare_expert = AssistantAgent(
    name="Healthcare_Expert",
    system_message="You are a healthcare expert focused on managing and mitigating the impact of Covid-19.",
    llm_config=llm_config
)

finance_analyst = AssistantAgent(
    name="Finance_Analyst",
    system_message="You are a finance analyst. Provide insights on the economic impact of Covid-19.",
    llm_config=llm_config
)

debate_expert = AssistantAgent(
    name="Debate_Expert",
    system_message="You are an expert in debate strategies and communication. Participate in meaningful debates.",
    llm_config=llm_config
)

academic_expert = AssistantAgent(
    name="Academic_Expert",
    system_message="You are an academic expert. Provide assistance and insights for academic challenges.",
    llm_config=llm_config
)

consultant = AssistantAgent(
    name="Consultant",
    system_message="You are a consultant. Offer professional advice and solutions.",
    llm_config=llm_config
)

# Define the problems for each team
PROBLEM = "How to use spark for parallel training in FLAML? Give me sample code."
COVID19_PROBLEM = "Analyze the current state of Covid-19 and provide recommendations for mitigation."
FINANCE_PROBLEM = "Assess the economic impact of Covid-19 and propose financial strategies."
DEBATE_PROBLEM = "Participate in a debate on the challenges and opportunities in technology."
HOMEWORK_PROBLEM = "Assist in solving complex academic problems related to computer science."
CONSULTING_PROBLEM = "Provide professional consulting services for a business challenge."

# Define a function to reset agents
def _reset_agents():
    boss_aid.reset()

# Define functions for each team
def codingteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, coder, pm, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, problem=PROBLEM, n_results=3)

def covid19team():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, covid19_scientist, healthcare_expert, finance_analyst],
        messages=[],
        max_round=12
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, covid19_problem=COVID19_PROBLEM, n_results=3)

def financeteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, finance_analyst, pm, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, finance_problem=FINANCE_PROBLEM, n_results=3)

def debateteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, debate_expert, pm, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, debate_problem=DEBATE_PROBLEM, n_results=3)

def homeworkteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, academic_expert, pm, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, homework_problem=HOMEWORK_PROBLEM, n_results=3)

def consultingteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, consultant, pm, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, consulting_problem=CONSULTING_PROBLEM, n_results=3)
