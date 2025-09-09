
async def generate_cover_letter(cv_text:str, job_description:str, formality:str) -> str:
    prompt = f"""
    write a {formality} cover letter for this job:
    
    Job Description:
    {job_description}
    
    with my cv:
    {cv_text}
    """
    
    # TODO : call gemini API and send this prompt
    
    return prompt