"""
Helper script to create .env file for AI feature setup.
Run: python setup_env.py
"""
import os

def create_env_file():
    env_path = ".env"
    
    if os.path.exists(env_path):
        print(f"⚠️  {env_path} already exists!")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    print("\n=== AI Feature Setup ===")
    print("\nTo enable AI quiz generation, you need a Google Gemini API key.")
    print("Get your API key from: https://aistudio.google.com/app/apikey")
    print()
    
    api_key = input("Enter your GEMINI_API_KEY (or press Enter to skip): ").strip()
    
    if not api_key:
        print("\n⚠️  No API key provided. Creating .env file with placeholder.")
        api_key = "your_gemini_api_key_here"
    
    model_name = input("\nEnter GEMINI_MODEL_NAME (optional, press Enter for auto-selection): ").strip()
    
    env_content = f"""# Google Gemini API Configuration
# Get your API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY={api_key}

# Optional: Specify which Gemini model to use
# Leave commented to use automatic model selection
# Available models: gemini-1.5-flash-latest, gemini-1.5-pro-latest, gemini-1.5-pro, gemini-pro
"""
    
    if model_name:
        env_content += f"GEMINI_MODEL_NAME={model_name}\n"
    else:
        env_content += "# GEMINI_MODEL_NAME=gemini-1.5-flash-latest\n"
    
    env_content += """
# Database Configuration (optional - defaults to SQLite)
# DATABASE_URL=sqlite:///./quiz_history.db
"""
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print(f"\n✅ Created {env_path} file successfully!")
        
        if api_key == "your_gemini_api_key_here":
            print("\n⚠️  Remember to replace 'your_gemini_api_key_here' with your actual API key!")
        else:
            print("\n✅ API key configured. Restart your backend server to apply changes.")
            
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file()

