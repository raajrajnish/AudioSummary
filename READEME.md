**Steps To Follow - This blog is inspired from below medium link**
URL - https://medium.com/jatana/unsupervised-text-summarization-using-sentence-embeddings-adb15ce83db1

***How to run model***
1. Download the pre trained model from here
    URL - https://github.com/ryankiros/skip-thoughts
    install all wget
    keep all files under model folder
2. pip install -r requirements.txt

# Before running make sure file architecture will be like

1.audio_to_text_to_summary
    2.mainfolder
        3.audio - contains the audio file to upload
        4.models - contains the model downloaded form above link
        5.static - css related files
        6.templates - html files
        7.text_file - save text to this folder after converting to audio to text
        8.config.py - contains the configuration details
        9.email_summarization.py - logic to summary the text
        10.extract_summary.py - logic to extract summary
        11.requirements.txt - contains all required libraries
        12.service_start.py - main flask file register it and run
        13.skipthoughts.py - logic to use model
        14.speech_to_text.py - logic to convert audio to text
    README.md


3. Run Flask
    export FLASK_APP=service_start.py
    flask run

optional How to create requirements.txt file
pip freeze > requirements.txt