import streamlit as st
import asyncio
import sys
import os
from io import StringIO
import time # For simulating delay in async generator

# --- Configuration (from user script, with warnings) ---
AZURE_ENDPOINT = "https://ai-tankalapavankalyan1043ai225872535216.openai.azure.com/"
AZURE_MODEL = "gpt-4.1"
API_KEY = "5KsTRepmOPk23t9VxaFSBUoZ1wRqniGfN40pB090c6SoPsu8o5o3JQQJ99BCACHYHv6XJ3w3AAAAACOGeMDH" # pragma: allowlist secret
API_VERSION = "2024-12-01-preview"
BROWSER_DATA_DIR_ORIGINAL = "/Users/tpavankalyan/Documents/repos/RunIT/profile/web.whatsapp.com"
BROWSER_DATA_DIR_SANDBOX = "/home/ubuntu/whatsapp_profile" # Sandbox compatible path

# --- Streamlit UI ---
st.title("MSME.ai")

task_input = st.text_area("Enter the task for the WhatsApp agent:", "Go to AI SUS group, search for words like stay etc. in the messages and list down atleast 5 people and their details, who are looking for people to share the stay. Search for the group if you dont see it.", key="task_input_streaming")
run_button = st.button("Run Agent Task (Stream Output)", key="run_button_streaming")

output_area = st.container()
log_expander = st.expander("Agent Logs and Details (Streaming)")

# --- Agent Logic (adapted for streaming) ---
async def run_agent_task_streamer(task_description):
    wa_agent_instance = None # To ensure we can close it in finally

    try:
        from autogen_agentchat.teams import MagenticOneGroupChat
        from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
        from autogen_ext.agents.whatsapp_operator import WhatsappOperator
        from openai import AsyncAzureOpenAI
    except ImportError as e:
        yield f"**Error:** ImportError: {e}. Please ensure 'pyautogen' is installed. If 'autogen_ext' is a custom local library, it needs to be present. Check server logs for details.\n"
        return

    try:

        # os.makedirs(BROWSER_DATA_DIR_SANDBOX, exist_ok=True)

        model_client = AzureOpenAIChatCompletionClient(
            azure_deployment=AZURE_MODEL,
            model=AZURE_MODEL,
            api_version=API_VERSION,
            azure_endpoint=AZURE_ENDPOINT,
            api_key=API_KEY,
        )

        wa_agent_instance = WhatsappOperator(
            name="WhatsappOperator",
            headless=False, # Changed to True
            browser_data_dir=BROWSER_DATA_DIR_ORIGINAL, # Changed to sandbox path
            model_client=model_client,
        )

        team = MagenticOneGroupChat([wa_agent_instance], model_client=model_client)

        yield "---\n**Agent Output Stream:**\n"

        model_client2 = AsyncAzureOpenAI(
            api_version=API_VERSION,
            azure_endpoint=AZURE_ENDPOINT,
            api_key=API_KEY,
        )



        async def format_message_with_llm(message_content, message_source):
            response = await model_client2.chat.completions.create(
                            model=AZURE_MODEL,
                            messages=[{"role": "system", "content": "You are message formatter. Please take the message from either orchestrator or whatsapp operator and present them to the user in a crisp and informative way. It should feel like the orchestrator and whatsapp operator are talking to each other. Do not include messages from both. Directly give the message. Do not start with 'Orchestrator:' or 'WhatsappOperator:'. Just give the message. Do not include any other information."},
                                      {"role": "user", "content": f"{message_source}: {message_content}"}],
            )
            # Assuming the formatted response is in the first choice and under the 'message' key
            formatted_message = response.choices[0].message.content
            return formatted_message



        async for message in team.run_stream(task=task_description):
            if message.source == 'MagenticOneOrchestrator':
                # Format the message using LLM before yielding
                formatted_message = await format_message_with_llm(message.content, message.source)
                yield f"**Orchestrator:** {formatted_message}\n\n"
            elif message.source == 'WhatsappOperator':
                # Format the message using LLM before yielding
                formatted_message = await format_message_with_llm(message.content, message.source)
                yield f"**WhatsappOperator:** {formatted_message}\n\n"
            
            await asyncio.sleep(0.1)  # Simulate some delay for streaming effect

        yield "---\n**Log:** Agent task stream finished.\n"

    except Exception as e:
        # yield f"**Error:** An error occurred during agent execution: {e}\n"
        print(f"**Error:** An error occurred during agent execution: {e}", file=sys.stderr)
    finally:
        if wa_agent_instance:
            yield "**Log:** Attempting to close WhatsappOperator browser...\n"
            try:
                await wa_agent_instance.close()
                yield "**Log:** WhatsappOperator browser closed.\n"
            except Exception as close_e:
                yield f"**Warning:** Error closing WhatsappOperator: {close_e}\n"
        yield "**Log:** End of operation.\n"

if run_button:
    if task_input:
        output_area.info("Initiating agent task... Messages will stream below.")
        # Use st.write_stream to display the generator's output
        # The log_expander can also be updated, but st.write_stream is better for the main output
        # For simplicity, all output from the generator will go to the main area.
        # A more complex setup could split logs and agent messages.
        with output_area.status("Agent Running...", expanded=True):
            st.write_stream(run_agent_task_streamer(task_input))
        output_area.success("Agent task finished streaming.")

    else:
        output_area.warning("Please enter a task for the agent.")

