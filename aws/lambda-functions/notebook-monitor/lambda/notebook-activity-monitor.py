import boto3
import datetime
import pytz

CLIENT = boto3.client('sagemaker')

# Main function
def lambda_handler(event, context):
    timezone = pytz.timezone('Europe/Brussels')
    local_time = timezone.localize(datetime.datetime.now())
    local_time = local_time.astimezone(timezone).time()
    print(local_time)

    stop_time = datetime.time(hour=20)
    print(stop_time)
    if local_time >= stop_time:
        instances = CLIENT.list_notebook_instances(StatusEquals='InService')["NotebookInstances"]
        if len(instances) != 0:
            for instance in instances:
                CLIENT.stop_notebook_instance(NotebookInstanceName=instance["NotebookInstanceName"])
            print("Notebook instances have been stopped")
        else:
            print("No notebooks in service")

