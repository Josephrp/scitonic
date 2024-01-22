import os
import gradio as gr
import autogen
from src.mapper.e5map import E5Mapper
from src.mapper.scimap import scimap
from src.mapper.parser import MapperParser
from src.datatonic.dataloader import DataLoader
from src.teams.agentteam import codingteam, covid19team, financeteam, debateteam, homeworkteam, consultingteam

title = """# Welcome to 👩🏻‍🔬🧪SciTonic
this is a highly adaptive technical operator that will listen to your query and load datasets and multi-agent teams based on those. Simply describe your problem in detail, ask a question and provide a reasoning method to get started:
"""

def update_config_file(api_key):
    config_path = "./config/OAI_CONFIG_LIST.json"
    with open(config_path, "r") as file:
        config = json.load(file)

    for item in config:
        item["api_key"] = api_key

    with open(config_path, "w") as file:
        json.dump(config, file, indent=4)

def process_query(oai_key, query, max_auto_reply):
    update_config_file(oai_key)
    os.environ['OAI_KEY'] = oai_key
    llm_config = autogen.config_list_from_json(
        env_or_file="./config/OAI_CONFIG_LIST.json",
        filter_dict={"model": {"gpt-4", "gpt-3.5-turbo-16k", "gpt-4-1106-preview"}}
    )

    # Initialize mappers
    taskmapper = E5Mapper(oai_key)
    teammapper = scimap(oai_key)

    # Get responses from mappers
    taskmap_response = taskmapper.get_completion(query)
    teammap_response = teammapper.get_completion(query)

    # Parse responses
    task = MapperParser.parse_taskmapper_response(taskmap_response)
    team = MapperParser.parse_teammapper_response(teammap_response)

    # Load dataset based on task
    data_loader = DataLoader()
    dataset = data_loader.load_and_process(task.lower())

    # Save dataset to a JSON file and get the file path
    json_file_path = "./src/datatonic"  # Define the JSON file path
    data_loader.save_to_json(dataset, json_file_path)

    # Initialize AgentsFactory with the path to the JSON file
    agents_factory = AgentsFactory(llm_config, json_file_path)

    # Retrieve the Boss Assistant agent
    boss_assistant = agents_factory.scitonic()

    # Select and initiate team based on team mapping
    team_function = {
        "CodingTeam": codingteam,
        "Covid19Team": covid19team,
        "FinanceTeam": financeteam,
        "DebateTeam": debateteam,
        "HomeworkTeam": homeworkteam,
        "ConsultingTeam": consultingteam
    }

    team_action = team_function.get(team, lambda: "No appropriate team found for the given input.")
    return team_action()

def main():
    with gr.Blocks() as demo:
        gr.Markdown(title)
        with gr.Row():
            txt_oai_key = gr.Textbox(label="OpenAI API Key", type="password")
            txt_query = gr.Textbox(label="Describe your problem in detail:")
            txt_max_auto_reply = gr.Number(label="Max Auto Replies", value=50)
        btn_submit = gr.Button("Submit")
        output = gr.Textbox(label="Output", readonly=True)

        btn_submit.click(
            process_query,
            inputs=[txt_oai_key, txt_query, txt_max_auto_reply],
            outputs=output
        )

    demo.launch()

if __name__ == "__main__":
    main()