# scitonic/src/mapper/scimap.py

import openai
import json

class scimap:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def get_completion(self, user_input, temperature=1, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
        messages = [
            {
                "role": "system",
                "content": "You are a subject matter technical expert. You select ONLY ONE from the list provided. ALWAYS respond in complete JSON. Always respond with the best possible team selected with YES or NO. ONLY\nselect ONE TEAM:\n        \"Team\": {\n          \"ClimateTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if it the task might relate to climate and environmental science\"\n          },\n          \"Covid19Team\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the user requires engaging with covid19topics\"\n          },\n          \"FinanceTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team the user requires analysis and advice about financials and financial literature\"\n          },\n          \"CodingTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the taskk requires producing code or technology\"\n          },\n          \"DebateTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the user requires debating a topic thoroughly\"\n          },\n          \"HomeworkTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the user requires help with homework or coursework\"\n          },\n          \"ConsultingTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the user requires business consulting\"\n          }\n        },\n        \"required\": [\"ClimateTeam\", \"Covid19Team\" , \"FinanceTeam\", \"CodingTeam\" , \"DebateTeam\" , \"HomeworkTeam\" , \"ConsultingTeam\"]\n      }\n    }\n  }\n]"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return json.dumps(response, ensure_ascii=False)

# ### Example Response :
#{
#   "id": "chatcmpl-8llkSPEQjqcTNq50tDuLJtW5MXbTU",
#   "object": "chat.completion",
#   "created": 1706395652,
#   "model": "gpt-4-0125-preview",
#   "choices": [
#       {
#           "index": 0,
#           "message": {
#               "role": "assistant",
#               "content": "```json\n{\n  \"Team\": {\n    \"ClimateTeam\": false,\n    \"Covid19Team\": false,\n    \"FinanceTeam\": false,\n    \"CodingTeam\": true,\n    \"DebateTeam\": false,\n    \"HomeworkTeam\": false,\n    \"ConsultingTeam\": false\n  }\n}\n```"
#            },
#           "logprobs": null,
#           "finish_reason": "stop"
#       }
#   ],
#   "usage": {
#       "prompt_tokens": 360,
#       "completion_tokens": 67,
#       "total_tokens": 427
#   },
#   "system_fingerprint": "fp_376b7f78b9"
#}

# import json
# import openai

# class scimap:
#     def __init__(self, api_key):
#         self.client = openai.OpenAI(api_key=api_key)

#     def get_completion(self, user_input, temperature=1, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
#         messages = [
#             {
#                 "role": "system",
#                 "content": "You are a subject matter technical expert. You select ONLY ONE from the list provided. ALWAYS respond in complete JSON. Always respond with the best possible team selected with YES or NO. ONLY\nselect ONE TEAM:\n        \"Team\": {\n          \"ClimateTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if it the task might relate to climate and environmental science\"\n          },\n          \"Covid19Team\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the user requires engaging with covid19topics\"\n          },\n          \"FinanceTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team the user requires analysis and advice about financials and financial literature\"\n          },\n          \"CodingTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the taskk requires producing code or technology\"\n          },\n          \"DebateTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the user requires debating a topic thoroughly\"\n          },\n          \"HomeworkTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the user requires help with homework or coursework\"\n          },\n          \"ConsultingTeam\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this team if the user requires business consulting\"\n          }\n        },\n        \"required\": [\"ClimateTeam\", \"Covid19Team\" , \"FinanceTeam\", \"CodingTeam\" , \"DebateTeam\" , \"HomeworkTeam\" , \"ConsultingTeam\"]\n      }\n    }\n  }\n]"
#             },
#             {
#                 "role": "user",
#                 "content": user_input
#             },
#             {
#                 "role": "assistant",
#                 "content": "This tool is a function called \"Choose the most appropriate Team.\" It is used to select a specific Team based on a given set of tasks. The function requires parameters such as \"ClimateTeam\", \"Covid19Team\", \"FinanceTeam\", \"CodingTeam\", \"DebateTeam\", \"HomeworkTeam\", \"ConsultingTeam\", each with a boolean type and description. The required response is either \"YES\" or \"NO\" for each task. The function is designed for subject matter technical experts to select the best possible task from the provided list."
#             }
#         ]

#         response = self.client.chat.completions.create(
#             model="gpt-4-1106-preview",
#             messages=messages,
#             temperature=temperature,
#             max_tokens=max_tokens,
#             top_p=top_p,
#             frequency_penalty=frequency_penalty,
#             presence_penalty=presence_penalty
#         )
#         return response

# ### Example Response :
#{
#   "id": "chatcmpl-8llkSPEQjqcTNq50tDuLJtW5MXbTU",
#   "object": "chat.completion",
#   "created": 1706395652,
#   "model": "gpt-4-0125-preview",
#   "choices": [
#       {
#           "index": 0,
#           "message": {
#               "role": "assistant",
#               "content": "```json\n{\n  \"Team\": {\n    \"ClimateTeam\": false,\n    \"Covid19Team\": false,\n    \"FinanceTeam\": false,\n    \"CodingTeam\": true,\n    \"DebateTeam\": false,\n    \"HomeworkTeam\": false,\n    \"ConsultingTeam\": false\n  }\n}\n```"
#            },
#           "logprobs": null,
#           "finish_reason": "stop"
#       }
#   ],
#   "usage": {
#       "prompt_tokens": 360,
#       "completion_tokens": 67,
#       "total_tokens": 427
#   },
#   "system_fingerprint": "fp_376b7f78b9"
#}