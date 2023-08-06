from datetime import timedelta
from retry import retry
from github import Github
from .aes_crypt import AESCrypt
import os
import time
import json
import re


def get_file_list(repo):
    def get_file_names(contents):
        """
        A generator that recursively retrieves file names from a GitHub repository.
        """
        for file_content in contents:
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file_name = re.sub(r"^.+\/", "", file_content.path)
                yield file_name

    all_files = list(get_file_names(repo.get_contents("")))
    return all_files


def get_github_repo(token, repo_name):
    """
    連接 Github API，獲取指定名稱和 Token 的 Github 倉庫對象
    """
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(repo_name)
    return repo


def decrypt_data_from_github(filename, my_password, github_token, repo_name):
    repo = get_github_repo(token=github_token, repo_name=repo_name)

    # Create AESCrypt instance
    aes = AESCrypt(my_password)

    # Download encrypted file from Github
    download_file(repo=repo, filename=filename)

    # Read encrypted data from file
    with open(filename, "rb") as f:
        encrypted_data = (f.readline().strip(), f.readline().strip())

    # Decrypt data
    decrypted_data = aes.decrypt(encrypted_data)

    # Deserialize decrypted data into Python object
    data_decrypt = json.loads(decrypted_data.decode("utf-8"))

    return data_decrypt


@retry(exceptions=Exception, tries=3, delay=2, backoff=2)
def download_file(repo, filename):
    """
    從指定的 Github 倉庫下載檔案並保存在本地
    """
    cwd = os.path.abspath(os.getcwd())
    file_content = repo.get_contents(filename)
    file_content_data = file_content.decoded_content
    mode = "wb" if isinstance(file_content_data, bytes) else "w"
    with open(os.path.join(cwd, filename), mode) as f:
        f.write(file_content_data)
    print(f"{filename} downloaded")


@retry(exceptions=Exception, tries=3, delay=2, backoff=2)
def update_file(repo, filename):
    cwd = os.path.abspath(os.getcwd())
    try:
        contents = repo.get_contents(filename)
        sha = contents.sha
        print(f"{filename} EXISTS")
    except Exception as e:
        sha = None
        print(f"{filename} DOES NOT EXIST")

    with open(filename, "rb") as f:
        file_content = f.read()

    content = None
    if isinstance(file_content, str):
        with open(os.path.join(cwd, filename), "r") as f:
            content = f.read()
    elif isinstance(file_content, bytes):
        with open(os.path.join(cwd, filename), "rb") as f:
            content = f.read()

    if sha:
        repo.update_file(filename, "committing files", content, sha)
        print(f"{filename} UPDATED")
    else:
        repo.create_file(filename, "committing files", content)
        print(f"{filename} CREATED")


@retry(exceptions=Exception, tries=3, delay=2, backoff=2)
def delete_file(repo, filename):
    """
    刪除指定的 Github 倉庫中的檔案
    """
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(file.path)

    # 要刪除的檔案路徑
    git_file = filename

    if git_file in all_files:
        # 如果已存在，刪除檔案
        file = repo.get_contents(git_file)
        repo.delete_file(file.path, "Delete files", file.sha)
        print(f"{git_file} deleted")
    else:
        print(f"{git_file} does not exist.")


def get_execution_time(func):
    """
    裝飾器：計算函數執行時間
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = timedelta(seconds=end_time - start_time)
        ms = int(elapsed_time.total_seconds() * 1000)
        print("Function {} took {} ms to execute.".format(func.__name__, ms))
        return result

    return wrapper
