from __future__ import annotations

from models.agent_state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage


def identify_filepath(state: AgentState, model) -> AgentState:
    message = state["message"]

    messages = [
        SystemMessage(
            content="""Your task is to evaluate the userinput and extract the filename he provided.
                              ONLY return the last filename, nothing else!"""
        ),
        HumanMessage(content=message),
    ]
    result = model.invoke(messages)
    state["file_path"] = result.content
    return state