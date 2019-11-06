from extract_summary import summary as s
from speech_to_text import transcribe, blob_upload
from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/start_analysis', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        f = request.files['file']
        print("File Name is : ", f.filename)
        blob_upload(f.filename, f.read())
        transcribe(f.filename)
        summary = s("text_file/extracted_text_from_audio.txt")
        return render_template("success.html", summary=summary,starttime=current_time)
