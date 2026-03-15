from app.github.repo_parser import scan_repo_structure_nested, save_tree, filter_repo_generic, extract_file_paths, load_files, chunk_documents, create_database

def preparation_node(state, output_file_name = "repo_structured_nested.json"): 
    local_dir = state["local_dir"]
    tree = scan_repo_structure_nested(local_dir)
    output_file = output_file_name
    save_tree(tree, output_file)
    filtered_tree = filter_repo_generic(tree)
    extracted_file_paths = extract_file_paths(filtered_tree)
    parsed_repo = load_files(local_dir, extracted_file_paths)
    chunked_documents = chunk_documents(parsed_repo)
    vector_db = create_database(chunked_documents, embeddings_model)
    retriever = vector_db.as_retriever(search_kwargs={"k":5})  # top 5 chunks
    qa_agent = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",  # how chunks are combined
        retriever=retriever,
        return_source_documents=True
    )
    return {"vector_db": vector_db, "chunked_documents": chunked_documents, "qa_agent": qa_agent}