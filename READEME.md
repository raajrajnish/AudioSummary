**Steps To Follow**
Complete Theory - https://medium.com/jatana/unsupervised-text-summarization-using-sentence-embeddings-adb15ce83db1
1. Download the pre trained model from here

    URL - https://github.com/ryankiros/skip-thoughts
    install all wget
    keep all files under model folder
2. pip install -r requirements.txt

Before running make sure file architecture will be like

project structure

article_to_summary
    mainfolder
        audio - contains the audio file to upload
        models - contains the model downloaded form above link
        static - css related files
        templates - html files
        text_file - save text to this folder after converting to audio to text
        config.py - contains the configuration details
        email_summarization.py - logic to summary the text
        extract_summary.py - logic to extract summary
        requirements.txt - contains all required libraries
        service_start.py - main flask file register it and run
        skipthoughts.py - logic to use model
        speech_to_text.py - logic to convert audio to text
    README.md


3. Run Flask App and it will do analysis






# How to create requirements.txt file
pip freeze > requirements.txt