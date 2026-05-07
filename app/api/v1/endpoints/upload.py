from fastapi import APIRouter, UploadFile, File, Form
from app.rag.embeddings import get_embedding
from app.rag.vector_store import vector_store
from app.core.logger import logger

import PyPDF2
import docx
import uuid


router = APIRouter()


# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    return text.strip()


# -----------------------------
# DOCX TEXT EXTRACTION
# -----------------------------
def extract_text_from_docx(file):
    document = docx.Document(file)
    text = ""

    for para in document.paragraphs:
        if para.text:
            text += para.text + "\n"

    return text.strip()


# -----------------------------
# TEXT CHUNKING
# -----------------------------
def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)

    return chunks


# -----------------------------
# UPLOAD ENDPOINT
# -----------------------------
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    session_id: str = Form(...)
):
    try:
        logger.info(f"[UPLOAD] File: {file.filename}, Session: {session_id}")

        # -----------------------------
        # STEP 1: GENERATE DOCUMENT ID
        # -----------------------------
        document_id = str(uuid.uuid4())

        # -----------------------------
        # STEP 2: EXTRACT TEXT
        # -----------------------------
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file.file)

        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(file.file)

        else:
            content = await file.read()
            text = content.decode("utf-8")

        if not text.strip():
            return {
                "error": "No text could be extracted from file"
            }

        # -----------------------------
        # STEP 3: CHUNK TEXT
        # -----------------------------
        chunks = chunk_text(text)

        logger.info(f"[UPLOAD] Chunks created: {len(chunks)}")

        # -----------------------------
        # STEP 4: CREATE EMBEDDINGS
        # -----------------------------
        embeddings = [get_embedding(chunk) for chunk in chunks]

        # -----------------------------
        # STEP 5: STORE IN VECTOR DB
        # -----------------------------
        vector_store.add(
            embeddings,
            chunks,
            session_id,
            document_id
        )

        logger.info(f"[UPLOAD] Stored successfully | Doc ID: {document_id}")

        # -----------------------------
        # RESPONSE
        # -----------------------------
        return {
            "message": "File uploaded successfully",
            "session_id": session_id,
            "document_id": document_id,
            "chunks": len(chunks)
        }

    except Exception as e:
        logger.error(f"[UPLOAD ERROR]: {str(e)}")

        return {
            "error": "File processing failed",
            "details": str(e)
        }