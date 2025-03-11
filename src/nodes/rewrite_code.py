from models.agent_state import AgentState
from tools.files.file_utils import write_code_to_file
from langchain_core.messages import SystemMessage, HumanMessage

def rewrite_code(state: AgentState, model) -> AgentState:
    state["code_rewritten"] = True
    code = state["code"]
    error = state["error_message"]
    state["iterations"] += 1

    messages = [
        SystemMessage(
            content="You can to analyze the following code and error provided in the user message. Your task is to fix that code and provide the user the correct new code. VERY IMPORTANT: ONLY RETURN THE UPDATED CODE, NOTHING ELSE! Dont use a markdown style, just the code as Text"
        ),
        HumanMessage(content=f"Code: {code} | Error: {error}"),
    ]
    ai_msg = model.invoke(messages)
    print("NEW SUGGESTED CODE:\n", ai_msg.content, f"\n{'-'*20}")
    write_code_to_file(file_path=f'{state["file_path"]}', code=ai_msg.content)
    state["code"] = ai_msg.content
    state["error"] = False
    return state
