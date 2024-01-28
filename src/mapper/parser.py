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
        
        pattern = re.compile(r'"task": \{[^}]*"([^"]+)": true[^}]*\}')

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
        print(response)
        print(response.choices[0].message.content)
        print(type(response.choices[0].message.content))
        pattern = re.compile(r'"(\w+)": "YES"')

        matches = pattern.findall(response.choices[0].message.content)
        print("testbala")

        for tas in matches:
            print(tas)
            return tas
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
        except json.JSONDecodeError:
            return "Invalid response format"