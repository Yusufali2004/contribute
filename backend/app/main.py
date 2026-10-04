from fastapi import FastAPI, HTTPException
from app.crawler import crawl_repository
from app.rag import index_files, search_repository
from app.github import parse_github_url, get_repository
from app.analyzer import ask_gemma

app = FastAPI(title="CONTRIBUTE API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/repository")
async def repository(url: str):
    try:
        owner, repo = parse_github_url(url)

        data = await get_repository(owner, repo)

        return {
            "owner": owner,
            "repo": repo,
            "name": data["name"],
            "full_name": data["full_name"],
            "description": data["description"],
            "html_url": data["html_url"],
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "language": data["language"],
            "default_branch": data["default_branch"],
            "open_issues": data["open_issues_count"],
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch repository"
        )

@app.get("/api/repository/files")
async def repository_files(url: str):
    try:
        owner, repo = parse_github_url(url)

        data = await get_repository(owner, repo)

        result = await crawl_repository(
            owner,
            repo,
            data["default_branch"]
        )

        return {
            "repository": data["full_name"],
            "file_count": result["file_count"],
            "files": result["files"],
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/api/repository/index")
async def index_repository(url: str):
    try:
        owner, repo = parse_github_url(url)

        data = await get_repository(
            owner,
            repo
        )

        result = await crawl_repository(
            owner,
            repo,
            data["default_branch"]
        )

        count = index_files(
            data["full_name"],
            result["files"]
        )

        return {
            "repository": data["full_name"],
            "indexed_chunks": count,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/api/repository/search")
async def search_repository_endpoint(
    url: str,
    q: str
):
    try:
        owner, repo = parse_github_url(url)

        data = await get_repository(
            owner,
            repo
        )

        results = search_repository(
            data["full_name"],
            q
        )

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/api/repository/ask")
async def ask_repository(
    url: str,
    q: str
):
    try:
        owner, repo = parse_github_url(url)

        data = await get_repository(
            owner,
            repo
        )

        results = search_repository(
            data["full_name"],
            q,
            n_results=5
        )

        answer = ask_gemma(
            q,
            results
        )

        return {
            "question": q,
            "answer": answer,
            "sources": [
                metadata.get("path")
                for metadata in results.get(
                    "metadatas",
                    [[]]
                )[0]
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )