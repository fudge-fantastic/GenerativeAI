from fastapi import FastAPI, Body, UploadFile, File
import os
import dotenv
from groq import Groq
import pdfplumber
import uvicorn
# Validation
import logging
logger = logging.getLogger(__name__)

dotenv.load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, resume-JD comparison app!"}

@app.post("/test")
async def compare_resume_jd(resume_file: UploadFile = File(...), jd_text: str = Body(...)):
    logging.basicConfig(filename='main.log', level=logging.INFO)
    logger.info("Started")
    try:
        # Read resume text from uploaded file (if provided)
        resume_text = ""
        if resume_file:
            with pdfplumber.open(resume_file.file) as pdf:
                for page in pdf.pages:
                    resume_text += page.extract_text() + "\n\n"
                logger.info(f"Extracted resume text: {resume_text}")
                
        prompt = f'''Can you compare this JD {jd_text}
                    with this Resume {resume_text}.
                    Can you please help me identify what am I missing, what can be improved, what should I learn more!
                    As if you're my Master'''

        client = Groq(api_key=api_key)  
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "assistant",
                    "content": ""
                }
            ],
            temperature=1.4,
            max_tokens=8192,
            top_p=1,
            stream=True,
            stop=None
        )

        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""

        return {"response": response_text}
    
    except Exception as e:
        print(f"Error processing resume: {e}")
        return {"error": "An error occurred while processing the resume."}

    logger.info("Finished")
    

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000)
