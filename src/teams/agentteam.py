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
