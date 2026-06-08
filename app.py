from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["resume"]

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        pdf = PdfReader(filepath)

        text = ""

        # Extract text from PDF
        for page in pdf.pages:
            text += page.extract_text() or ""

        # Convert to lowercase for keyword matching
        resume_text = text.lower()

        keywords = [
            "python",
            "sql",
            "git",
            "dsa",
            "pandas",
            "numpy",
            "machine learning",
            "matplotlib",
            "power bi",
            "opencv"
        ]

        found_keywords = []

        for keyword in keywords:
            if keyword in resume_text:
                found_keywords.append(keyword)

        ats_score = int((len(found_keywords) / len(keywords)) * 100)

        return f"""
        <h2>ATS Score: {ats_score}%</h2>

        <h3>Matched Keywords</h3>

        <ul>
            {''.join(f'<li>{k}</li>' for k in found_keywords)}
        </ul>

        <h3>Extracted Resume Text</h3>

        <pre>{text}</pre>
        """

    return "No file selected"


if __name__ == "__main__":
    app.run(debug=True)