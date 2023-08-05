from unittest.mock import patch
from gpt_code_review.git_service import GitService

@patch('gpt_code_review.git_service.git.Repo')
def test_init(mock_repo):
    mock_repo.return_value = 'Mock repo'
    service = GitService(repo_path='/path/to/repo', main_branch='main', review_branch='feature')
    assert service.repo == 'Mock repo'
    assert service.main_branch == 'main'
    assert service.review_branch == 'feature'

def test_get_diff():
    mock_commit = {'diff.return_value': ['file1.diff', 'file2.diff']}
    mock_review_branch = {'commit': mock_commit}
    service = GitService(main_branch='main', review_branch=mock_review_branch)
    diffs = service.get_diff()
    assert diffs == ['file1.diff', 'file2.diff']
