import os
import openai
from .git_service import GitService

class GptService:
    def __init__(self, gpt_model="gpt-3.5-turbo", token=os.getenv('GPT_KEY'), repo_path='.', main_branch='master', review_branch=None, extend=False):
        self.openai = openai
        self.openai.api_key = token
        self.gpt_model = gpt_model
        self.git_service = GitService(repo_path=repo_path, main_branch=main_branch, review_branch=review_branch, extend=extend)

    def send_message(self):
        return openai.ChatCompletion.create(model=self.gpt_model,messages=[{"role": "user", "content": self.git_service.preper_message_for_chat()}])

    def get_message(self):
        result = self.send_message()
        return result['choices'][0]['message']['content']

    def send_completion_message(self, model='text-davinci-002'):
        return openai.Completion.create(model=model, prompt=self.git_service.preper_message_for_chat())
