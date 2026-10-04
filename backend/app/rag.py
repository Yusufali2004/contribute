import chromadb

from app.analyzer import ask_gemma


client = chromadb.PersistentClient(
    path="./chroma_data"
)

collection = client.get_or_create_collection(
    name="repository_code"
)


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += chunk_size - overlap

    return chunks


def index_files(
    repository: str,
    files: list[dict]
):
    documents = []
    ids = []
    metadatas = []

    for file in files:

        chunks = chunk_text(
            file["content"]
        )

        for index, chunk in enumerate(chunks):

            if not chunk.strip():
                continue

            documents.append(chunk)

            ids.append(
                f"{repository}:{file['path']}:{index}"
            )

            metadatas.append({
                "repository": repository,
                "path": file["path"],
                "chunk": index,
            })

    if documents:
        collection.upsert(
            documents=documents,
            ids=ids,
            metadatas=metadatas,
        )

    return len(documents)


def search_repository(
    repository: str,
    query: str,
    n_results: int = 5
):
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={
            "repository": repository
        }
    )

    return results


def analyze_with_rag(repository: str, query: str) -> str:
    results = search_repository(
        repository=repository,
        query=query,
        n_results=8,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return "No relevant repository information was found."

    context_parts = []

    for document, metadata in zip(documents, metadatas):
        path = metadata.get("path", "unknown")
        context_parts.append(
            f"FILE: {path}\n"
            f"CONTENT:\n{document}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are CONTribute, an AI assistant for open-source contributors.

A developer wants to understand this repository.

Repository:
{repository}

Question:
{query}

Use ONLY the repository context below.

Do not invent files, commands, technologies, functions, issues,
or behavior that are not supported by the context.

If the context is insufficient, say what information is missing.

REPOSITORY CONTEXT:

{context}

Give a practical answer for a developer who wants to contribute
to this project.
"""

    return ask_gemma(prompt)