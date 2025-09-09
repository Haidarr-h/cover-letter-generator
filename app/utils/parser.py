import PyPDF2
from fastapi import UploadFile
import re

async def exctract_text_from_pdf(file: UploadFile) -> str:
    reader = PyPDF2.PdfReader(file.file)
    
    # extract text with page breaks
    raw_text = "\n\n --- PAGE BREAKS --- \n\n".join[
        [page.extract_text() or "" for page in reader.pages]
    ]
    
    # clean up spacing
    cleaned_text = re.sub(r'[ \t]', ' ', raw_text)
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)
    
    return cleaned_text.strip()