import os
import json
from dotenv import load_dotenv  # type: ignore

# Core LangChain pieces (v1 uses langchain_core)
from langchain_core.prompts import PromptTemplate  # type: ignore
try:
    from langchain_core.output_parsers import JsonOutputParser  # type: ignore
except Exception:
    JsonOutputParser = None

# Gemini integration
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore

# Pydantic model for validation
from models import QuizOutput

# Load .env file from the backend directory
from pathlib import Path
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)  # loads GEMINI_API_KEY if present in .env

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY", None)
# Strip quotes and whitespace if present (common when copying from some sources)
if GOOGLE_API_KEY:
    GOOGLE_API_KEY = GOOGLE_API_KEY.strip().strip('"').strip("'")
    # Debug: Print first and last few chars to verify (without exposing full key)
    if len(GOOGLE_API_KEY) > 10:
        print(f"✓ API key loaded (starts with: {GOOGLE_API_KEY[:4]}..., length: {len(GOOGLE_API_KEY)})")
    else:
        print(f"⚠️  Warning: API key seems too short: {len(GOOGLE_API_KEY)} characters")

# Prompt template
prompt_template = PromptTemplate.from_template(
    """
Read the following Wikipedia article content and generate a JSON quiz with 5-10 multiple-choice questions.
Include summary, key entities, and related topics. Use concise, factual answers.

Article Title: {title}

Article Text:
{article_text}

Return ONLY valid JSON that conforms to the format instructions below.
{format_instructions}
"""
)

# Initialize Gemini model (ensure GEMINI_API_KEY set or change to your auth method)
# model name can be adjusted to your available Gemini model
if GOOGLE_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it in your .env file or environment.")

# Try different model names in order of preference
# Common model names vary by API version and region
# You can set GEMINI_MODEL_NAME in .env to override
# To find available models, run: python list_models.py

# List of models to try in order (most common first)
MODEL_CANDIDATES = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest", 
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-pro",
    "models/gemini-1.5-flash-latest",
    "models/gemini-1.5-pro-latest",
    "models/gemini-1.5-pro",
    "models/gemini-pro",
]

# Get model name from env or use first candidate
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", MODEL_CANDIDATES[0])

# Initialize the model (validation happens at invoke time, not here)
model = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GOOGLE_API_KEY)

# If JsonOutputParser is available, use it. Otherwise fallback to manual parse+validation.
if JsonOutputParser is not None:
    parser = JsonOutputParser(pydantic_object=QuizOutput)
else:
    parser = None  # fallback below will run

def generate_quiz(title: str, article_text: str):
    """
    Generate quiz data (validated against QuizOutput pydantic model).
    Uses JsonOutputParser when available; otherwise falls back to JSON parse + pydantic validation.
    """
    format_instructions = parser.get_format_instructions() if parser is not None else (
        "Return a JSON object matching the QuizOutput pydantic schema. Example keys: "
        '{"article_title": "...", "summary": "...", "questions": [{"question":"", "options": ["",""], "answer":""}], '
        '"key_entities": [], "related_topics": [] }'
    )

    # Format the prompt using the template
    formatted_prompt = prompt_template.format(
        title=title,
        article_text=article_text,
        format_instructions=format_instructions,
    )

    # Invoke the model - returns an AIMessage object
    # Try the current model first, then fallback to alternatives if it fails
    global model, MODEL_NAME  # Declare globals at the start
    
    response = None
    last_error = None
    
    # Try current model and all alternatives
    models_to_try = [MODEL_NAME] + [m for m in MODEL_CANDIDATES if m != MODEL_NAME]
    
    for model_name_to_try in models_to_try:
        try:
            # Create a new model instance for this attempt
            test_model = ChatGoogleGenerativeAI(model=model_name_to_try, google_api_key=GOOGLE_API_KEY)
            response = test_model.invoke(formatted_prompt)
            # Success! Update the global model for next time
            model = test_model
            MODEL_NAME = model_name_to_try
            if model_name_to_try != os.getenv("GEMINI_MODEL_NAME", ""):
                print(f"Successfully using model: {MODEL_NAME}")
            break
        except Exception as model_error:
            error_msg = str(model_error)
            last_error = model_error
            # If it's a 404/not found error, try next model
            if "404" in error_msg or "not found" in error_msg.lower():
                continue
            else:
                # Different error (auth, rate limit, etc.), re-raise it
                raise
    
    if response is None:
        # All models failed
        raise RuntimeError(
            f"All Gemini models failed. Please:\n"
            "1. Check your GEMINI_API_KEY is valid\n"
            "2. Run 'python list_models.py' to see available models\n"
            "3. Set GEMINI_MODEL_NAME in your .env file to a valid model name\n\n"
            f"Last error: {last_error}"
        )

    # Extract content from AIMessage object
    # LangChain AIMessage has a .content attribute that contains the text
    response_text = response.content if hasattr(response, 'content') else str(response)

    # Try using the LangChain parser if available
    if parser is not None:
        try:
            # JsonOutputParser works with AIMessage objects directly
            parsed = parser.parse(response)
            
            # parser.parse returns a pydantic model instance or dict depending on implementation
            # Normalize to pydantic model
            if isinstance(parsed, dict):
                quiz = QuizOutput.model_validate(parsed)
            else:
                # If parsed is already a pydantic model
                quiz = parsed
            return quiz
        except Exception as e:
            # fall through to manual parse below
            print(f"JsonOutputParser failed, falling back to manual parse: {e}")

    # Fallback: try to extract JSON from the model text and validate with pydantic
    try:
        # If the model returned extra text, attempt to locate the first and last brace pair
        text = response_text.strip()
        # Try direct json.loads first
        try:
            data = json.loads(text)
        except Exception:
            # crude method to find JSON substring
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                json_sub = text[start:end+1]
                data = json.loads(json_sub)
            else:
                raise

        # Validate with pydantic (v2 syntax)
        quiz = QuizOutput.model_validate(data)
        return quiz
    except Exception as e:
        # Propagate a clear error so FastAPI can report it
        raise RuntimeError(f"Failed to parse LLM response as JSON matching QuizOutput: {e}\nModel output:\n{response_text}")