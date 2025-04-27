from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
from llmbp import llm_bp 
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

app.register_blueprint(llm_bp)


@app.route("/upload", methods=["POST"])
def upload_resume():
    resume = request.files.get("resume")
    prompt = request.form.get("prompt")

    if resume:
        # ✅ Save to parent directory's 'Resumes' folder
        parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        resumes_path = os.path.join(parent_path, "Resumes")
        os.makedirs(resumes_path, exist_ok=True)  # ensures folder exists
        save_path = os.path.join(resumes_path, resume.filename)

        resume.save(save_path)

        return jsonify({
            "message": "Resume received",
            "filename": resume.filename,
            "prompt": prompt
        })
    else:
        return jsonify({"error": "No resume uploaded"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)