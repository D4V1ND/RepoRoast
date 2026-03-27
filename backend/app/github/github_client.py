import os
import shutil
from git import Repo
import stat

def remove_readonly(func, path, _):
    """Helper for shutil.rmtree to handle read-only files."""
    os.chmod(path, stat.S_IWRITE)
    func(path)
    
def get_repo(repo_url: str, local_dir: str = "./temp_repo", replace: bool = False):
    """
    Clones a Github repo to a local folder.
    If replace=True, delete the folder first.
    """
    if replace and os.path.exists(local_dir):
        print(f"Deleting existing folder {local_dir}...")
        shutil.rmtree(local_dir, onerror=remove_readonly)
    elif os.path.exists(local_dir):
        # Folder exists and replace=False; use it as is
        print(f"Using existing folder {local_dir}...")
        return local_dir

    print(f"Cloning {repo_url} into {local_dir}...")
    Repo.clone_from(repo_url, local_dir)
    print("Clone completed")
    return local_dir

def filter_repo_generic(tree, path="", optional=False):
    SOURCE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".java", ".cpp"}
    OPTIONAL_EXTENSIONS = {".ipynb", ".csv", ".json", ".jsonl", ".txt"}
    INCLUDE_ROOT = {"README.md", "requirements.txt", "package.json", "package-lock.json"}
    SKIP_FOLDERS = {".git", ".idea", "node_modules", ".next", "dist", "public", "archive"}
    SKIP_EXTENSIONS = {".pkl", ".faiss", ".zip", ".tar.gz", ".mp4", ".png", ".jpg", ".svg"}
    filtered = {}
    for key, value in tree.items():
        if key == "__files__":
            filtered_files = []
            for file in value:
                ext = "." + file.split(".")[-1] if "." in file else ""
                if path == "" and file in INCLUDE_ROOT:
                    filtered_files.append(file)
                elif ext in SOURCE_EXTENSIONS:
                    filtered_files.append(file)
                elif ext in OPTIONAL_EXTENSIONS and optional: 
                    filtered_files.append(file)
            if filtered_files:
                filtered["__files__"] = filtered_files
        elif isinstance(value, dict):
            if key in SKIP_FOLDERS:
                continue
            new_path = f"{path}/{key}" if path else key
            sub_filtered = filter_repo_generic(value, new_path)
            if sub_filtered:
                filtered[key] = sub_filtered
    return filtered