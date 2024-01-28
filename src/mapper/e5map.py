# scitonic/src/mapper/e5map.py

import openai

class E5Mapper:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def get_completion(self, user_input, temperature=1, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
        messages = [
            {
            "role": "system",
            "content": "You are a subject matter technical expert. You select ONLY ONE from the list provided. ALWAYS respond in complete JSON. Always respond with the best possible task selected with YES or NO. ONLY\nselect ONE TASK:\n        \"task\": {\n          \"ArguAna\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a claim, find documents that refute the claim\"\n          },\n          \"ClimateFEVER\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a claim about climate change, retrieve documents that support or refute the claim\"\n          },\n          \"DBPedia\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a query, retrieve relevant entity descriptions from DBPedia\"\n          },\n          \"FEVER\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a claim, retrieve documents that support or refute the claim\"\n          },\n          \"FiQA2018\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a financial question, retrieve user replies that best answer the question\"\n          },\n          \"HotpotQA\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a multi-hop question, retrieve documents that can help answer the question\"\n          },\n          \"MSMARCO\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a web search query, retrieve relevant passages that answer the query\"\n          },\n          \"NFCorpus\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a question, retrieve relevant documents that best answer the question\"\n          },\n          \"NQ\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a question, retrieve Wikipedia passages that answer the question\"\n          },\n          \"QuoraRetrieval\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a question, retrieve questions that are semantically equivalent to the given question\"\n          },\n          \"SCIDOCS\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a scientific paper title, retrieve paper abstracts that are cited by the given paper\"\n          },\n          \"SciFact\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a scientific claim, retrieve documents that support or refute the claim\"\n          },\n          \"Touche2020\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a question, retrieve detailed and persuasive arguments that answer the question\"\n          },\n          \"TRECCOVID\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a query on COVID-19, retrieve documents that answer the query\"\n          },\n        },\n        \"required\": [\"ArguAna\", \"ClimateFEVER\" , \"DBPedia\", \"FEVER\" , \"FiQA2018\" , \"HotpotQA\" , \"MSMARCO\" , \"NFCorpus\", \"NQ\", \"QuoraRetrieval\", \"SCIDOCS\", \"SciFact\", \"Touche2020\" , \"TRECCOVID\"]\n      }\n    }"
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
        return response

# Example Response
# {
#   "id": "chatcmpl-8lweouguDvUk1FPY0gfqg8JSY7PHH",
#   "object": "chat.completion",
#   "created": 1706437586,
#   "model": "gpt-4-0125-preview",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": "```json\n{\n  \"task\": {\n    \"ArguAna\": false,\n    \"ClimateFEVER\": false,\n    \"DBPedia\": false,\n    \"FEVER\": false,\n    \"FiQA2018\": false,\n    \"HotpotQA\": false,\n    \"MSMARCO\": false,\n    \"NFCorpus\": false,\n    \"NQ\": false,\n    \"QuoraRetrieval\": false,\n    \"SCIDOCS\": false,\n    \"SciFact\": false,\n    \"Touche2020\": false,\n    \"TRECCOVID\": true\n  }\n}\n```"
#       },
#       "logprobs": null,
#       "finish_reason": "stop"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 891,
#     "completion_tokens": 130,
#     "total_tokens": 1021
#   },
#   "system_fingerprint": "fp_376b7f78b9"
# }

