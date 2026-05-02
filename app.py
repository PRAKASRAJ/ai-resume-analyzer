from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    skills = ["python", "java", "sql", "machine learning"]
    found = [s for s in skills if s in text.lower()]

    return render_template("result.html", skills=found)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)