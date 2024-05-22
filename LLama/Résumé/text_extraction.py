import os
from pdf2image import convert_from_path
from pytesseract import image_to_string

cwd = os.getcwd()
path1 = os.path.dirname(cwd)
poppler_path = os.path.join(path1, 'Gemini', 'poppler-24.02.0', 'Library', 'bin')
print(poppler_path)

def convert_pdf2img(pdf_file):
    return convert_from_path(pdf_file, poppler_path=poppler_path)

def convert_img2txt(file):
    txt = image_to_string(file)
    return txt

# Extracts text from PDF using Tesseract
def get_txt_from_pdf(pdf_file):
    images = convert_pdf2img(pdf_file)
    final_txt = ""
    for pg, img in enumerate(images):
        final_txt += image_to_string(img)
    return final_txt