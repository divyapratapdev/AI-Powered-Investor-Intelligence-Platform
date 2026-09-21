import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from ingestion.ingest_documents import ingest_pdf

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()

    try:
        result = ingest_pdf(
            pdf_bytes=content,
            filename=file.filename,
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            api_key=os.getenv("AZURE_SEARCH_API_KEY"),
            index_name=os.getenv("AZURE_SEARCH_INDEX_NAME")
        )
        return JSONResponse(content={"message": "Ingestion complete", "details": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
