from typing import Dict
import json
import os
from pathlib import Path
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma



def scan_repo_structure_nested(repo_path):
    """
    Scan a repo folder and return a nested dictionary representing its structure.
    """
    def build_tree(current_path):
        tree = {}
        # List all items in the current directory
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                # If directory, recurse
                tree[item] = build_tree(item_path)
            else:
                # If file, just add to list
                tree.setdefault("__files__", []).append(item)
        return tree

    return build_tree(repo_path)

def extract_file_paths(tree, current_path=""): 
    files = []
    
    for key, value in tree.items(): 
        if key == "__files__": 
            for file in value: 
                path = f"{current_path}/{file}" if current_path else file
                files.append(path)
        else: 
            new_path = f"{current_path}/{key}" if current_path else key
            files.extend(extract_file_paths(value, new_path))

    return files

def save_tree(tree: Dict, file_name: str): 
    with open(file_name, "w", encoding="utf-8") as f: 
        json.dump(tree, f, indent=2)
    print(f"Nested repository structure saved to {file_name}")

from anytree import Node, RenderTree
# from anytree.exporter import DotExporter
from graphviz import Digraph
import json

def create_graph(output_file_json):
    with open(output_file, "r") as f: 
        tree = json.load(f)

    # Build anytree nodes
    def build_anytree(tree_dict, parent_node):
        for key, value in tree_dict.items():
            if key == "__files__":
                for file in value:
                    Node(file, parent=parent_node)
            else:
                folder_node = Node(key, parent=parent_node)
                build_anytree(value, folder_node)
    
    root = Node("root")
    build_anytree(tree, root)
    
    # Print ASCII tree in console
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")
    
    # DotExporter(root).to_picture("repo_tree_anytree.png")

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


def extract_file_paths(tree, current_path=""): 
    files = []
    
    for key, value in tree.items(): 
        if key == "__files__": 
            for file in value: 
                path = f"{current_path}/{file}" if current_path else file
                files.append(path)
        else: 
            new_path = f"{current_path}/{key}" if current_path else key
            files.extend(extract_file_paths(value, new_path))

    return files

def load_files(repo_path, file_paths, save = True): 
    documents = []

    for path in file_paths: 
        full_path = Path(repo_path) / path

        try: 
            with open(full_path, "r", encoding="utf-8") as f: 
                content = f.read()

            documents.append({
                "path": path, 
                "content": content
            })
        except: 
            print("hm")
            continue

    if save: 
        with open("parsed_repo.json", "w", encoding="utf-8") as f: 
            json.dump(documents, f, indent=2)
    return documents

def chunk_documents(documents, chunk_size: int = 800, chunk_overlap: int = 150): 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size, 
        chunk_overlap = chunk_overlap
    )

    chunks = []
    for doc in documents: 
        path = doc["path"]
        content = doc["content"]

        split_texts = splitter.split_text(content)
       
        for i, text in  enumerate(split_texts):
            chunks.append({
                "path": path, 
                "chunk_id": i, 
                "content": text, 
            })

    return chunks

def create_database(chunked_documents, embeddings_model):
    splitted_docs = [
        Document(page_content=chunk["content"], metadata={"path": chunk["path"]})
        for chunk in chunked_documents
    ]
    vector_db = Chroma.from_documents(
        documents = splitted_docs, 
        embedding = embeddings_model
    )
    return vector_db