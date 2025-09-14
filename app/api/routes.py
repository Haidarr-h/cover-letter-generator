# app/api/routes.py

from fastapi import APIRouter, UploadFile, Form, status, HTTPException
from fastapi.responses import JSONResponse
from app.utils.parser import exctract_text_from_pdf
from app.services.service import generate_cover_letter
from typing import Optional
from app.utils.cv_validator import validate_file_cv
from fastapi.responses import StreamingResponse
from app.utils.file_generator import generate_doc, generate_pdf
from app.schemas.download_request import DownloadRequest
from google.genai import errors
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok"}

@router.post("/generate")
async def generate(
    file_cv: UploadFile,
    job_description: str = Form(...),
    tone: str = Form("formal"),
    company_name_address: Optional[str] = Form(None),
    additional_request: Optional[str] = Form(None),
):
    try:
        # validation of the file
        file_cv_validated = await validate_file_cv(file_cv)
        
        # extracting the text
        cv_text = await exctract_text_from_pdf(file_cv_validated)
        
        # generating cover letter with gemini
        letter = await generate_cover_letter(cv_text, job_description, tone, company_name_address, additional_request)
        
        return {
            "status": "success",
            "Cover Letter": letter
        }
        
    except errors.ServerError as e:
        logger.error(f"ServerError: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "error", "error_type": "server_unavailable", "message": "AI service is overloaded, please retry later."}
        )

    except Exception as e:
        logger.error(f"ServerError: {e}")
        # Unknown/unexpected issue
        return JSONResponse(
            status_code=500,
            content={"status": "error", "error_type": "internal_error", "message": "Something went wrong. Please try again later."}
        )
    

@router.post("/download")
async def download(request: DownloadRequest):
    if request.type == "pdf":
        file_buffer = generate_pdf(request.generated_letter)
        file_name = "cover_letter.pdf"
        media_type = "application/pdf"
    elif request.type == "word":
        file_buffer = generate_doc(request.generated_letter)
        file_name = "cover_letter.docx"
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        return JSONResponse(
            {
                "status": "Fail",
                "message": "Invalid type, must be pdf or word"
            },
            status_code=400
        )
    
    return StreamingResponse(
        file_buffer,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )