# CONTribute

> Find your way into any codebase.

CONTribute is an AI-powered onboarding assistant that turns an unfamiliar
GitHub repository into a practical roadmap for making a first open-source
contribution.

Instead of asking a developer to understand an entire codebase before
contributing, CONTribute crawls the repository, retrieves relevant code and
documentation, and uses Gemma 4 to explain the project and suggest realistic
beginner-friendly contribution opportunities.

## The Problem

Contributing to open source can be intimidating for beginners.

A repository may contain hundreds of files, unfamiliar architecture,
multiple services, complex setup instructions, and issues that provide little
context about where to start.

The biggest barrier is often not writing code.

It is knowing **where to begin**.

## The Solution

CONTribute provides a guided path:

```text
GitHub Repository
       ↓
Repository Crawler
       ↓
Code + Documentation
       ↓
ChromaDB Retrieval
       ↓
Gemma 4
       ↓
Repository Intelligence
       ↓
Contributor Roadmap
```

A developer pastes a public GitHub repository URL and receives:

- Repository overview
- Architecture explanation
- Important files to inspect
- Setup guidance when supported by repository documentation
- Three AI-suggested beginner-friendly contribution opportunities
- Suggested implementation approach
- Skills the contributor can learn
- A simple contributor roadmap

## AI Model

CONTribute uses **Gemma 4** through the Gemini API as the repository
analysis and reasoning model.

Gemma receives repository context retrieved through ChromaDB and generates
contributor-oriented analysis.

The model is instructed to avoid inventing files, commands, issues, or
functionality that are not supported by the retrieved repository context.

## Retrieval-Augmented Generation

The repository is not simply pasted into a language model.

CONTribute:

1. Retrieves the GitHub repository tree.
2. Filters relevant source code and documentation.
3. Downloads repository files.
4. Splits files into manageable chunks.
5. Stores the chunks in ChromaDB.
6. Retrieves relevant chunks for a contributor question.
7. Sends the retrieved context to Gemma 4.
8. Generates grounded repository guidance.

## Features

### Repository Understanding

Understand an unfamiliar project's purpose and architecture.

### Important Files

Identify files a new contributor should inspect first.

### Contribution Opportunities

Generate realistic beginner-friendly contribution ideas grounded in the
repository.

These are explicitly marked as **AI-suggested contributions**, not existing
GitHub issues.

### Contributor Roadmap

Move from understanding the project to making a first contribution through
a simple step-by-step path.

## Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- Python
- FastAPI
- Uvicorn

### AI

- Gemma 4
- Gemini API

### Retrieval

- ChromaDB
- Retrieval-Augmented Generation (RAG)

### Repository Integration

- GitHub REST API

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Yusufali2004/contribute.git
cd contribute
```

### 2. Backend

```bash
cd backend
python -m venv .venv
```

Activate the environment.

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will run at:

```text
http://127.0.0.1:8000
```

### 3. Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Example

Try analyzing:

```text
https://github.com/Yusufali2004/smart-sort
```

CONTribute will crawl the repository and generate repository intelligence
using Gemma 4 and retrieved repository context.

## Project Structure

```text
contribute/
├── backend/
│   ├── app/
│   │   ├── analyzer.py
│   │   ├── crawler.py
│   │   ├── github.py
│   │   ├── main.py
│   │   └── rag.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── app/
│       └── page.tsx
│
├── .gitignore
├── LICENSE
└── README.md
```

## Open-Source AI

Gemma 4 is an important part of CONTribute's core functionality.

The project uses an open-weight AI model through the Gemini API to transform
retrieved repository context into practical contributor guidance.

Please review Google's current Gemma terms and model license/usage
requirements before deploying or redistributing the system.

