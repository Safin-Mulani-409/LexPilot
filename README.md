# LexPilot AI

> Your AI Junior Advocate — a focused legal intelligence workspace for turning case files into structured hearing preparation.

## MVP

Upload a PDF case file, extract its text, and generate a structured report with a case summary, parties, facts, chronology, issues, information gaps, suggested questions, and a hearing checklist.

## Stack

- Frontend: React, Vite, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLAlchemy, Pydantic, PyMuPDF
- AI: OpenAI Responses API with structured JSON validation
- Data: SQLite for the MVP, PostgreSQL-ready configuration

## Repository layout

```text
frontend/                  React application
backend/                   FastAPI application
  app/api/routers/         HTTP endpoints
  app/services/            Case, document, AI and storage services
  app/models/              SQLAlchemy database models
  app/schemas/             Request and response contracts
  app/prompts/             Versioned AI prompt templates
  tests/                   Unit-test-ready test suite
docs/                      Architecture and API notes
```

## Run locally

### 1. Backend

```powershell
cd backend
python -m venv .venv  # Use Python 3.12 or 3.13 for the broadest package compatibility.
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

Set `OPENAI_API_KEY` in `backend/.env` to enable AI analysis. Without it, LexPilot produces a clearly-labelled deterministic demo report, keeping the application demoable offline.

### 2. Frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open `http://localhost:5173`.

## Architecture

Routers contain HTTP concerns only. `CaseService` orchestrates use-cases; `DocumentService` owns text extraction; `AIService` is the single OpenAI integration point; repository classes encapsulate persistence; and `StorageService` can later be replaced with S3 without changing application workflows.

Analysis is asynchronous: upload creates a case, then analysis is triggered independently and report status can be polled. This protects users from long document and model-processing requests.

## API

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/api/v1/cases/upload` | Upload a PDF and create a case |
| `POST` | `/api/v1/cases/{case_id}/analyze` | Start report generation |
| `GET` | `/api/v1/cases` | List cases |
| `GET` | `/api/v1/cases/{case_id}` | Get a case and its latest report |
| `GET` | `/api/v1/reports/{report_id}` | Get a full report |

## Roadmap

The current MVP intentionally excludes authentication, research, contracts, drafting, cause lists, and client management. The feature-oriented frontend and service boundaries are ready for those modules in later releases.

## Disclaimer

LexPilot assists legal professionals with document organisation and preparation. It does not provide legal advice and all output must be independently reviewed by a qualified advocate.
