import pandas as pd
from text_summarization import summarize


def summary(path):
    df = pd.read_csv(path)
    content = df.to_string()
    list_content = [content]
    summaries = summarize(list_content)
    print ('Summary is : ',summaries)
    return summaries


#summary('/home/ntl/Documents/summary/deep_summary/main_folder/skipthoughts/models/email_content.csv')

