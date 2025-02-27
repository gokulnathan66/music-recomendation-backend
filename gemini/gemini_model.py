import os
import google.generativeai as genai

from dotenv import load_dotenv, find_dotenv
import os

# Find .env file from the parent directory
dotenv_path = find_dotenv()

# Load environment variables from .env
load_dotenv(dotenv_path)


# Example: Accessing an environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

