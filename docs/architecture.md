# Architecture

## Design principles

- A case analysis is a workflow, not a chat session.
- Each layer depends inward: API → service → repository/model.
- File extraction, AI generation, storage, and persistence are independently replaceable.
- All model output is parsed into a Pydantic schema before it reaches the UI.

## Request lifecycle

```text
Browser → Case router → Case service → Local storage + Document service
Browser → Analysis router → Case service → AI service → Report repository
Browser ← Case/report read models ← Case router
```

## Extension points

`StorageService` is the boundary for a future S3 adapter. `DocumentService` is the boundary for OCR. `AIService` is the boundary for future research, drafting and contract-review methods. Feature folders in the frontend keep their views and state independent.

## Data model

`Case` owns one source `Document` and many `AnalysisReport` revisions. A report keeps the complete structured result as JSON, enabling new UI sections without schema migration. `AnalysisSource` preserves optional report-to-page references for future citation UX.
