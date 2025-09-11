from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

async def generate_prompt(cv_text:str, job_description:str, formality:str):
    prompt = f"""
    You are an AI specialized in writing personalized cover letters. Generate a formal cover letter in plain text, following the instructions below.

    Job Description:
    {job_description}

    My CV (all pasted together, you should identify the sections, including name, email, phone number, and address if available):
    {cv_text}

    Instructions:
    - Extract my full name, email, phone number, and address from the CV, and use them in the header of the cover letter.
    - Tailor each paragraph to show why I am a perfect fit for this role.
    - Use specific examples from my CV that match the requirements in the job description.
    - Keep the language professional but engaging.
    - Avoid generic statements like "I am a hard worker."
    - Conclude with enthusiasm and a call to action for an interview.
    - Output the cover letter in plain text, ready to use.
    """
    
    return prompt

async def generate_cover_letter(cv_text:str, job_description:str, formality:str):
    prompt = await generate_prompt(cv_text, job_description, formality)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    
    # return prompt
    return response.text
