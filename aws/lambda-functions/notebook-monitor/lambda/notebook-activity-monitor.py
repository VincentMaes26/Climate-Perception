import boto3

CLIENT = boto3.client('sagemaker')

# Main function
def lambda_handler(event, context):
    if len(CLIENT.list_notebook_instances(StatusEquals='InService')["NotebookInstances"]) != 0:
        CLIENT.stop_notebook_instance(NotebookInstanceName='Twitter-sentiment-analysis')
        print("Notebook instance has been stopped")
    else:
        print("Notebook is not in service")
