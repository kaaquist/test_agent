from unittest.mock import AsyncMock, MagicMock
from nodes.identify_filepath import identify_filepath

def test_identify_filepath_node(state):
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "This here is mocked"
    mock_model.invoke.return_value = mock_response

    state["message"] = "error_script.py"
    updated_state = identify_filepath(state=state, model=mock_model)
    print(updated_state)
    assert updated_state["file_path"] == "This here is mocked"
