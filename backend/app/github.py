import httpx


GITHUB_API = "https://api.github.com"


def parse_github_url(url: str) -> tuple[str, str]:
    url = url.rstrip("/")

    if url.endswith(".git"):
        url = url[:-4]

    parts = url.split("/")

    if len(parts) < 2 or "github.com" not in url:
        raise ValueError("Invalid GitHub repository URL")

    owner = parts[-2]
    repo = parts[-1]

    if not owner or not repo:
        raise ValueError("Invalid GitHub repository URL")

    return owner, repo


async def get_repository(owner: str, repo: str):
    url = f"{GITHUB_API}/repos/{owner}/{repo}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 404:
        raise ValueError("Repository not found")

    response.raise_for_status()

    return response.json()

async def get_repository_tree(owner: str, repo: str, branch: str):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}"

    params = {"recursive": "1"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()

    return response.json()


async def get_file_content(
    owner: str,
    repo: str,
    path: str,
    branch: str
):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"

    params = {"ref": branch}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict) and data.get("encoding") == "base64":
        import base64

        return base64.b64decode(data["content"]).decode(
            "utf-8",
            errors="ignore"
        )

    return ""

async def get_repository_issues(owner: str, repo: str):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/issues"

    params = {
        "state": "open",
        "per_page": 30,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()

    issues = response.json()

    # GitHub's issues endpoint also returns pull requests.
    return [
        issue
        for issue in issues
        if "pull_request" not in issue
    ]
    
async def get_repository_issues(owner: str, repo: str):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/issues"

    params = {
        "state": "open",
        "per_page": 30,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    response.raise_for_status()

    issues = response.json()

    # GitHub's issues endpoint also returns pull requests.
    return [
        issue
        for issue in issues
        if "pull_request" not in issue
    ]