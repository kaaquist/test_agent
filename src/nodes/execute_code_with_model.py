from tools.files.file_utils import read_code_from_file, write_code_to_file
from tools.python.python_repl import python_repl
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage


from models.agent_state import AgentState


def execute_code_with_model(state: AgentState, model) -> AgentState:

    code = read_code_from_file(state["file_path"])
    model_with_tools = model.bind_tools([python_repl])

    messages = [
        SystemMessage(
            content=""" You have got the task to execute code. Use the python_repl tool to execute it. It will return a message and your task is to detect if it was successfully run or produced an error.
            If the code produced an error just return 'True'. If it was successfully executed, return 'False'."""
        ),
        HumanMessage(content=code),
    ]

    ai_msg = model_with_tools.invoke(messages)
    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {"python_repl": python_repl}[tool_call["name"].lower()]
        tool_output = selected_tool.invoke(tool_call["args"])
        state["error_message"] = tool_output
        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

    result = model_with_tools.invoke(messages)
    # print(f"Result: {result}")
    # need to check if we get a result from the model, if not store this as no output from repl.
    if not result.content:
        # print(f"No content!! :: {result.content}  !!!")
        state["no_content"] = True
        state["iterations"] += 1
    else:
        # print(f"Content!! :: {result.content}  !!!", f"\n\nError message!!!: {state["error_message"]}", f"\n\n !!!! {bool(result.content == 'True')} !!!!")
        state["no_content"] = False
    state["error"] = bool(result.content=='True')  # if result.content else True
    state["code"] = code
    return state