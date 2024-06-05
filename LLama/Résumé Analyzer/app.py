import os
import dotenv
import pdfplumber
import docx
import re
from flask import Flask, request, render_template, jsonify, send_file
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
        temperature=1.5,
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
    full_text = [para.text.strip() for para in doc.paragraphs]
    return '\n\n'.join(full_text)

def clean_text(text):
    # Remove extra newlines and leading/trailing whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    return text

ERROR_MESSAGE = 'An unexpected error occurred. Please try again later.'
INPUT_ERROR = 'Please provide both a Resume and a Job Description.'

@app.route('/')
def index():
    return render_template('index.html')

DOCX_EXTENSION = '.docx'

@app.route('/compare', methods=['POST'])
def compare():
    try:
        resume_file = request.files['resume']
        job_description = request.form.get('job_description')

        if not resume_file or not job_description:
            raise ValueError('Please provide both a Resume and a Job Description.')

        if resume_file.filename.endswith('.pdf'):
            with pdfplumber.open(resume_file) as pdf:
                all_text = "\n\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            all_text = clean_text(all_text)
        elif resume_file.filename.endswith(DOCX_EXTENSION):
            all_text = extract_text_from_docx(resume_file)
            all_text = clean_text(all_text)
        else:
            raise ValueError(f'Unsupported file format. Please upload a PDF or {DOCX_EXTENSION} file.')

        # Step to structure the document
        structured_text = get_llama_assistance(f'''I need your help to organize and structure the Resume text, even personal information:
                                                {all_text}''')

        main_role = '''[You're a professional consultant helping people land their dream job, by analyzing the job description and their resume details. YOU DO NOT HAVE TO MENTION YOUR ROLE TO THE USER, start direct to the point.
        You'll identify discrepancies, recommend areas for improvement, align candidate qualifications with company expectations, and outline areas of development. 
        This involves discerning the candidate's strengths and weaknesses, assessing their compatibility with the company's needs, and proposing actionable steps for improvement. 
        However, if the job description (JD) is entirely unrelated to the resume, strictly recommend them to prioritize focusing on the relevant areas instead of the unrelated ones.
        Note this: If you find both the Resume/Job-Description data is irrelevant, be bold and answer them about its irrelevance, be wild with the responses. One more thing, feel free to write as lengthy as you can]'''

        comparison = get_llama_assistance(f'''{main_role}
        Here's the Job Description: [{job_description}] 
        And here's the Resume Details: [{structured_text}]''')

        return jsonify({'comparison': comparison})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': ERROR_MESSAGE}), 500

@app.route('/review', methods=['POST'])
def review():
    try:
        resume_file = request.files['resume']

        if not resume_file:
            raise ValueError('Please upload a resume to review.')

        if resume_file.filename.endswith('.pdf'):
            with pdfplumber.open(resume_file) as pdf:
                all_text = "\n\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            all_text = clean_text(all_text)
        elif resume_file.filename.endswith(DOCX_EXTENSION):
            all_text = extract_text_from_docx(resume_file)
            all_text = clean_text(all_text)
        else:
            raise ValueError(f'Unsupported file format. Please upload a PDF or {DOCX_EXTENSION} file.')

        review_prompt = f'''Please review the following resume text and provide a detailed analysis. Start with scoring, highlight strengths, weaknesses, and areas for improvement:
                            {all_text}'''

        review = get_llama_assistance(review_prompt)

        return jsonify({'review': review})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': ERROR_MESSAGE}), 500

@app.route('/ask_question', methods=['POST'])
def ask_question():
    try:
        review_text = request.form.get('review_text')
        user_question = request.form.get('user_question')

        if not review_text or not user_question:
            raise ValueError('Both review text and user question are required.')

        prompt = f'''Based on the following review (given solely by you), answer the user's question in detail.
        It can be any question, so be friendly and open :) Don't mention your role (Answer in normmal text, don't use markdown language, and remember the flow of conversation, it must not look like we're starting a new conversation, but a continuation of the review/content).
        [Your Content Review:
        {review_text}]

        [User Question:
        {user_question}]

        Response:'''
        
        response = get_llama_assistance(prompt)

        return jsonify({'response': response})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': ERROR_MESSAGE}), 500

@app.route('/view_resume', methods=['POST'])
def view_resume():
    try:
        resume_file = request.files['resume']

        if resume_file.filename.endswith('.pdf'):
            with pdfplumber.open(resume_file) as pdf:
                all_text = "\n\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            all_text = clean_text(all_text)
            structured_text = get_llama_assistance(f'''I need your help to organize and structure the Resume text, don't mention your role or what task you did:
                                                        {all_text}''')
        elif resume_file.filename.endswith(DOCX_EXTENSION):
            all_text = extract_text_from_docx(resume_file)
            all_text = clean_text(all_text)
            structured_text = get_llama_assistance(f'''I need your help to organize and structure the Resume text, don't mention your role or what task you did:
                                                        {all_text}''')
        else:
            raise ValueError('Unsupported file format. Please upload a PDF or DOCX file.')

        FILENAME = "structured_resume.txt"
        with open(FILENAME, 'w') as f:
            f.write(structured_text)

        return send_file(FILENAME, as_attachment=True)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': ERROR_MESSAGE}), 500

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port= 8000, debug=True)
