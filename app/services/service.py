import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

async def generate_cover_letter(cv_text:str, job_description:str, formality:str) -> str:
    prompt = f"""
    write a {formality} cover letter for this job:
    
    Job Description:
    {job_description}
    
    with my cv:
    {cv_text}
    """
    
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
    }
    
    url_with_key = f"{GEMINI_API_URL}?key={API_KEY}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url_with_key, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    return prompt