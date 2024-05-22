from flask import Flask, request, render_template, jsonify
import os
import dotenv
import pdfplumber
from groq import Groq

dotenv.load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

app = Flask(__name__)

def get_llama_assistance(prompt):
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": ""}
        ],
        temperature=1.4,
        max_tokens=8192,
        top_p=1,
        stream=True,
        stop=None,
    )

    response_text = ""

    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    return response_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    resume_file = request.files['resume']
    job_description = request.form['job_description']

    with pdfplumber.open(resume_file) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text() + "\n\n"
    
    main_role = '''[You're a career consultant helping a client land their dream job. By analyzing the job description and their resume, you become their strategic partner.
    You'll highlight relevant skills and experiences, identify any missing qualifications (like specific software or tools), 
    and suggest areas for further exploration to strengthen their candidacy.
    This allows them to tailor their resume for maximum impact and streamline their efforts by focusing on what truly matters for the position.]'''
    
    comparison = get_llama_assistance(f'''{main_role}
    This is the Job Description: {job_description} 
    And here's the Resume of the Client/User: {all_text}''')
    
    return jsonify({'comparison': comparison})

if __name__ == '__main__':
    app.run(debug=True)
