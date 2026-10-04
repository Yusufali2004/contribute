from fastapi import FastAPI, HTTPException
from app.crawler import crawl_repository
from app.rag import index_files, search_repository
from app.github import parse_github_url, get_repository
from app.analyzer import ask_gemma
from app.github import parse_github_url, get_repository
from app.crawler import crawl_repository
from app.rag import index_files, analyze_with_rag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CONTRIBUTE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        
@app.get("/api/repository/analyze")
async def analyze_repository(url: str):
    try:
        owner, repo = parse_github_url(url)

        repository = await get_repository(owner, repo)

        branch = repository["default_branch"]

        crawled = await crawl_repository(
            owner,
            repo,
            branch,
        )

        repository_name = repository["full_name"]

        indexed_chunks = index_files(
            repository_name,
            crawled["files"],
        )

        analysis = analyze_with_rag(
            repository_name,
            """
You are CONTribute, an AI onboarding assistant for open-source contributors.

Analyze this repository from the perspective of a developer making their
FIRST contribution.

Return the answer using exactly these sections:

# Repository Overview

Explain what the project does in 2-4 sentences.

# Architecture

Explain the major components and how data flows between them.

# Start Here

List the 5 most important files/directories a new contributor should inspect.
For each, explain why it matters.

# Setup

Explain how to run the project locally, but ONLY if the repository context
provides enough information. Never invent commands.

# Contribution Opportunities

Suggest exactly 3 realistic beginner-friendly improvements based on the
actual repository code.

For EACH opportunity use this format:

### [Title]
**Difficulty:** Easy / Medium
**Type:** AI-suggested contribution
**Why:** Explain why this is a useful contribution.
**Likely files:** List files supported by the repository context.
**Approach:** Give 2-4 practical steps.
**What you'll learn:** Explain the skills a contributor would gain.

# Contributor Roadmap

Give a short 4-step path:

1. Understand
2. Set up
3. Make a small change
4. Test and contribute

IMPORTANT RULES:

- Use ONLY information supported by the repository context.
- Never invent files, commands, technologies, endpoints, issues, or behavior.
- These are AI-suggested contribution opportunities, NOT existing GitHub issues.
- If evidence is insufficient for something, explicitly say so.
- Prefer small, realistic improvements over ambitious features.
- Ground recommendations in the actual code and documentation retrieved.

""",
        )

        return {
            "repository": repository_name,
            "url": repository["html_url"],
            "files_analyzed": crawled["file_count"],
            "indexed_chunks": indexed_chunks,
            "analysis": analysis,
        }

    except ValueError as e:
        return {"error": str(e)}

    except Exception as e:
        return {
            "error": "Failed to analyze repository",
            "details": str(e),
        }