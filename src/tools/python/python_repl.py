from __future__ import annotations

from typing import Annotated

from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

repl = PythonREPL()

def read_code_from_file(file_path: str) -> str:
    with open(file_path) as file:
        code = file.read()
    return code


@tool
def python_repl(code: Annotated[str, "filename to read the code from"]):
    """Use this to execute python code read from a file. If you want to see the output of a value,
    Make sure that you read the code from correctly
    you should print it out with `print(...)`. This is visible to the user."""

    try:
        result = repl.run(code)
        print("RESULT CODE EXECUTION:", result)
    except BaseException as e:
        return f"Failed to execute. Error: {e!r}"
    return f"Executed:\n```python\n{code}\n```\nStdout: {result}"
