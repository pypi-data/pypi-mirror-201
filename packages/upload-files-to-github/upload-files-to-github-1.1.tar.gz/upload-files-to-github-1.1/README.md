# Upload Files to GitHub

Upload multiple files or directories to a GitHub repository using the GitHub API.

## Installation

You can install `upload-files-to-github` using pip:

```
pip install upload-files-to-github
```

## Usage

You can use `upload-files-to-github` as a CLI tool or as a Python module.

### CLI Usage

The CLI tool requires the following arguments:

- `--files` or `-f`: A list of file or directory paths to upload.
- `--repo` or `-r`: The GitHub repository, in the format `user/repo`.
- `--token` or `-t`: The GitHub personal access token.
- `--branch` or `-b`: The branch to upload the files (default: `main`).

Example usage:

```
upload-files-to-github -f file.txt -r user/repo -t <github_access_token> -b main
```

You can also upload multiple files or directories at once:

```
upload-files-to-github -f dir1/ -f dir2/ -r user/repo -t <github_access_token>
```

### Module Usage

You can also use `upload-files-to-github` as a Python module:

```python
from upload_files_to_github import upload_files_to_github

files = ["file.txt", "dir1/", "dir2/"]
repo = "user/repo"
token = "<github_access_token>"
branch = "main"

upload_files_to_github(files, repo, token, branch)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# 上傳檔案到 GitHub

使用 GitHub API 上傳多個檔案或目錄到 GitHub 儲存庫。

## 安裝

可使用 pip 安裝 `upload-files-to-github`：

```
pip install upload-files-to-github
```

## 使用方法

`upload-files-to-github` 可作為 CLI 工具或 Python 模組使用。

### CLI 使用

CLI 工具需要以下參數：

- `--files` 或 `-f`：要上傳的檔案或目錄路徑清單。
- `--repo` 或 `-r`：GitHub 儲存庫，格式為 `user/repo`。
- `--token` 或 `-t`：GitHub 個人存取權杖。
- `--branch` 或 `-b`：要上傳檔案的分支（預設為 `main`）。

範例使用方法：

```
upload-files-to-github -f file.txt -r user/repo -t <github_access_token> -b main
```

也可一次上傳多個檔案或目錄：

```
upload-files-to-github -f dir1/ -f dir2/ -r user/repo -t <github_access_token>
```

### 模組使用

也可將 `upload-files-to-github` 作為 Python 模組使用：

```python
from upload_files_to_github import upload_files_to_github

files = ["file.txt", "dir1/", "dir2/"]
repo = "user/repo"
token = "<github_access_token>"
branch = "main"

upload_files_to_github(files, repo, token, branch)
```

## 授權

本專案採用 MIT 授權 - 詳情請參閱 [LICENSE](LICENSE) 檔案。