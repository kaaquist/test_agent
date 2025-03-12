import pytest

from models.agent_state import AgentState


@pytest.fixture
def state():
    """
    Fixture for the AgentState.
    """
    return AgentState(
        message="",
        error=False,
        error_message="",
        file_path="",
        code="",
        iterations=0,
        no_content=False,
        code_rewritten=False
    )