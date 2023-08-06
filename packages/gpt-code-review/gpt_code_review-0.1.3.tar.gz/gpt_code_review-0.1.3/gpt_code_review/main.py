import os

import click

from .gpt_service import GptService


class SomeFunctionClass:
    @staticmethod
    @click.command()
    @click.option('--gpt_model', default="gpt-3.5-turbo", help='gtp model for generate response')
    @click.option('--token', default=os.getenv('GPT_KEY'), help='You can add it here, or set GPT_KEY evn variable')
    @click.option('--repo_path', default='.', help='Path to repo')
    @click.option('--main_branch', default='master', help='main branch')
    @click.option('--review_branch', default=None, help='branch to compare')
    @click.option('--extend', default=False, help='branch to compare')
    def cli(gpt_model, token, repo_path, main_branch, review_branch, extend):
        service = GptService(gpt_model=gpt_model, token=token, repo_path=repo_path, main_branch=main_branch,
                             review_branch=review_branch, extend=extend)
        print(service.get_message())
