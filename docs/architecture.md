# Architecture Overview

## 1. Overview

AI Resume Parser is a modular FastAPI-based system that extracts and analyzes resume data using NLP and ML.

## 2. Key Components

- **FastAPI** – Backend framework with automatic OpenAPI docs.
- **PostgreSQL** – Stores parsed resume data.
- **SQLAlchemy** – ORM for schema management.
- **PyPDF2 / DOCX / Tesseract** – Extracts text from multiple resume formats.
- **JWT Auth (python-jose)** – Handles secure authentication.
- **SlowAPI** – Provides per-user rate limiting.
- **Sentence Transformers** – Semantic job-resume matching.
- **Docker Compose** – Handles deployment of app + database.

## 3. Flow Diagram

User → `/upload` → Extraction → AI Parsing → Database → `/match` → Response

## 4. Scalability

- Stateless API (can scale horizontally)
- PostgreSQL optimized for concurrent reads
- Caching via rate-limiting and future Redis layer
