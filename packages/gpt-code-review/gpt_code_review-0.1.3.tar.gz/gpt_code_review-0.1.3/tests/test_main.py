from click.testing import CliRunner
from gpt_code_review.main import SomeFunctionClass

def test_cli():
    runner = CliRunner()
    result = runner.invoke(SomeFunctionClass.cli, ['--gpt_model', 'test-model', '--repo_path', '/path/to/repo'])
    assert result.exit_code == 0
    assert 'Generated message from GPT-3' in result.output
