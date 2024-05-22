import os
import dotenv
import pdfplumber
import docx
import re
from flask import Flask, request, render_template, jsonify
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

def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text.strip())
    return '\n\n'.join(full_text)

def clean_text(text):
    # Remove extra newlines and leading/trailing whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text) 
    text = text.strip()  
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    try:
        resume_file = request.files['resume']
        job_description = request.form['job_description']

        if resume_file.filename.endswith('.pdf'):
            with pdfplumber.open(resume_file) as pdf:
                all_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n\n"
            all_text = clean_text(all_text)
        elif resume_file.filename.endswith('.docx'):
            all_text = extract_text_from_docx(resume_file)
            all_text = clean_text(all_text)
        else:
            raise ValueError('Unsupported file format. Please upload a PDF or DOCX file.')

        main_role = '''[You're a professional consultant helping people land their dream job, by analyzing the job description and their resume details.
        You'll highlight relevant skills and experiences, identify any missing qualifications, 
        and suggest areas for further exploration to strengthen their candidacy (suggest softwares or tools as well).
        Note this: If you find both the Resume/Job-Description data is irrelevant, be bold and answer them about its irrelevance. And be wild with the response, hehe. 
        And if the name's not mentioned, call him/her with something cool name. We want to provide comprehensive support to help people achieve their goals. 
        Please feel free to give as detailed and extensive response if needed]'''

        comparison = get_llama_assistance(f'''{main_role}
        Here's the Job Description: [{job_description}] 
        And here's the Resume Details: [{all_text}]''')

        return jsonify({'comparison': comparison})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
