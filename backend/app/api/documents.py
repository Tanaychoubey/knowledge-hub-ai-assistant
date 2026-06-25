import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.api.deps import get_current_user, get_current_active_admin
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.worker.tasks import process_document_task
from app.services.rag import delete_document_vectors

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    # 1. Validate file extension
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "txt"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Only PDF and TXT are supported."
        )
    
    # 2. Setup storage directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    doc_id = uuid.uuid4()
    unique_filename = f"{doc_id}.{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # 3. Read and stream copy file to local disk, computing file size
    file_size = 0
    try:
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                file_size += len(chunk)
                if file_size > 20 * 1024 * 1024:  # 20MB limit
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File size exceeds maximum limit of 20MB."
                    )
                buffer.write(chunk)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # 4. Save metadata record to DB
    doc_record = Document(
        id=doc_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file_ext.upper(),
        file_size=file_size,
        status="UPLOADED",
        uploaded_by=current_user.id
    )
    
    db.add(doc_record)
    db.commit()
    db.refresh(doc_record)
    
    # 5. Delegate processing queue task
    process_document_task.delay(str(doc_record.id))
    
    return doc_record

@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Document).order_by(Document.created_at.desc()).all()

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    doc_record = db.query(Document).filter(Document.id == document_id).first()
    if not doc_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found."
        )
        
    # Remove local PDF/TXT file
    if os.path.exists(doc_record.file_path):
        try:
            os.remove(doc_record.file_path)
        except Exception as e:
            print(f"Failed to remove file from disk: {e}")
            
    # Clean up vectors from Qdrant database
    try:
        delete_document_vectors(doc_record.id)
    except Exception as e:
        print(f"Failed to delete Qdrant vectors: {e}")
        
    # Remove database record
    db.delete(doc_record)
    db.commit()
    return None
