# This file is used to convert PDFs to Images

from pdf2image import convert_from_path
import os

pdf_folder = r"D:\CODING\Test\Python\pdfs"
poppler_path = r"D:\CODING\Test\Python\poppler-24.02.0\Library\bin"
save_files = r"D:\CODING\Test\Python\Images"
pdf_files = [file for file in os.listdir(pdf_folder) if file.endswith(".pdf")]

for pdf_file in pdf_files:
    # Path to the PDF files
    pdf_path = os.path.join(pdf_folder, pdf_file)

    # Converting each PDF to a list of images
    pages = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path)

    # Iterate over each page image
    for i, page in enumerate(pages):
        img_name = f"{pdf_file}_Page_{i+1}.jpeg"
        page.save(os.path.join(save_files, img_name), "JPEG")