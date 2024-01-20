class MapperParser:
    @staticmethod
    def parse_taskmapper_response(response):
        """Parses the response from the taskmapper and returns the task name."""
        if not response or 'task' not in response:
            return "No task identified"
        task_info = response['task']
        for task, is_selected in task_info.items():
            if is_selected == "YES":
                return task
        return "No task identified"

    @staticmethod
    def parse_teammapper_response(response):
        """Parses the response from the teammapper and returns the team name."""
        if not response or 'Team' not in response:
            return "No team identified"
        team_info = response['Team']
        for team, is_selected in team_info.items():
            if is_selected:
                return team
        return "No team identified"