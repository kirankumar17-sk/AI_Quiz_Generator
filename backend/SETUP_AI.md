# AI Feature Setup Guide

To enable the AI quiz generation feature, you need to configure your Google Gemini API key.

## Steps to Enable AI Feature:

### 1. Get Your Gemini API Key

1. Visit one of these URLs:
   - https://makersuite.google.com/app/apikey
   - https://aistudio.google.com/app/apikey

2. Sign in with your Google account
3. Click "Create API Key" or "Get API Key"
4. Copy your API key

### 2. Create .env File

Create a file named `.env` in the `backend` directory with the following content:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_actual_api_key_here

# Optional: Specify which Gemini model to use
# Leave commented to use automatic model selection
# GEMINI_MODEL_NAME=gemini-1.5-flash-latest
```

### 3. Replace the Placeholder

Replace `your_actual_api_key_here` with your actual Gemini API key.

### 4. Restart the Backend Server

After creating/updating the `.env` file, restart your backend server for the changes to take effect.

## Optional Configuration

### Model Selection

You can specify which Gemini model to use by uncommenting and setting `GEMINI_MODEL_NAME`:

```env
GEMINI_MODEL_NAME=gemini-1.5-flash-latest
```

Available models:
- `gemini-1.5-flash-latest` (fastest, recommended)
- `gemini-1.5-pro-latest` (more capable)
- `gemini-1.5-pro` (stable version)
- `gemini-pro` (legacy)

If not specified, the system will automatically try to find a working model.

## Verify Setup

To verify your API key and see available models, run:

```bash
cd backend
python list_models.py
```

This will list all available Gemini models for your API key.

## Troubleshooting

- **Error: "GEMINI_API_KEY environment variable is not set"**
  - Make sure the `.env` file exists in the `backend` directory
  - Check that the file is named exactly `.env` (not `.env.txt`)
  - Verify the `GEMINI_API_KEY=` line is present and has your key

- **Error: "Model not found"**
  - The system will automatically try alternative models
  - You can manually set `GEMINI_MODEL_NAME` in `.env` to a specific model
  - Run `python list_models.py` to see available models

