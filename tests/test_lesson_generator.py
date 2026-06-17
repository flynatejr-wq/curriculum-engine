import json
import pytest
from unittest.mock import patch, MagicMock

from app.services.lesson_generator import generate_lesson

VALID_LESSON = {
    "objective": "Students will understand X",
    "key_points": ["Point A", "Point B", "Point C"],
    "activity": "Group discussion on X",
    "exit_ticket": "What is the main idea of X?",
}


def make_mock_client(lesson_dict):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(lesson_dict)
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


def test_generate_lesson_returns_dict():
    with patch("app.services.lesson_generator.client", make_mock_client(VALID_LESSON)):
        result = generate_lesson("Some textbook content")
    assert isinstance(result, dict)


def test_generate_lesson_has_all_required_keys():
    with patch("app.services.lesson_generator.client", make_mock_client(VALID_LESSON)):
        result = generate_lesson("Some textbook content")
    assert "objective" in result
    assert "key_points" in result
    assert "activity" in result
    assert "exit_ticket" in result


def test_generate_lesson_key_points_is_list():
    with patch("app.services.lesson_generator.client", make_mock_client(VALID_LESSON)):
        result = generate_lesson("Some textbook content")
    assert isinstance(result["key_points"], list)


def test_generate_lesson_raises_on_missing_keys():
    incomplete_lesson = {
        "objective": "Students will understand X",
        "key_points": ["Point A", "Point B"],
        # missing "activity" and "exit_ticket"
    }
    with patch("app.services.lesson_generator.client", make_mock_client(incomplete_lesson)):
        with pytest.raises(ValueError, match="missing required keys"):
            generate_lesson("Some textbook content")


def test_generate_lesson_sends_chunk_text_in_prompt():
    chunk = "The mitochondria is the powerhouse of the cell."
    mock_client = make_mock_client(VALID_LESSON)
    with patch("app.services.lesson_generator.client", mock_client):
        generate_lesson(chunk)
    call_args = mock_client.chat.completions.create.call_args
    messages = call_args.kwargs.get("messages") or call_args.args[0] if call_args.args else call_args.kwargs["messages"]
    user_message = next(m["content"] for m in messages if m["role"] == "user")
    assert chunk in user_message
