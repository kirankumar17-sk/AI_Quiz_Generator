from fastapi import FastAPI, HTTPException, Request  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
import os, json

from database import SessionLocal, create_tables, Quiz
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz  # keep your existing LLM integration

app = FastAPI()
create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_quiz")
async def generate_quiz_endpoint(payload: dict):
    url = payload.get("url")
    if not url or not url.startswith("https://en.wikipedia.org/wiki/"):
        raise HTTPException(status_code=400, detail="Invalid Wikipedia URL. Use https://en.wikipedia.org/wiki/ARTICLE_TITLE")

    try:
        title, article_text = scrape_wikipedia(url)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Convert scraping/fetching errors into a friendly 502/503 for the client
        raise HTTPException(status_code=502, detail=f"Failed to fetch article content: {e}")

    # If your LLM requires a key and might fail, you may want to catch and return meaningful error messages
    try:
        quiz_data = generate_quiz(title, article_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")

    db = SessionLocal()
    quiz_obj = Quiz(
        url=url,
        title=quiz_data.article_title,
        scraped_content=article_text,
        full_quiz_data=json.dumps(quiz_data.dict())
    )
    db.add(quiz_obj)
    db.commit()
    db.refresh(quiz_obj)
    db.close()

    return quiz_data.dict()