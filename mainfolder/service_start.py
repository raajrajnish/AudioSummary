from extract_summary import summary as s
from speech_to_text import transcribe, blob_upload
from flask import Flask, request, render_template
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/start_analysis', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        name = str(f)
        if '.mp3' in name:
            print("Starting the audio to text to summary process.")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            f = request.files['file']
            print("File Name is : ", f.filename)
            blob_upload(f.filename, f.read())
            transcribe(f.filename)
            summary = s("text_file/extracted_text_from_audio.txt")
            return render_template("success.html", summary=summary, starttime=current_time)

        elif '.txt' in name:
            os.makedirs(os.path.join(app.instance_path, 'uploaded_file'), exist_ok=True)
            filepath = 'text_file/'
            print("Starting text to summary process.")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            f = request.files['file']
            f.save(os.path.join(app.instance_path, 'uploaded_file', secure_filename(f.filename)))
            summary = s('instance/uploaded_file/'+f.filename)
            return render_template("success.html", summary=summary, starttime=current_time)

        else :
            return render_template('home.html')



