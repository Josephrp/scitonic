from typing import Optional, Dict, List
import semantic_kernel, autogen
import datetime
import autogen
from .agent_builder import AgentBuilder

class AutoGenPlanner:
    """
    Semantic Kernel planner using Conversational Programming via AutoGen.
    Leverages OpenAI Function Calling and AutoGen agents to solve tasks using
    loaded Semantic Kernel plugins. Supports functions with a single string parameter.
    Tested with GPT 3.5 Turbo and GPT 4, primarily uses GPT 3.5 Turbo for performance.
    """

    ASSISTANT_PERSONA = (
        f"Only use provided functions. Do not ask the user for other actions. "
        f"Use functions to find unavailable information. "
        f"Today's date: {datetime.date.today().strftime('%B %d, %Y')}. "
        f"Reply TERMINATE when the task is done."
    )

    def __init__(self, kernel: semantic_kernel.Kernel, llm_config: Dict = None, builder_config_path: str = None, zilliz_config: Dict = None):
        self.kernel = kernel
        self.llm_config = llm_config or {}
        self.builder_config_path = builder_config_path
#       self.validate_llm_config()
        self.builder = self.create_builder()
        self.Zilliz_agent = ZillizRetrievalAgent(**zilliz_config) if zilliz_config else None

    def execute_code(self, code: str) -> str:
        """
        Execute a Python code snippet and return the result.
        Args:
            code (str): The Python code to execute.
        Returns:
            str: The output of the executed code.
        """
        ipython = get_ipython()
        result = ipython.run_cell(code)
        output = str(result.result)
        if result.error_before_exec is not None:
            output += f"\n{result.error_before_exec}"
        if result.error_in_exec is not None:
            output += f"\n{result.error_in_exec}"
        return output

    def create_builder(self) -> AgentBuilder:
        """
        Create an instance of AgentBuilder.
        """
        if not self.builder_config_path:
            raise ValueError("Builder config path is required to create AgentBuilder.")
        return AgentBuilder(
            config_path= '',
            builder_model='gpt-4-1106-preview',
            agent_model='gpt-4-1106-preview'
        )

    def build_agents_for_task(self, task_description: str):
        """
        Build agents for a specific task using the AgentBuilder.
        Args:
            task_description (str): A description of the task for which agents are to be built.
        """
        try:
            agent_list, agent_configs = self.builder.build(task_description, self.__get_autogen_config(), coding=True)
            print(f"Agents built successfully for task: '{task_description}'")
            return agent_list, agent_configs
        except Exception as e:
            print(f"Error in building agents for task '{task_description}': {e}")

    def create_assistant_agent(self, name: str, persona: str = ASSISTANT_PERSONA) -> autogen.AssistantAgent:
        return autogen.AssistantAgent(name=name, system_message=persona, llm_config=self.__get_autogen_config())

    def create_user_agent(
        self, name: str, max_auto_reply: Optional[int] = None, human_input: Optional[str] = "ALWAYS"
    ) -> autogen.UserProxyAgent:
        return autogen.UserProxyAgent(
            name=name,
            human_input_mode=human_input,
            max_consecutive_auto_reply=max_auto_reply,
            function_map=self.__get_function_map(),
        )
    
    def perform_retrieval(self, query_vector: List[float], top_k: int = 10):
        if not self.Zilliz_agent:
            raise ValueError("Zilliz agent is not configured.")
        return self.Zilliz_agent.search([query_vector], top_k, {"nprobe": 16})

#   def validate_llm_config(self):
#       if self.llm_config.get("type") == "openai":
#           if not self.llm_config.get("openai_api_key"):
#               raise ValueError("OpenAI API key is required for OpenAI LLM.")
#       elif self.llm_config.get("type") == "azure":
#           required_keys = ["azure_api_key", "azure_deployment", "azure_endpoint"]
#           if any(key not in self.llm_config for key in required_keys):
#               raise ValueError("Azure OpenAI API configuration is incomplete.")
#       else:
#           raise ValueError("LLM type not provided, must be 'openai' or 'azure'.")

    def update_llm_config(self, new_config: Dict):
        self.llm_config = new_config
        self.validate_llm_config()

    def load_semantic_kernel_plugins(self, plugins: List[str]):
        """
        Load Semantic Kernel plugins into the kernel.
        Args:
            plugins (List[str]): A list of plugin names to load.
        """
        for plugin in plugins:
            try:
                self.kernel.import_skill(plugin)
                print(f"Plugin '{plugin}' loaded successfully.")
            except Exception as e:
                print(f"Error loading plugin '{plugin}': {e}")

    def __get_autogen_config(self) -> Dict:

        desired_model = "gpt-4-1106-preview"  # Update this with your choice of model

        for config in self.llm_config:
            if config.get("model") == desired_model:
                return {
                    "functions": self.__get_function_definitions(),
                    "config_list": [config]
                }
        raise ValueError(f"No suitable LLM configuration found for model '{desired_model}'.")

    def __get_function_definitions(self) -> List:
        functions = []
        sk_functions = self.kernel.skills.get_functions_view()
        for ns, funcs in {**sk_functions.native_functions, **sk_functions.semantic_functions}.items():
            for f in funcs:
                if len(f.parameters) == 1 and f.parameters[0].type_ == "string":
                    functions.append({
                        "name": f.name,
                        "description": f.description,
                        "parameters": {
                            "type": "object",
                            "properties": {f.parameters[0].name: {"description": f.parameters[0].description, "type": "string"}},
                            "required": [f.parameters[0].name]
                        }
                    })
        return functions

    def __get_function_map(self) -> Dict:
        function_map = {}
        sk_functions = self.kernel.skills.get_functions_view()
        for ns, funcs in {**sk_functions.native_functions, **sk_functions.semantic_functions}.items():
            for f in funcs:
                function_map[f.name] = self.kernel.skills.get_function(f.skill_name, f.name)
        return function_map