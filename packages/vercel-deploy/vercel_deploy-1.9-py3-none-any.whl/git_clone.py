#!/usr/bin/env python
#!/usr/bin/env python
import argparse
import base64
import os

from dotenv import load_dotenv
from github import Github

load_dotenv()


def copy_directory(source_repo, target_repo, path=""):
    contents = source_repo.get_contents(path)
    for content in contents:
        if content.type == "dir":
            # 如果是目錄，則遞迴處理
            copy_directory(source_repo, target_repo, content.path)
        else:
            # 如果是檔案，則複製
            file_content = base64.b64decode(content.content).decode("utf-8")
            target_repo.create_file(content.path, f"Copy from {source_repo.full_name}", file_content)


def main(source_url, target_name):
    # 使用從 .env 檔案讀取的 Personal Access Token
    pat = os.getenv("GITHUB_ACCESS_TOKEN")
    g = Github(pat)

    source_repo = g.get_repo(source_url)
    user = g.get_user()
    new_repo = user.create_repo(target_name)

    copy_directory(source_repo, new_repo)
    response = f"git_clone.py {source_url}, {target_name}"
    print(response)
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="複製 GitHub repository")
    parser.add_argument("source_url", help="來源 repository 的 URL")
    parser.add_argument("target_name", help="新 repository 的名稱")

    args = parser.parse_args()

    main(args.source_url, args.target_name)
