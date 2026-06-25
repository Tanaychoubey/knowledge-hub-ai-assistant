import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Connecting to: {db_url.split('@')[-1]}") # hide password

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        # Check tables
        tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()
        print("Tables in public schema:")
        for t in tables:
            print(f" - {t[0]}")
            
        # Check users
        users = conn.execute(text("SELECT id, email, role, password_hash FROM users")).fetchall()
        print(f"\nUsers count: {len(users)}")
        for u in users:
            print(f" - ID: {u[0]}, Email: {u[1]}, Role: {u[2]}, Hash: {u[3]}")
            
except Exception as e:
    print(f"Error querying database: {e}")
