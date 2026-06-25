import os
import sys
from dotenv import load_dotenv

# Load env from backend/.env
load_dotenv(".env")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.models import Base, Document, Conversation, RetrievalLog

db_url = os.getenv("DATABASE_URL")
print(f"Connecting to: {db_url.split('@')[-1]}")

try:
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    print("1. Querying documents count...")
    total_docs = db.query(Document).count()
    print(f"   Docs count: {total_docs}")
    
    print("2. Querying sum of chunks...")
    total_chunks = db.query(func.sum(Document.chunk_count)).scalar()
    print(f"   Sum of chunks (raw): {total_chunks}")
    total_chunks_val = int(total_chunks or 0)
    print(f"   Sum of chunks (int): {total_chunks_val}")
    
    print("3. Querying conversations count...")
    total_convs = db.query(Conversation).count()
    print(f"   Convs count: {total_convs}")
    
    print("4. Querying average latency...")
    avg_latency = db.query(func.avg(RetrievalLog.retrieval_latency_ms)).scalar()
    print(f"   Avg latency (raw): {avg_latency}")
    avg_latency_val = int(avg_latency or 0)
    print(f"   Avg latency (int): {avg_latency_val}")
    
    print("\nAll queries succeeded!")
    db.close()
    
except Exception as e:
    import traceback
    print("\nError occurred:")
    traceback.print_exc()
