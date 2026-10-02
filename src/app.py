import os
import shutil
import tempfile
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from src.vector_store import VectorStore, get_global_model_and_tokenizer
from src.chatbot import LegalDocumentAssistant
from src.session_manager import SessionManager
from src.document_processor import DocumentProcessor

# Define request and response models
class Query(BaseModel):
    text: str
    session_id: Optional[str] = None

class Document(BaseModel):
    page_content: str
    metadata: Dict[str, Any]

class ChatResponse(BaseModel):
    response: str
    session_id: str
    source_documents: Optional[List[Document]] = None

class SessionInfoResponse(BaseModel):
    session_id: str
    created_at: str
    last_active: str

class UploadDocumentResponse(BaseModel):
    status: str
    filename: str
    chunks: int
    indexed: bool
    message: str

# Global variables
vectorstore = None
session_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize on startup
    global vectorstore, session_manager
    try:
        # Pre-load the transformer model globally before any requests are processed
        # This will initialize the model once for all future instances
        print("Pre-loading global transformer model...")
        get_global_model_and_tokenizer()
        print("Global transformer model loaded successfully")
        
        # Initialize vector store
        vector_store = VectorStore()
        vectorstore = vector_store.load_index()
        
        # Initialize session manager with 30 minute timeout
        session_manager = SessionManager(timeout_minutes=30)
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
    yield
    # Clean up on shutdown if needed

app = FastAPI(title="Legal Document Assistant API", lifespan=lifespan)

def get_vectorstore():
    """Dependency to get the vector store."""
    if vectorstore is None:
        raise HTTPException(status_code=503, detail="Vector store service unavailable")
    return vectorstore

def get_session_manager():
    """Dependency to get the session manager."""
    if session_manager is None:
        raise HTTPException(status_code=503, detail="Session management service unavailable")
    return session_manager

def create_chatbot():
    """Factory function to create a new chatbot instance."""
    return LegalDocumentAssistant(get_vectorstore())

@app.get("/")
async def root():
    return {"message": "Legal Document Assistant API is running. Send POST requests to /chat endpoint."}

@app.post("/upload", response_model=UploadDocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF or TXT file and index it using the existing document-processing and Pinecone pipeline."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in {".pdf", ".txt"}:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or TXT file.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    temp_dir = tempfile.mkdtemp(prefix="lexintel_upload_")
    temp_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_path, "wb") as output_file:
            output_file.write(file_bytes)

        processor = DocumentProcessor()
        loaded_documents = processor.load_documents(temp_dir)
        if not loaded_documents:
            raise HTTPException(status_code=400, detail="No readable content found in the uploaded file.")

        processed_documents = processor.process_documents(loaded_documents)
        if not processed_documents:
            raise HTTPException(status_code=500, detail="Document processing failed.")

        vector_store = VectorStore()
        upload_result = vector_store.upload_documents(processed_documents)
        if upload_result is None:
            raise HTTPException(status_code=500, detail="Document indexing failed.")

        return UploadDocumentResponse(
            status="success",
            filename=file.filename,
            chunks=len(processed_documents),
            indexed=True,
            message="Document processed successfully."
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Document upload failed: {str(exc)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.post("/chat", response_model=ChatResponse)
async def chat(
    query: Query,
    sm: SessionManager = Depends(get_session_manager)
):
    """Process a chat query using a specific or new session."""
    if not query.text.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty")
    
    try:
        # Get or create session
        session_id, bot = sm.get_or_create_session(create_chatbot, query.session_id)
        
        # Process the query
        response = bot.chat(query.text)
        
        # For future implementation: extract source documents if available
        # Currently the bot doesn't directly expose source documents in its response
        source_docs = None
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            source_documents=source_docs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.delete("/session/{session_id}")
async def end_session(
    session_id: str,
    sm: SessionManager = Depends(get_session_manager)
):
    """End a specific session."""
    if sm.end_session(session_id):
        return {"message": f"Session {session_id} has been terminated"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/sessions/count")
async def get_session_count(
    sm: SessionManager = Depends(get_session_manager)
):
    """Get the count of active sessions."""
    return {"active_sessions": sm.get_active_session_count()}

@app.post("/session/reset/{session_id}")
async def reset_session(
    session_id: str,
    sm: SessionManager = Depends(get_session_manager)
):
    """Reset the conversation state for a specific session."""
    session = sm.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Reset the conversation
    reset_message = session["chatbot"].reset_conversation()
    return {"message": reset_message, "session_id": session_id}

@app.get("/sources/{session_id}")
async def get_sources(
    session_id: str,
    sm: SessionManager = Depends(get_session_manager)
):
    """Get sources referenced in the current session."""
    session = sm.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get document references from the conversation state
    if hasattr(session["chatbot"], "conversation_state"):
        doc_refs = list(session["chatbot"].conversation_state.get("document_references", []))
        return {"document_references": doc_refs, "session_id": session_id}
    else:
        return {"document_references": [], "session_id": session_id}

# For local development and testing
if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))