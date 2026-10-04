from app.github import (
    get_repository_tree,
    get_file_content,
)


IGNORED_DIRECTORIES = {
    "node_modules",
    ".git",
    ".next",
    "dist",
    "build",
    "__pycache__",
    "venv",
    ".venv",
}


IMPORTANT_FILES = {
    "README.md",
    "README",
    "CONTRIBUTING.md",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
}


ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".cs",
    ".html",
    ".css",
    ".md",
}


def should_include(path: str) -> bool:
    parts = path.split("/")

    if any(part in IGNORED_DIRECTORIES for part in parts):
        return False

    filename = parts[-1]

    if filename in IMPORTANT_FILES:
        return True

    return any(
        filename.endswith(extension)
        for extension in ALLOWED_EXTENSIONS
    )


async def crawl_repository(
    owner: str,
    repo: str,
    branch: str
):
    tree_data = await get_repository_tree(
        owner,
        repo,
        branch
    )

    files = []

    for item in tree_data.get("tree", []):

        if item.get("type") != "blob":
            continue

        path = item.get("path", "")

        if not should_include(path):
            continue

        # Don't pull gigantic files
        if item.get("size", 0) > 100_000:
            continue

        try:
            content = await get_file_content(
                owner,
                repo,
                path,
                branch
            )

            files.append({
                "path": path,
                "content": content,
                "size": item.get("size", 0),
            })

        except Exception:
            continue

    return {
        "files": files,
        "file_count": len(files),
    }