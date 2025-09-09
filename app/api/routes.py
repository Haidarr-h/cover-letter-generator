from fastapi import APIRouter, UploadFile, Form, status, HTTPException
from app.utils.parser import exctract_text_from_pdf
from app.services.service import generate_cover_letter

router = APIRouter()

# check file types
allowed_file_types = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
]
# check file size
max_file_size = 10 * 1024 * 1024

@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok"}

@router.post("/generate")
async def generate(
    file_cv: UploadFile,
    job_description: str = Form(...),
    tone: str = Form("formal")
):
    # validation of the file
    file_cv_validated = await validate_file_cv(file_cv)
    
    # extracting the text
    cv_text = await exctract_text_from_pdf(file_cv_validated)
    
    # generating cover letter with gemini
    letter = await generate_cover_letter(cv_text, job_description, tone)
    
    return {"Cover Letter": letter}

async def validate_file_cv(file_cv):
    """
    Checks if the file_cv is of an accepted type.
    The accepted types are PDF, Word, and Text.
    If the file type is not accepted, raises a 415 error.

    :param file_cv: The file containing the CV
    :type file_cv: UploadFile
    :raises HTTPException: 415 error if the file is not of an accepted type
    """
    
    # check file types
    if file_cv.content_type not in allowed_file_types:
        raise HTTPException(
            status_code=415,
            detail=f"File type '{file_cv.content_type}' is not allowed. Only PDF, Word, and Text"
        )
    
    # check file size
    content = await file_cv.read()
    if len(content) > max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. Yours is {content} while max is {max_file_size}"
        )
    
    file_cv.file.seek(0)
    return file_cv