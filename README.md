# AI Resume Parser

An intelligent resume parsing API powered by **FastAPI**, **NLP**, and **Machine Learning** — designed to extract, analyze, and structure candidate data with precision and scalability.

---

## Features

- Multi-format upload — PDF, DOCX, TXT, and image-based resumes
- AI-driven entity extraction (name, email, skills, experience, etc.)
- Resume-job relevance scoring using semantic embeddings
- JWT-secured authentication for protected endpoints
- Smart rate limiting using **SlowAPI**
- Full Dockerized microservice setup with **FastAPI** and **PostgreSQL**

---

## Tech Stack

| Layer                | Technology                                           |
| -------------------- | ---------------------------------------------------- |
| **Backend**          | FastAPI, Uvicorn                                     |
| **Database**         | PostgreSQL with SQLAlchemy ORM                       |
| **AI/NLP**           | Sentence Transformers, regex-based entity extraction |
| **Auth & Security**  | JWT (via python-jose), Passlib (bcrypt), SlowAPI     |
| **Testing**          | Pytest                                               |
| **Containerization** | Docker & Docker Compose                              |

---

## Project Structure

```
ai-resume-parser/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── setup.sh
├── README.md
│
├── src/
│   └── app/
│       ├── main.py
│       ├── db.py
│       ├── models.py
│       ├── schemas.py
│       ├── utils/
│       │   ├── ai_parser.py
│       │   └── anonymizer.py
│       └── routers/
│           ├── resumes.py
│           ├── health.py
│           └── auth.py
│
├── tests/
│   ├── test_health.py
│   └── test_resumes.py
│
└── .env.example
```

---

## API Endpoints

| Endpoint                 | Method | Description                                     |
| ------------------------ | ------ | ----------------------------------------------- |
| `/api/v1/resumes/upload` | `POST` | Upload and parse a resume (PDF/DOCX/TXT/Image)  |
| `/api/v1/resumes/match`  | `POST` | Match resume content to a given job description |
| `/api/v1/auth/login`     | `POST` | Generate JWT token for secure endpoints         |
| `/health`                | `GET`  | API health check                                |

---

#  Authentication (JWT)

Protected endpoints require a JWT access token.


### Default Test Credentials

For demo and testing purposes, use:

```
Username: ari12345  
Password: test1234
```


### 1️. Generate a JWT Token

**Endpoint:**

```
POST /api/v1/auth/token
```

**Example Body:**

```json
{
  "username": "ari12345",
  "password": "test1234"
}
```

---

### 2. Use the Token in Requests

Add this header to any protected endpoint (like `/upload`):

```
Authorization: Bearer <your_access_token>
```


## Testing

Run all tests inside Docker:

```bash
docker compose exec api pytest -v
```

---

## Docker Setup

### Option 1: One-click Setup (Recommended)

Run:

```bash
bash setup.sh
```

This will:

- Stop any running containers
- Build images without cache
- Start resume-api and resume-db services
- Initialize PostgreSQL and link all services automatically

Once setup completes, visit:

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Option 2: Manual Setup

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## Developer Commands

| Command                             | Description                 |
| ----------------------------------- | --------------------------- |
| `docker compose ps`                 | View running containers     |
| `docker compose logs -f`            | View real-time logs         |
| `docker compose exec api bash`      | Open shell in API container |
| `docker compose down`               | Stop all containers         |
| `docker compose exec api pytest -v` | Run tests                   |

---

## AI Processing Overview

The resume parser extracts structured information using a hybrid NLP pipeline combining:

- Transformer-based sentence embeddings for contextual understanding
- Regex and pattern recognition for accurate entity tagging
- Cleaned and anonymized outputs stored in PostgreSQL

This design ensures reliability, scalability, and compatibility across various file types without requiring large external model downloads.

---

## API Documentation

Auto-generated and accessible via:

```
http://localhost:8000/docs
```

Includes OpenAPI specification with schemas for all request and response models.

## Link To Presentation : 
### https://docs.google.com/presentation/d/1MTgBz3FDCmFBLP2c79EpuZory95_wEV_/edit?usp=sharing&ouid=110955731191591180458&rtpof=true&sd=true
