# scitonic/src/mapper/parser.py
import json
import re

class MapperParser:
    @staticmethod
    def parse_taskmapper_response(response):
        """Parses the response from e5map and returns the identified task."""
        print(response)
        print(response.choices[0].message.content)
        print(type(response.choices[0].message.content))
        pattern = re.compile(r'"(\w+)": "YES"')

        matches = pattern.findall(response.choices[0].message.content)
        print("testbala")

        for task in matches:
            print(task)
            return task
               

        
        
        #task_data = json.loads(response.choices[0].message.content)
        if not response or 'choices' not in response or not response['choices']:
            return "No task identified3"
        
        assistant_message = next((choice['message']['content'] for choice in response['choices'] if choice['message']['role'] == 'assistant'), None)
        
        if not assistant_message:
            return "No task identified1"

        try:
            task_data = json.loads(assistant_message)
            print("json conversion working")
            for task, is_selected in task_data.get('task', {}).items():
                if is_selected == "YES":
                    return task
            return "No task identified2"
        except json.JSONDecodeError:
            return "Invalid response format"

    @staticmethod
    def parse_teammapper_response(response):
        """Parses the response from scimap and returns the identified team."""
        if not response or 'choices' not in response or not response['choices']:
            return "No team identified"
        
        assistant_message = next((choice['message']['content'] for choice in response['choices'] if choice['message']['role'] == 'assistant'), None)
        
        if not assistant_message:
            return "No team identified"

        try:
            team_data = json.loads(assistant_message)
            for team, is_selected in team_data.get('Team', {}).items():
                if is_selected:
                    return team
            return "No team identified"
    @staticmethod
    def serialize_chat_completion(chat_completion):
        """
        Serializes a ChatCompletion object into a JSON-serializable format.
        """
        if not hasattr(chat_completion, '__dict__'):
            raise TypeError("Input is not a serializable object")

        # Convert the ChatCompletion object to a dictionary
        serializable_dict = {
            "id": getattr(chat_completion, "id", None),
            "object": getattr(chat_completion, "object", None),
            "created": getattr(chat_completion, "created", None),
            "model": getattr(chat_completion, "model", None),
            "choices": [{
                "index": choice.index,
                "message": {
                    "role": choice.message.role,
                    "content": choice.message.content
                },
                "logprobs": choice.logprobs,
                "finish_reason": choice.finish_reason
            } for choice in getattr(chat_completion, "choices", [])],
            "usage": getattr(chat_completion, "usage", None),
            "system_fingerprint": getattr(chat_completion, "system_fingerprint", None)
        }
    
        return json.dumps(serializable_dict, ensure_ascii=False)

def parse_special_response(response):
    """
    Parses the response with a specific format using regex and returns the identified team or task.
    """
    # Extracting the assistant's message
    assistant_message = next((choice['message']['content'] for choice in response['choices'] if choice['message']['role'] == 'assistant'), None)
    
    if not assistant_message:
        return "No team or task identified"

    # Using regex to extract content within triple backticks
    extracted_content = re.search(r"```json\n([\s\S]*?)\n```", assistant_message)
    if not extracted_content:
        return "No valid format identified"

    json_content = extracted_content.group(1)

    try:
        # Parsing the extracted content as JSON
        parsed_content = json.loads(json_content)

        # Process the parsed JSON to find the team or task
        if 'Team' in parsed_content:
            for team, is_selected in parsed_content['Team'].items():
                if is_selected:
                    return team
        elif 'task' in parsed_content:
            for task, is_selected in parsed_content['task'].items():
                if is_selected == "YES":
                    return task

        return "No team or task identified"
    except json.JSONDecodeError:
        return "Invalid JSON format"