# this code is for listing the models available in the gemini api. 
# it will also test the connectivity to the gemini api.
# if the connectivity test fails, it will list the available models.

import os
import sys

print("Verifying setup...")

try:
    import aiogram
    print(f"aiogram imported successfully (version {aiogram.__version__})")
except ImportError as e:
    print(f"Error importing aiogram: {e}")
    sys.exit(1)

try:
    import google.generativeai as genai
    print(f"google.generativeai imported successfully (version {genai.__version__})")
except ImportError as e:
    print(f"Error importing google.generativeai: {e}")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment.")
    sys.exit(1)

print("Testing Gemini API connectivity...")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') # after deciding to choose what model do you want to run, just change this to the model name.

try:
    response = model.generate_content("Hello")
    print("Gemini API test successful!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Gemini API test failed: {e}")
    print("\nListing available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    sys.exit(1)

print("Setup verification complete.")
