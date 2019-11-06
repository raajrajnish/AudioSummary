# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:35:36 2019

@author: Ritesh.Tiwary
"""

from typing import List
from azure.storage.blob import BlockBlobService, PublicAccess
import logging
import sys
import requests
import time
import swagger_client as cris_client
import json
import config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")

SUBSCRIPTION_KEY = config.SUBSCRIPTION_KEY
SERVICE_REGION = config.SERVICE_REGION

NAME = config.NAME
DESCRIPTION = config.DESCRIPTION

LOCALE = config.LOCALE
#RECORDINGS_BLOB_URI = "https://momsa.blob.core.windows.net/mom/momaudio/AlltoPittsburg_M.wav"
RECORDINGS_BLOB_URI = config.RECORDINGS_BLOB_URI

def blob_upload(file_name, file_bytes_array):
    try:
        block_blob_service = BlockBlobService(account_name=config.account_name,
                                              account_key=config.account_key)
        block_blob_service.set_container_acl("mom", public_access=PublicAccess.Container)
        block_blob_service.create_blob_from_bytes("mom", "momaudio/" + file_name, file_bytes_array)
        return "Successfully Uploaded"
    except Exception as e:
        print(e)

def transcribe(fileName):
    logging.info("Starting transcription client...")    
    configuration = cris_client.Configuration()
    configuration.api_key['Ocp-Apim-Subscription-Key'] = SUBSCRIPTION_KEY
    configuration.host = "https://{}.cris.ai".format(SERVICE_REGION)    
    client = cris_client.ApiClient(configuration)    
    transcription_api = cris_client.CustomSpeechTranscriptionsApi(api_client=client)    
    transcriptions: List[cris_client.Transcription] = transcription_api.get_transcriptions()
    logging.info("Deleting all existing completed transcriptions.")
    for transcription in transcriptions:
        try:
            transcription_api.delete_transcription(transcription.id)
        except ValueError:
            # ignore swagger error on empty response message body: https://github.com/swagger-api/swagger-core/issues/2446
            pass

    print("Path is : ", RECORDINGS_BLOB_URI + fileName)
    transcription_definition = cris_client.TranscriptionDefinition(
        name=NAME, description=DESCRIPTION, locale=LOCALE, recordings_url=RECORDINGS_BLOB_URI + fileName
    )

    data, status, headers = transcription_api.create_transcription_with_http_info(transcription_definition)
    transcription_location: str = headers["location"]
    created_transcription: str = transcription_location.split('/')[-1]
    
    logging.info("Created new transcription with id {}".format(created_transcription))
    logging.info("Checking status.")

    completed = False
    while not completed:
        running, not_started = 0, 0
        transcriptions: List[cris_client.Transcription] = transcription_api.get_transcriptions()
        
        for transcription in transcriptions:
            if transcription.status in ("Failed", "Succeeded"):        
                if created_transcription != transcription.id:
                    continue

                completed = True

                if transcription.status == "Succeeded":
                    results_uri = transcription.results_urls["channel_0"]
                    results = requests.get(results_uri)

                    resultstr = results.content.decode("utf-8")
                    resultjson = json.loads(resultstr)
                    speechtext = resultjson["AudioFileResults"][0]["CombinedResults"][0]["Display"]
                    file1 = open("text_file/extracted_text_from_audio.txt", "w+")
                    file1.write(speechtext)
                    file1.close()


                    logging.info("Transcription succeeded. Results: ")
                    logging.info(results.content.decode("utf-8"))
                else:
                    logging.info("Transcription failed :{}.".format(transcription.status_message))
                    break
            elif transcription.status == "Running":
                running += 1
            elif transcription.status == "NotStarted":
                not_started += 1

        logging.info("Transcriptions status: "
                "completed (this transcription): {}, {} running, {} not started yet".format(
                    completed, running, not_started))

        # wait for 5 seconds
        time.sleep(5)
