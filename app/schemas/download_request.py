# app/schemas/download_request.py

from pydantic import BaseModel
from app.schemas.file_type import FileType

class DownloadRequest(BaseModel):
  generated_letter: str
  type: FileType = FileType.pdf