# AI_Quiz_Generator
# AI Wikipedia Quiz Generator

A full-stack application that turns a Wikipedia article into a structured multiple-choice quiz using an LLM.  
Backend is Python (FastAPI) and frontend is React (Vite + Tailwind). The backend scrapes (or uses the REST summary), generates quizzes with a Gemini LLM via LangChain integration, and stores results in a local SQLite database. The frontend lets users generate quizzes and view history/details.

---

## Table of Contents

- Project Overview
- Features
- Requirements
- Repository Structure
- Backend — Setup & Run (Windows / macOS / Linux)
- Frontend — Setup & Run
- Environment Variables
- Database
- API Endpoints
- Example Requests
- Troubleshooting & Known Issues
- Development Notes
- Contributing
- License

---

## Project Overview

This project accepts a Wikipedia URL, extracts the article text, asks a Large Language Model to generate a quiz (5–10 MCQs + summary + metadata), stores the quiz and original content, and serves the quiz to the frontend. The architecture prioritizes reliability of scraping (uses Wikipedia REST summary API first, falls back to HTML scraping with a friendly User-Agent).

---

## Features

- Accepts a Wikipedia article URL and generates a quiz (summary, questions, key entities, related topics).
- Works with Gemini LLM via LangChain (langchain-google-genai).
- Stores quiz history (URL, title, generated date, scraped content, quiz JSON) in SQLite by default.
- Frontend (React + Tailwind) with:
  - Generate Quiz tab (enter URL, view quiz)
  - History tab (list saved quizzes, view details)
- Robust scraping: uses Wikipedia REST summary endpoint when possible; fallbacks to HTML with headers to avoid 403.
- Clear error handling and helpful status codes.

---

## Requirements

Backend
- Python 3.10 or 3.11 (Do NOT use Python 3.12+ / 3.13 — many dependencies may be incompatible)
- pip

Frontend
- Node.js (recommended LTS: 18.x or 20.x)
- npm (bundled with Node) or use nvm / nvm-windows to manage versions

Other
- Gemini API key (GEMINI_API_KEY) for LLM access (if you want quiz generation using Gemini). If not available, you can stub out the generator to return sample JSON for testing.

---

## Repository Structure

```
ai-quiz-generator/
├── backend/
│   ├── venv/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── scraper.py
│   ├── llm_quiz_generator.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── QuizDisplay.jsx
│   │   │   └── Modal.jsx
│   │   ├── services/api.js
│   │   └── tabs/
│   │       ├── GenerateQuizTab.jsx
│   │       └── HistoryTab.jsx
│   ├── tailwind.config.js
│   └── postcss.config.js
└── README.md
```

---

## Backend — Setup & Run

Important: use Python 3.10 or 3.11. If you currently have Python 3.13 installed, install Python 3.10/3.11 and recreate the venv.

1. Open a terminal and go to the backend directory:
   ```
   cd ai-quiz-generator/backend
   ```

2. Create a virtual environment (Windows PowerShell):
   ```
   py -3.10 -m venv venv
   .\venv\Scripts\Activate
   ```
   Or for macOS / Linux:
   ```
   python3.10 -m venv venv
   source venv/bin/activate
   ```

   Confirm:
   ```
   python --version
   # should output Python 3.10.x or 3.11.x
   ```

3. Upgrade pip and install dependencies:
   ```
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
   If you don't have `requirements.txt`, install required packages:
   ```
   python -m pip install fastapi uvicorn[standard] sqlalchemy beautifulsoup4 requests pydantic python-dotenv langchain-core langchain-community langchain-google-genai
   ```

4. Environment variables:
   - Create a `.env` file in `backend/` containing:
     ```
     GEMINI_API_KEY="your_gemini_api_key_here"
     DATABASE_URL="sqlite:///./quiz_history.db"  # optional; defaults to this if not set
     ```
   - Do not commit `.env`.

5. Start the server (recommended: use `python -m uvicorn` to avoid stale launchers):
   ```
   python -m uvicorn main:app --reload
   ```
   - Server: http://127.0.0.1:8000
   - API docs: http://127.0.0.1:8000/docs

---

## Frontend — Setup & Run

In a separate terminal:

1. Ensure Node.js and npm are installed:
   ```
   node -v
   npm -v
   ```
   If missing, install Node LTS from https://nodejs.org or use nvm/nvm-windows.

2. Go to the frontend folder:
   ```
   cd ai-quiz-generator/frontend
   ```

3. Install packages:
   ```
   npm install
   ```

4. Install Tailwind (if not already installed as devDependencies):
   ```
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
   If `npx tailwindcss init -p` fails, create these files manually:
   - `tailwind.config.js`
   - `postcss.config.js`
   and add Tailwind directives in `src/index.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

5. Start dev server:
   ```
   npm run dev
   ```
   Open: http://localhost:5173 (Vite default) — adjust if different.

---

## Environment Variables

Backend `.env` (in backend folder)
- GEMINI_API_KEY — your Gemini API key (if using Gemini)
- DATABASE_URL — optional SQLAlchemy URL (defaults to SQLite file `./quiz_history.db`)

Example `.env`:
```
GEMINI_API_KEY="sk-..."
DATABASE_URL="sqlite:///./quiz_history.db"
```

---

## Database

- Default: SQLite at `backend/quiz_history.db`.
- To switch to PostgreSQL or MySQL, set `DATABASE_URL` to a valid SQLAlchemy URL:
  - Postgres: `postgresql://user:pass@localhost:5432/dbname`
  - MySQL: `mysql+pymysql://user:pass@localhost:3306/dbname`
