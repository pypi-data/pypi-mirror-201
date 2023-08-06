# Upload Files to GitHub

This package provides a simple way to upload multiple files or directories to a GitHub repository using a command-line interface.

## Installation

You can install this package using pip:

```bash
pip install upload-files-to-github
```

## Usage - CLI

To upload files using the CLI, run the `upload_files_to_github.py` script with the following arguments:

```bash
python upload_files_to_github.py --files <file_or_directory_paths> --repo <user/repo> --token <github_token>
```

- `<file_or_directory_paths>`: a list of file or directory paths to upload, separated by spaces.
- `<user/repo>`: the GitHub repository where you want to upload the files.
- `<github_token>`: your GitHub personal access token.

For example, to upload all the files in the current directory to a repository `myuser/myrepo`, you can run:

```bash
python upload_files_to_github.py --files . --repo myuser/myrepo --token <github_token>
```

## Usage - Module

You can also use this package as a module in your Python code. After installing the package, you can import the `upload_files_to_github` function and use it as follows:

```python
from upload_files_to_github import upload_files_to_github

files = ['path/to/file1', 'path/to/file2']
repo = 'myuser/myrepo'
token = 'mygithubtoken'
upload_files_to_github(files, repo, token)
```

The `upload_files_to_github` function takes the same arguments as the CLI script, but `files` should be a list of file paths instead of a space-separated string.

Alternatively, you can also use the package as a module from the command line:

```bash
python -m upload_files_to_github --files <file_or_directory_paths> --repo <user/repo> --token <github_token>
```

This will run the `upload_files_to_github` function with the same arguments as the CLI script.