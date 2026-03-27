from app.github.github_client import get_repo

def retriever_node(state): 
    local_dir = get_repo(state["url"])
    return {"local_dir": local_dir}
