# Trigger Uvicorn reload to load new serviceAccountKey.json
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from datetime import datetime

# Initialize FastAPI
app = FastAPI(title="Note App API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase Admin
try:
    # Look for the service account key in the backend folder
    cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase Admin initialized successfully.")
    else:
        print(f"Warning: {cred_path} not found. Firebase features will fail.")
        db = None
except Exception as e:
    print(f"Warning: Firebase Admin initialization failed: {e}")
    db = None

# Pydantic models
class NoteCreate(BaseModel):
    content: str

class NoteUpdate(BaseModel):
    content: str

class NoteResponse(BaseModel):
    id: str
    user_id: str
    content: str
    created_at: str

# Dependency to verify Firebase Token
async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = authorization.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

# API Routes
@app.get("/")
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Note App Backend is running!"}

@app.get("/auth/me")
async def get_current_user(user: dict = Depends(verify_token)):
    return {"user_id": user.get("uid"), "email": user.get("email")}

@app.post("/notes")
async def create_note(note: NoteCreate, user: dict = Depends(verify_token)):
    if not db:
        raise HTTPException(status_code=500, detail="Database not configured. Missing serviceAccountKey.json")
    
    user_id = user.get("uid")
    doc_ref = db.collection("notes").document()
    
    new_note = {
        "id": doc_ref.id,
        "user_id": user_id,
        "content": note.content,
        "created_at": datetime.now().isoformat()
    }
    
    doc_ref.set(new_note)
    return new_note

@app.get("/notes")
async def get_notes(sort_order: str = "desc", user: dict = Depends(verify_token)):
    if not db:
        raise HTTPException(status_code=500, detail="Database not configured. Missing serviceAccountKey.json")
    
    user_id = user.get("uid")
    
    notes_ref = db.collection("notes").where("user_id", "==", user_id).stream()
    
    notes = []
    for doc in notes_ref:
        notes.append(doc.to_dict())
        
    # Sort in memory by created_at
    notes.sort(key=lambda x: x.get("created_at", ""), reverse=(sort_order == "desc"))
    
    return notes

@app.put("/notes/{note_id}")
async def update_note(note_id: str, note_update: NoteUpdate, user: dict = Depends(verify_token)):
    if not db:
        raise HTTPException(status_code=500, detail="Database not configured.")
    user_id = user.get("uid")
    doc_ref = db.collection("notes").document(note_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Note not found")
    if doc.to_dict().get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    doc_ref.update({"content": note_update.content, "updated_at": datetime.now().isoformat()})
    return {"status": "success", "message": "Note updated"}

@app.delete("/notes/{note_id}")
async def delete_note(note_id: str, user: dict = Depends(verify_token)):
    if not db:
        raise HTTPException(status_code=500, detail="Database not configured.")
    user_id = user.get("uid")
    doc_ref = db.collection("notes").document(note_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Note not found")
    if doc.to_dict().get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    doc_ref.delete()
    return {"status": "success", "message": "Note deleted"}
