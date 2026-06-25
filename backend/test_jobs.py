import os
import sys
from dotenv import load_dotenv

load_dotenv(".env")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, ProcessingJob, Document

db_url = os.getenv("DATABASE_URL")
print(f"Connecting to: {db_url.split('@')[-1]}")

try:
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    print("Querying jobs joined with documents...")
    results = db.query(
        ProcessingJob.id,
        ProcessingJob.document_id,
        ProcessingJob.status,
        ProcessingJob.started_at,
        ProcessingJob.completed_at,
        ProcessingJob.error_message,
        ProcessingJob.created_at,
        Document.file_name
    ).join(Document, ProcessingJob.document_id == Document.id).all()
    
    print(f"Jobs count: {len(results)}")
    for r in results:
        print(f" - Job ID: {r.id}, Document: {r.file_name}, Status: {r.status}")
        
    db.close()
    print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
