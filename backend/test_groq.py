import os
import sys
from dotenv import load_dotenv

load_dotenv(".env")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.rag import get_llm

print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER')}")
print(f"GROQ_API_KEY length: {len(os.getenv('GROQ_API_KEY') or '')}")

try:
    print("Initializing Groq LLM...")
    llm = get_llm()
    print(f"LLM initialized: {type(llm)}")
    
    print("Testing chat response...")
    response = llm.complete("Hello! Are you working?")
    print(f"Response: {response}")
    print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
