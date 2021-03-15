import logging
import requests
import os
import json

from azure.storage.fileshare import ShareClient
import azure.functions as func

def main(req: func.HttpRequest, ACCOutputQueue: func.Out[func.QueueMessage], ACCOutputBlob: func.Out[func.InputStream]) -> str:


    # connect to file share and get files
    share_connection_string = os.environ["AzureWebJobsStorage"]
    share_name = os.environ["AZURE_FILE_SHARE_NAME"]
    model_parent_dir = os.environ["MODEL_PARENT_DIR"]

    share = ShareClient.from_connection_string(share_connection_string, share_name)
    #my_files = list(share.list_directories_and_files())
    model_file_name = req.get_json().get('model_file')
    model_file_client = share.get_file_client(model_parent_dir + "/" + model_file_name)
    #model_file = share.get_file_client(model_file_name)
    with open(model_file_name, "rb") as data:
        stream = model_file_client.download_file()
        #data.write(stream.readall())

    # code for reading the actual file content itself - delete this later
    #filecontent = req.files['file'].read()
    #filename = req.files['file'].filename
    #ACCOutputQueue.set(filename)
    #ACCOutputBlob.set(filecontent)
    #files = {"file": filecontent}
     
         
    session = requests.Session()
    url = os.environ["INFERENCE_ENDPOINT"]
    headers = {"accept" : "application/json"}
    payload = {"compkey" : "c1", "userkey" : "Anjuna"}
    files = {"file": open(model_file_name, "rb")}
    modelresponse = requests.request("POST", url, data=payload, headers=headers, files=files)

    # Write JSON output
    model_file_out_name = model_parent_dir + "/" + model_file_name + ".out.json"
    model_file_out_client = share.get_file_client(model_file_out_name)
    model_file_out_client.upload_file(modelresponse.text)
    
    return func.HttpResponse(modelresponse.text)
    

    
