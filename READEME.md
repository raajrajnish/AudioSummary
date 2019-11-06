**Steps To Follow - This blog is inspired from below medium link**
URL - https://medium.com/jatana/unsupervised-text-summarization-using-sentence-embeddings-adb15ce83db1

***How to run model***
1. Download the pre trained model from here
    URL - https://github.com/ryankiros/skip-thoughts
    install all wget
    keep all files under model folder
2. pip install -r requirements.txt

3. Run Flask
    export FLASK_APP=service_start.py
    flask run

optional How to create requirements.txt file
pip freeze > requirements.txt