import git


class GitService:
    def __init__(self, repo_path='.', main_branch='master', review_branch=None, extend=False):
        self.repo = git.Repo(repo_path)
        self.extend = extend
        self.main_branch = self.repo.branches[main_branch]
        self.review_branch = self.repo.branches[review_branch] if review_branch else self.repo.active_branch
        self.diffs = self.get_diff()

    def get_diff(self):
        return self.review_branch.commit.diff(self.get_base_commit())

    def get_base_commit(self):
        review_commit = self.review_branch.commit
        main_commit = self.main_branch.commit
        merge_base = self.repo.merge_base(review_commit, main_commit)
        if not merge_base:
            raise Exception('No merge base found')
        return self.repo.merge_base(review_commit, main_commit)[-1]

    def get_diffrence_per_file(self):
        changes_per_file = {}
        for i in self.get_diff():
            changes_per_file[i.a_path] = self.simple_diff(i.a_path)
        return changes_per_file

    def simple_diff(self, file_path):
        return self.repo.git.diff(self.main_branch, self.repo.active_branch.name, '--', file_path, unified=0,
                                  ignore_blank_lines=True, ignore_space_at_eol=True, ignore_space_change=True,
                                  ignore_all_space=True, ignore_submodules=True, ignore_cr_at_eol=True)

    def preper_message_for_chat(self):
        data = self.get_diffrence_per_file()

        result = """Make code review for this code ('-' at the start of the line mean that code was deleted and '+' mean that code was add): \n ```"""
        if self.extend:
            result += f'and make some example how to solve those problems \n'
        for diff in data:
            str_from_diff = f'{diff} \n {data[diff]}'
            result += str_from_diff
        return result + '```'
