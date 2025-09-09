from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

async def generate_prompt(cv_text:str, job_description:str, formality:str):
    prompt = f"""
    Using the job description and my CV, write a {formality} and highly personalized cover letter.
    
    Job Description:
    {job_description}

    My CV:
    {cv_text}

    Instructions:
    - Tailor each paragraph to show why I am a perfect fit for this role.
    - Use specific examples from my CV that match the requirements in the job description.
    - Keep the language professional but engaging.
    - Avoid generic statements like "I am a hard worker."
    - Conclude with enthusiasm and a call to action for an interview.
    """
    
    return prompt

async def generate_cover_letter(cv_text:str, job_description:str, formality:str):
    prompt = await generate_prompt(cv_text, job_description, formality)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    
    return response.text
