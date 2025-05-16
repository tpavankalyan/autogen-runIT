import sys

import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_ext.agents.whatsapp_operator import WhatsappOperator

azure_endpoint = "https://ai-tankalapavankalyan1043ai225872535216.openai.azure.com/"
azure_model = "gpt-4.1"
api_key="5KsTRepmOPk23t9VxaFSBUoZ1wRqniGfN40pB090c6SoPsu8o5o3JQQJ99BCACHYHv6XJ3w3AAAAACOGeMDH"
api_version="2024-12-01-preview"

async def main() -> None:

    model_client = AzureOpenAIChatCompletionClient(
        azure_deployment=azure_model,
        model=azure_model,
        api_version=api_version,
        azure_endpoint=azure_endpoint,  # Optional if you choose key-based authentication.
        api_key=api_key,  # For token-based authentication.
    )

    # Define an agent
    wa_agent = WhatsappOperator(
        name="WhatsappOperator",
        headless=False,
        browser_data_dir="/Users/tpavankalyan/Documents/repos/RunIT/profile/web.whatsapp.com",
        model_client=model_client,
    )

    # # Define a team
    # agent_team = RoundRobinGroupChat([web_surfer_agent], max_turns=50)

    # # Run the team and stream messages to the console
    # stream = agent_team.run_stream(task="1. Go To AI SUS group 2. Read last 50 messages 3. Summarize in a pointwise fashion.")
    # await Console(stream)
    # # Close the browser controlled by the agent
    # await web_surfer_agent.close()

    team = MagenticOneGroupChat([wa_agent], model_client=model_client)
    await Console(team.run_stream(task="Go to AI SUS group, list down atleast 5 people and their details, who are looking for people to share the stay."))



asyncio.run(main())