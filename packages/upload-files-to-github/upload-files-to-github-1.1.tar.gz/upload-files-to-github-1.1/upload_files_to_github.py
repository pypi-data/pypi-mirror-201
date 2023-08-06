#!/usr/bin/env python
import argparse
import base64
import os

import requests
from dotenv import load_dotenv


def get_all_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def upload_files_to_github(files, repo, token, branch):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    repo_api_url = f"https://api.github.com/repos/{repo}"

    for file in files:
        file_path = os.path.normpath(file).replace("\\", "/")
        file_url = f"{repo_api_url}/contents/{file_path}"

        with open(file, "rb") as f:
            content = f.read()

        encoded_content = base64.b64encode(content).decode("utf-8")

        file_response = requests.get(file_url, headers=headers)
        file_exists = file_response.status_code != 404
        file_data = file_response.json() if file_exists else {}

        update_data = {
            "message": f"Update {file_path}",
            "content": encoded_content,
            "branch": branch,
        }

        if "sha" in file_data:
            update_data["sha"] = file_data["sha"]

        response = requests.put(file_url, json=update_data, headers=headers)
        response.raise_for_status()

        print(f"Successfully uploaded {file_path} to {repo}/{branch}/{file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload multiple files or directories to a GitHub repository.")
    parser.add_argument("--files", "-f", action="append", required=True,
                        help="List of file or directory paths to upload, e.g., '-f path/name' or '-f path/dir/'.")
    parser.add_argument("--repo", "-r", required=True, help="GitHub repository, format: 'user/repo'.")
    parser.add_argument("--token", "-t", help="GitHub personal access token.")
    parser.add_argument("--branch", "-b", default="main", help="Branch to upload the files (default: 'main').")
    args = parser.parse_args()

    load_dotenv()
    token = args.token or os.getenv("GITHUB_ACCESS_TOKEN")
    if not token:
        raise ValueError("You must provide a valid GitHub token.")

    all_files = []
    for file_or_dir in args.files:
        if os.path.isdir(file_or_dir):
            all_files.extend(get_all_files(file_or_dir))
        else:
            all_files.append(file_or_dir)

    upload_files_to_github(all_files, args.repo, token, args.branch)
