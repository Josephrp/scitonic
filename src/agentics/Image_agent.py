import json
import os
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import matplotlib.pyplot as plt
import requests
from PIL import Image
from termcolor import colored

import autogen
from autogen import Agent, AssistantAgent, ConversableAgent, UserProxyAgent
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

config_list_4v = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-vision-preview"],
    },
)


config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

gpt4_llm_config = {"config_list": config_list_gpt4, "cache_seed": 42}

agent1 = MultimodalConversableAgent(
    name="image-explainer-1",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": config_list_4v, "temperature": 0.5, "max_tokens": 300},
    system_message="Your image description is poetic and engaging.",
)
agent2 = MultimodalConversableAgent(
    name="image-explainer-2",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": config_list_4v, "temperature": 0.5, "max_tokens": 300},
    system_message="Your image description is factual and to the point.",
)

def imagechat():
    def _reset_agents():
        agent1.reset()
        agent2.reset()
        user_proxy.reset()
    _reset_agents()

    # User Proxy Agent
    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="Ask both image explainer 1 and 2 for their description.",
        human_input_mode="TERMINATE",  # Try between ALWAYS, NEVER, and TERMINATE
        max_consecutive_auto_reply=10,
        code_execution_config={
            "use_docker": False
        },
    )

    # # Group Chat setup
    # groupchat = autogen.GroupChat(agents=[agent1, agent2, user_proxy], messages=[], max_round=5)
    # group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_llm_config)

    # # Initiate the chat with a message
    # user_proxy.initiate_chat(
    #     group_chat_manager,
    #     message="""Describe the image:
    #                 <img path/url of image>."""
    # )
