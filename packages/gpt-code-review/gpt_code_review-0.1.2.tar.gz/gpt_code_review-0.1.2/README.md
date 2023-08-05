# gpt_code_review

`gpt_code_review` is a Python package that helps in code review with the help of OpenAI's GPT-3.5 API. This package provides a simple command-line interface to generate a code review message for a given branch in a Git repository.

## Installation
To install gpt_code_review, you can use pip:

```bash
pip install gpt_code_review
```
## Usage

To use the gpt_code_review package, you need to have an OpenAI API key. You can get the API key from the OpenAI website (https://beta.openai.com/signup/).

```
token = YOUR_OPENAI_API_KEY, you can provided directly from the token flag, or you can set it in 'GPT_GTP_KEY' env variable
```

You can use the gpt_code_review command-line tool to generate a code review message for a given Git repository branch using the following command:

```bash
gpt_code_review --gpt_model=<gpt_model_name> --token=<your_openai_api_key> --repo_path=<path_to_git_repo> --main_branch=<main_branch_name> --review_branch=<review_branch_name>
```
The gpt_model_name is the name of the GPT-3.5 model you want to use. The your_openai_api_key is your OpenAI API key. The path_to_git_repo is the path to the Git repository you want to review. The main_branch_name is the name of the main branch of the Git repository. The review_branch_name is the name of the branch you want to compare with the main branch. If you do not specify the review_branch_name, it will use the active branch.

For example:

```bash
gpt_code_review --gpt_model=gpt-3.5-turbo --token=1234567890 --repo_path=/path/to/git/repo --main_branch=master --review_branch=feature-branch
```
This command will generate a code review message for the feature-branch branch in the /path/to/git/repo Git repository using the gpt-3.5-turbo GPT-3.5 model and the 1234567890 OpenAI API key.

Additionally, you can also import and use the GptService and GitService classes directly in your Python code. For example:



### Default values:
```
gpt_model = gpt-3.5-turbo
repo_path = '.'
main_branch = 'master'
review_branch = active branch
```

So the minimal usega:
```bash
gpt_code_review
```
Make the CR for active branch compare with master branch.

##License
gpt_code_review is released under the MIT License. See LICENSE for more information.
