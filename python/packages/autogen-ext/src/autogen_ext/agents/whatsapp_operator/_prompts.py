WHATSAPP_OPERATOR_TOOL_PROMPT_MM = """
{state_description}

Consider the following screenshot of Whatsapp. The messages are on the right side and contacts/groups are on the left side of the screenshot. In this screenshot, interactive elements are outlined in bounding boxes of different colors. Each bounding box has a numeric ID label in the same color. Additional information about each visible label is listed below:

{visible_targets}{other_targets_str}{focused_hint}

You are to respond to my next request by selecting an appropriate tool from the following set, or by answering the question directly if possible:

{tool_names}

When deciding between tools, consider if the request can be best addressed by:
    - the contents of the CURRENT VIEWPORT (in which case actions like clicking links, clicking buttons, inputting text, or hovering over an element, might be more appropriate)
    - contents found elsewhere on the CURRENT WEBPAGE [{title}]({url}), in which case actions like scrolling, summarization, or full-page Q&A might be most appropriate
    - If you want to scroll up or down, first click on atleast one element in the part of the screen you want to scroll. This will ensure that the scroll action is performed in the correct part of the screen.
    - For scrolling up and down in the messages click on atleast one element in the messages area. For scrolling up and down in the contacts/groups click on atleast one element in the contacts/groups area.

My request follows:
"""

WHATSAPP_OPERATOR_TOOL_PROMPT_TEXT = """
{state_description}

You have also identified the following interactive components:

{visible_targets}{other_targets_str}{focused_hint}

You are to respond to my next request by selecting an appropriate tool from the following set, or by answering the question directly if possible:

{tool_names}

When deciding between tools, consider if the request can be best addressed by:
    - the contents of the CURRENT VIEWPORT (in which case actions like clicking links, clicking buttons, inputting text, or hovering over an element, might be more appropriate)
    - contents found elsewhere on the CURRENT WEBPAGE [{title}]({url}), in which case actions like scrolling, summarization, or full-page Q&A might be most appropriate
    - If you want to scroll up or down, first click on atleast one element in the part of the screen you want to scroll. This will ensure that the scroll action is performed in the correct part of the screen.

My request follows:
"""


WHATSAPP_OPERATOR_QA_SYSTEM_MESSAGE = """
You are a helpful assistant that can summarize long list of messages to answer question.
"""


def WHATSAPP_OPERATOR_QA_PROMPT(title: str, question: str | None = None) -> str:
    base_prompt = f"We are visiting whatsapp. Its full-text content are pasted below, along with a screenshot of the page's current viewport."
    if question is not None:
        return (
            f"{base_prompt} Please summarize the messages into one or two paragraphs with respect to '{question}':\n\n"
        )
    else:
        return f"{base_prompt} Please summarize the messages into one or two paragraphs:\n\n"
