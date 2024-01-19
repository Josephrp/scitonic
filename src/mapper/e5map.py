import openai

class E5Mapper:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def get_completion(self, user_input, temperature=1, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
        messages = [
            {
                "role": "system",
                "content": "You are a subject matter technical expert. You select ONLY ONE from the list provided. ALWAYS respond in complete JSON. Always respond with the best possible task selected with YES or NO. ONLY\nselect ONE TASK:\n        \"task\": {\n          \"ArguAna\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a claim, find documents that refute the claim\"\n          },\n          \"ClimateFEVER\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a claim about climate change, retrieve documents that support or refute the claim\"\n          },\n          \"DBPedia\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a query, retrieve relevant entity descriptions from DBPedia\"\n          },\n          \"FEVER\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a claim, retrieve documents that support or refute the claim\"\n          },\n          \"FiQA2018\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a financial question, retrieve user replies that best answer the question\"\n          },\n          \"HotpotQA\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a multi-hop question, retrieve documents that can help answer the question\"\n          },\n          \"MSMARCO\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a web search query, retrieve relevant passages that answer the query\"\n          },\n          \"NFCorpus\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a question, retrieve relevant documents that best answer the question\"\n          },\n          \"NQ\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a question, retrieve Wikipedia passages that answer the question\"\n          },\n          \"QuoraRetrieval\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a question, retrieve questions that are semantically equivalent to the given question\"\n          },\n          \"SCIDOCS\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a scientific paper title, retrieve paper abstracts that are cited by the given paper\"\n          },\n          \"SciFact\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a scientific claim, retrieve documents that support or refute the claim\"\n          },\n          \"Touche2020\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a question, retrieve detailed and persuasive arguments that answer the question\"\n          },\n          \"TRECCOVID\": {\n            \"type\": \"boolean\",\n            \"description\": \"select this task if it requires that given a query on COVID-19, retrieve documents that answer the query\"\n          },\n        },\n        \"required\": [\"ArguAna\", \"ClimateFEVER\" , \"DBPedia\", \"FEVER\" , \"FiQA2018\" , \"HotpotQA\" , \"MSMARCO\" , \"NFCorpus\", \"NQ\", \"QuoraRetrieval\", \"SCIDOCS\", \"SciFact\", \"Touche2020\" , \"TRECCOVID\"]\n      }\n    }\n  }\n]"
            },
            {
                "role": "user",
                "content": user_input
            },
            {
                "role": "assistant",
                "content": "This tool is a function called \"Choose the most appropriate specialty.\" It is used to select a specific task based on a given set of options. The function requires parameters such as \"ArguAna\", \"ClimateFEVER\", \"DBPedia\", \"FEVER\", \"FiQA2018\", \"HotpotQA\", \"MSMARCO\", \"NFCorpus\", \"NQ\", \"QuoraRetrieval\", \"SCIDOCS\", \"SciFact\", \"Touche2020\", and \"TRECCOVID\", each with a boolean type and description. The required response is either \"YES\" or \"NO\" for each task. The function is designed for subject matter technical experts to select the best possible task from the provided list."
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

# ### Example Response :
    
# ```json
# {
#   "task": {
#     "DBPedia": "YES"
#   }
# }
# ```
