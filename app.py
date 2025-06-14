from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_bytes
import pytesseract
from docx import Document
import tempfile
import os

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # за Render

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdf']
    if file.filename == '':
        return 'Не е избран файл', 400

    images = convert_from_bytes(file.read())
    doc = Document()

    for img in images:
        text = pytesseract.image_to_string(img, lang='bul')
        doc.add_paragraph(text)
        doc.add_page_break()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
    doc.save(temp_file.name)
    return send_file(temp_file.name, as_attachment=True, download_name='converted.docx')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)