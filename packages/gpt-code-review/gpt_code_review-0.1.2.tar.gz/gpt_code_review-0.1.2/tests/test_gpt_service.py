from unittest.mock import patch
from gpt_code_review.gpt_service import GptService

@patch('gpt_code_review.gpt_service.openai.ChatCompletion.create')
def test_send_message(mock_create):
    mock_create.return_value = {'choices': [{'message': {'content': 'Generated message from GPT-3'}}]}
    service = GptService()
    message = service.send_message()
    assert message == 'Generated message from GPT-3'

def test_get_message():
    service = GptService()
    service.send_message = lambda: {'choices': [{'message': {'content': 'Generated message from GPT-3'}}]}
    message = service.get_message()
    assert message == 'Generated message from GPT-3'
