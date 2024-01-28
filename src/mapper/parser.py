# scitonic/src/mapper/parser.py
import json

class MapperParser:
    @staticmethod
    def parse_taskmapper_response(response):
        """Parses the response from e5map and returns the identified task."""
        response = json.loads(response)
        if not response or 'choices' not in response or not response['choices']:
            return "No task identified"
        
        assistant_message = next((choice['message']['content'] for choice in response['choices'] if choice['message']['role'] == 'assistant'), None)
        
        if not assistant_message:
            return "No task identified"

        try:
            parsed_message = json.loads(assistant_message)
        except json.JSONDecodeError:
            parsed_message = assistant_message
        
        task_data = parsed_message
        if isinstance(task_data, dict):
            for task, is_selected in task_data.get('task', {}).items():
                if is_selected == "YES":
                    return task
        return "No task identified"

    @staticmethod
    def parse_teammapper_response(response):
        """Parses the response from scimap and returns the identified team."""
        response = json.loads(response)
        if not response or 'choices' not in response or not response['choices']:
            return "No team identified"
        
        assistant_message = next((choice['message']['content'] for choice in response['choices'] if choice['message']['role'] == 'assistant'), None)
        
        if not assistant_message:
            return "No team identified"

        try:
            parsed_message = json.loads(assistant_message)
        except json.JSONDecodeError:
            parsed_message = assistant_message
        
        team_data = parsed_message
        if isinstance(team_data, dict):
            for team, is_selected in team_data.get('Team', {}).items():
                if is_selected:
                    return team
        return "No team identified"
