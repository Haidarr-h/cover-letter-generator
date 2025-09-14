from enum import Enum

class FileType(str, Enum):
  pdf = "pdf"
  word = "word"
  text = "text"