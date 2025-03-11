from typing import TypedDict


class AgentState(TypedDict):
    message: str
    error: bool
    error_message: str
    file_path: str
    code: str
    iterations: int
    no_content: bool
    code_rewritten: bool