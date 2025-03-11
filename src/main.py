from __future__ import annotations

import os
from models.agent_state import AgentState
from langchain_openai import ChatOpenAI
from nodes.identify_filepath import identify_filepath
from nodes.execute_code_with_model import execute_code_with_model
from nodes.rewrite_code import rewrite_code
# from langchain_groq import ChatGroq
from functools import partial

from langgraph.graph import END, StateGraph

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL_NAME = os.environ.get("GROQ_MODEL_NAME")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME")


"""
This here is a sample to create a few agents that can be  supervised in a group using langchain langgraph and langgraph supervisor
"""

def next_step(state: AgentState):
    if state["iterations"] > 3:
        print("Max Iterations done.... Exit Agent")
        return "max_iterations"
    if state["no_content"]:
        print("No content from model")
        return "retry"
    if state["error"]:
        print(f"Error in {state['file_path']}. {state['iterations']} tries done")
        return "error"
    if not state["error"]:
        if state.get("code_rewritten", False):
            print(
                f"Code was probably fixed... check out {state['file_path']} if it is correct"
            )
        else:
            print("No error in code found.")
        return "ok"



def main():
    model = ChatOpenAI(
        temperature=0,
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL_NAME
    )

    workflow = StateGraph(AgentState)

    workflow.add_node("identify_filepath", partial(identify_filepath, model=model))
    workflow.add_node("execute_code_with_model", partial(execute_code_with_model, model=model))
    workflow.add_node("rewrite_code", partial(rewrite_code, model=model))
    workflow.add_node("retry",  partial(execute_code_with_model, model=model))

    workflow.set_entry_point("identify_filepath")
    workflow.add_edge("identify_filepath", "execute_code_with_model")

    workflow.add_conditional_edges(
        "execute_code_with_model",
        next_step,
        {"retry": "execute_code_with_model", "error": "rewrite_code", "ok": END, "max_iterations": END},
    )
    workflow.add_edge("rewrite_code", "execute_code_with_model")
    app = workflow.compile()
    app.invoke({"message": "Please analyze the error_script.py file", "iterations": 1})

if __name__ == "__main__":
    main()
