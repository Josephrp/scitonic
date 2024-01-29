# scitonic/src/teams/agentteams.py

import autogen
import sqlite3
import autogen
from src.agentics.agents import AgentsFactory
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    file_location="./src/config/",
    filter_dict={
        "model": ["gpt-3.5-turbo-preview", "gpt-4-preview", "gpt-4-vision-preview", "dall-e-3"],
    },
)
llm_config = {
         "timeout": 60,
         "cache_seed": 42,
         "config_list": config_list,
         "temperature": 0,
     }


ag = AgentsFactory(llm_config)

#def _reset_agents():
#    ag.scitonic.reset()


def codingteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[scitonic, coder, pm, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    scitonic.initiate_chat(manager, problem=PROBLEM, n_results=3)

def covid19team():
    #_reset_agents()
    team = autogen.GroupChat(
        agents=[ag.scitonic, ag.covid19_scientist, ag.healthcare_expert, ag.finance_analyst],
        messages=[],
        max_round=12
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    scitonic.initiate_chat(manager, covid19_problem=COVID19_PROBLEM, n_results=3)

def financeteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[scitonic, finance_analyst, pm, reviewer, finance_expert],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    scitonic.initiate_chat(manager, finance_problem=FINANCE_PROBLEM, n_results=3)

def debateteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[scitonic, debate_expert, pm, reviewer, debate_champion],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    scitonic.initiate_chat(manager, debate_problem=DEBATE_PROBLEM, n_results=3)

def homeworkteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[scitonic, academic_expert, pm, reviewer, academic_whiz],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    scitonic.initiate_chat(manager, homework_problem=HOMEWORK_PROBLEM, n_results=3)

def consultingteam():
    _reset_agents()
    team = autogen.GroupChat(
        agents=[scitonic, consultant, pm, reviewer, consulting_pro],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"
    )

    manager = autogen.GroupChatManager(groupchat=team, llm_config=llm_config)
    scitonic.initiate_chat(manager, consulting_problem=CONSULTING_PROBLEM, n_results=3)