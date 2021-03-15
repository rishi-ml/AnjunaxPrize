# anjunaxprize

Azure functions POC for the Anjuna Enclave for xPrize

Instructions:
Enclave:
Launch the Anjuna Enclave in the ACC Sandbox environment as follows:

SSH to the Sandbox

cd /home/anjuna

./run-server.sh


Execute the steps till the Anjuna Enclave is launched in the Flask API

Azure:
Deploy the Azure function contained here

Go to function settings and change the values for the connection strings for 

AzureWebJobsStorage: This is the connection string for the storage account that the Jupyter Lab environment is mounted on

AZURE_FILE_SHARE_NAME: The name of the specific file share pointing to the "work" directory

MODEL_PARENT_DIR: The sub directory under "work" where the notebook, model and output files are kept


