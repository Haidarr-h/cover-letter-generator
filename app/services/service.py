from dotenv import load_dotenv
from google import genai
from datetime import date

load_dotenv()

client = genai.Client()

async def generate_prompt(cv_text:str, job_description:str, formality:str, company_name_address:str=None, additional_request:str=None):
    today_date = date.today()
    today_formatted = today_date.strftime("%d %B %Y")
    prompt = f"""
    You are an AI specialized in writing personalized cover letters. Generate a formal cover letter in plain text, following the instructions below.

    Job Description:
    {job_description}

    My CV (all pasted together, you should identify the sections, including name, email, phone number, and address if available):
    {cv_text}

    Instructions:
    - Extract my full name, email, and phone number, from the CV, and use them in the header of the cover letter. Make sure each section is in a separate line.
    - Tailor each paragraph to show why I am a perfect fit for this role.
    - Use specific examples from my CV that match the requirements in the job description.
    - Keep the language professional but engaging.
    - Avoid generic statements like "I am a hard worker."
    - Conclude with enthusiasm and a call to action for an interview.
    - Output the cover letter in plain text, ready to use.
    
    Todays date is:
    {today_formatted}
    
    Heres the company name and address if any:
    {company_name_address}
    
    Heres an Additional Request if any:
    {additional_request}
    """
    
    return prompt

async def generate_cover_letter(cv_text:str, job_description:str, formality:str, company_name_address:str=None, additional_request:str=None):
    prompt = await generate_prompt(cv_text, job_description, formality, company_name_address, additional_request)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    
    # return prompt
    return response.text