- Install the DB driver:
  - Postgres: `pip install psycopg2-binary`
  - MySQL: `pip install pymysql`

The app uses SQLAlchemy declarative model `Quiz` (id, url, title, date_generated, scraped_content, full_quiz_data).

---

## API Endpoints

- POST /generate_quiz
  - Body: `{ "url": "https://en.wikipedia.org/wiki/Alan_Turing" }`
  - Returns: generated quiz JSON (summary, questions, key_entities, related_topics)
- GET /history
  - Returns: list of saved quizzes (id, url, title, date_generated)
- GET /quiz/{quiz_id}
  - Returns: saved quiz object (full parsed JSON)

See Swagger UI: http://127.0.0.1:8000/docs

---

## Example Requests

Generate a quiz (curl):
```bash
curl -X POST "http://127.0.0.1:8000/generate_quiz" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Alan_Turing"}'
```

Get history:
```bash
curl "http://127.0.0.1:8000/history"
```

Get one quiz:
```bash
curl "http://127.0.0.1:8000/quiz/1"
```

---

## Troubleshooting & Common Issues

1. ModuleNotFoundError: No module named 'langchain'
   - Cause: packages not installed or wrong Python version.
   - Fix: ensure venv active and install:
     ```
     python -m pip install -r requirements.txt
     ```
     Ensure Python 3.10 or 3.11 is used.

2. Uvicorn "Fatal error in launcher" referencing Python313:
   - Cause: a uvicorn.exe launcher points to a removed Python. Fix by recreating venv and running uvicorn via the module:
     ```
     python -m uvicorn main:app --reload
     ```
   - To clean stale global launchers, locate and remove uvicorn.exe from the old Python Scripts folder.

3. Requests 403 when scraping Wikipedia
   - Cause: some websites block requests without a User-Agent.
   - Fix: scraper includes a friendly `User-Agent` and uses the Wikipedia REST API as a first attempt. If you still see 403, check network / proxy. You can modify `scraper.py` DEFAULT_HEADERS to a more descriptive UA.

4. LangChain / Gemini issues
   - Ensure `GEMINI_API_KEY` is set in `.env` and that the library versions used are compatible with your Python version.
   - If you don't have a valid Gemini key, you can stub `generate_quiz` to return sample JSON during development.

5. Node/Tailwind issues (`npx tailwindcss init -p` error)
   - Ensure `tailwindcss` is installed locally as devDependency:
     ```
     npm install -D tailwindcss postcss autoprefixer
     ```
   - Then run:
     ```
     npx tailwindcss init -p
     ```
   - If `npx` cannot determine executable, run the exact binary from `node_modules/.bin`:
     ```
     .\node_modules\.bin\tailwindcss init -p
     ```
   - Alternatively, create `tailwind.config.js` and `postcss.config.js` manually.

6. Google-related warnings about Python 3.10
   - Some Google client libs may warn that Python 3.10 is nearing end-of-life for those libraries; consider upgrading to Python 3.11 in the future.

---

## Development Notes

- The backend `scraper.py` uses the Wikipedia REST summary endpoint first for a reliable clean extract. If more content is required it falls back to HTML parsing of `#mw-content-text`.
- The LLM integration uses LangChain and `langchain-google-genai`. The sample code uses `JsonOutputParser` / Pydantic schema to validate output. Adjust the `llm_quiz_generator.py` prompt to tune output format and length.
- All complex quiz JSON is stored in `full_quiz_data` as a serialized JSON string.

---

## Contributing

- Fork the repo, create a feature branch, add tests where appropriate, and open a pull request.
- Please include reproducible steps for any bugfix.

---


---

If you want, I can:
- Generate a sample `.env.example` file,
- Provide a pre-filled `requirements.txt` tuned to your installed Python version,
- Or create a zip of a complete runnable codebase.
