# SCAGS — Smart College & Branch Guidance System

A full-stack web application that helps JEE Mains students find the best colleges based on their percentile, preferred branch, fees budget, and location preferences.

---

## Features

- **JWT Authentication** — Register and login with secure password hashing
- **Real Recommendation Engine** — Queries a SQLite database of 50+ NIT/IIIT records with actual 2024 cutoffs
- **Scoring Algorithm** — Ranks colleges using a composite score (placement 40%, ranking 30%, cutoff margin 20%, fees 10%)
- **Filters** — Max fees and location filters
- **Modern Frontend** — Dark-themed SPA with real-time results
- **Dockerized** — Single-command deployment
- **CI/CD** — GitHub Actions pipeline that boots Flask and runs live API tests

---

## Tech Stack

| Layer     | Technology                         |
|-----------|------------------------------------|
| Backend   | Python, Flask, Flask-JWT-Extended  |
| Database  | SQLite                             |
| Auth      | JWT + Werkzeug password hashing    |
| Frontend  | Vanilla JS, HTML5, CSS3            |
| DevOps    | Docker, docker-compose, GitHub Actions |

---

## Quick Start

### 1. Clone
```bash
git clone https://github.com/Pushpenderrathore/SCAGS.git
cd SCAGS
```

### 2. Install dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Seed the database
```bash
python database/seed.py
```

### 4. Run the server
```bash
python backend/app.py
```

### 5. Open frontend
Open `frontend/index.html` in your browser (or serve via Live Server in VS Code).

---

## Docker

```bash
cp .env.example .env
# Edit JWT_SECRET in .env
docker-compose up --build
```

---

## API Endpoints

| Method | Endpoint           | Auth     | Description                          |
|--------|--------------------|----------|--------------------------------------|
| GET    | `/`                | No       | Health check                         |
| POST   | `/auth/register`   | No       | Create account                       |
| POST   | `/auth/login`      | No       | Login → returns JWT token            |
| POST   | `/recommend`       | JWT      | Get ranked college recommendations   |
| GET    | `/branches`        | No       | List all available branches          |

### POST `/auth/register`
```json
{ "username": "john", "email": "john@example.com", "password": "secret123" }
```

### POST `/auth/login`
```json
{ "username": "john", "password": "secret123" }
```
Returns: `{ "token": "<jwt>", "username": "john" }`

### POST `/recommend`
Header: `Authorization: Bearer <token>`
```json
{
  "percentile": 97.5,
  "branch": "CSE",
  "max_fees": 120000,
  "location": "Rajasthan"
}
```
Returns ranked list of colleges with SCAGS composite score.

---

## Scoring Algorithm

```
SCAGS Score = (Placement% / 100) × 40
            + max(0, (30 - ranking) / 30) × 30
            + min(margin / 10, 1) × 20
            + (1 - fees / 250000) × 10
```

---

## Project Structure

```
SCAGS/
├── backend/
│   ├── app.py              ← Flask app, blueprint registration
│   ├── db.py               ← SQLite connection helper
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py         ← /auth/register, /auth/login
│       └── recommend.py    ← /recommend, /branches
├── database/
│   ├── schema.sql          ← Table definitions
│   └── seed.py             ← 50+ college records
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── docker/
│   └── Dockerfile
├── .github/
│   └── workflows/main.yml
├── docker-compose.yml
├── .env.example
└── README.md
```
