import os
import sys
from dotenv import load_dotenv

load_dotenv(".env")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Use the token extracted from the screenshot request header
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODI3Mjc5MjUsInN1YiI6IjQxNDA2ZGEyLWMzNjQtNDFkOS04ZjFiLTQzOGM3Mzc0NjVmOSJ9.lQKimlZHgX1cDHwyXe-tdIPt6hIAIXHNoYZGiqpBVQ0"

print("Sending request to /api/v1/dashboard/metrics...")
try:
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/dashboard/metrics", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    import traceback
    traceback.print_exc()
