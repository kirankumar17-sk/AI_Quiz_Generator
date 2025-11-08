"""
Helper script to list available Gemini models for your API key.
Run this to see which models are available: python list_models.py
"""
import os
import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    print("\n=== Available Gemini Models ===\n")
    if 'models' in data:
        for model in data['models']:
            name = model.get('name', 'Unknown')
            display_name = model.get('displayName', '')
            supported_methods = model.get('supportedGenerationMethods', [])
            if 'generateContent' in supported_methods:
                print(f"✓ {name}")
                if display_name:
                    print(f"  Display Name: {display_name}")
                print(f"  Methods: {', '.join(supported_methods)}")
                print()
    else:
        print("No models found in response")
        print(f"Response: {data}")
except Exception as e:
    print(f"Error fetching models: {e}")
    print(f"\nTry checking your API key and network connection.")

