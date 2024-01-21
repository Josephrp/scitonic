import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
config_list = [
    {
        "model": "gpt-4",
        "api_key": "<your OpenAI API key>",
    },  # OpenAI API endpoint for gpt-4
]


llm_config = {
    "timeout": 60,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0,
}
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
        "task": "code",
        "docs_path": "",
        "chunk_token_size": 1000,
        "model": llm_config["config_list"][0]["model"],
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "collection_name": "groupchat",
        "get_or_create": True,
    },
    code_execution_config=False,
)
# Placeholder definitions for agents used in team functions
coder = AssistantAgent(
    name="Coder",
    system_message="You are a coder. Help in writing and reviewing code.",
    llm_config=llm_config
)

pm = AssistantAgent(
    name="Project_Manager",
    system_message="You are a project manager. Coordinate tasks and ensure project success.",
    llm_config=llm_config
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="You are a code reviewer. Provide feedback on code quality.",
    llm_config=llm_config
)

# Define more agents for each team
finance_expert = AssistantAgent(
    name="Finance_Expert",
    system_message="You are a finance expert. Provide insights on financial matters.",
    llm_config=llm_config
)

debate_champion = AssistantAgent(
    name="Debate_Champion",
    system_message="You are a debate champion. Contribute to meaningful debates.",
    llm_config=llm_config
)

academic_whiz = AssistantAgent(
    name="Academic_Whiz",
    system_message="You are an academic whiz. Offer solutions to academic challenges.",
    llm_config=llm_config
)

consulting_pro = AssistantAgent(
    name="Consulting_Pro",
    system_message="You are a consulting professional. Offer professional advice and solutions.",
    llm_config=llm_config
)
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


# Function to reset agents
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
        agents=[boss_aid, finance_analyst, pm, reviewer, finance_expert],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, finance_problem=FINANCE_PROBLEM, n_results=3)

def debateteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, debate_expert, pm, reviewer, debate_champion],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, debate_problem=DEBATE_PROBLEM, n_results=3)

def homeworkteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, academic_expert, pm, reviewer, academic_whiz],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, homework_problem=HOMEWORK_PROBLEM, n_results=3)

def consultingteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[boss_aid, consultant, pm, reviewer, consulting_pro],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    boss_aid.initiate_chat(manager, consulting_problem=CONSULTING_PROBLEM, n_results=3)
