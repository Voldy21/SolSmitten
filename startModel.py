
import boto3


def start_model(project_arn, model_arn, version_name, min_inference_units):

    client = boto3.client('rekognition')

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response = client.start_project_version(
            ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
        print("response", response)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter(
            'project_version_running')
        print("a")
        project_version_running_waiter.wait(
            ProjectArn=project_arn, VersionNames=[version_name])
        print("b")

        # Get the running status
        describe_response = client.describe_project_versions(ProjectArn=project_arn,
                                                             VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage'])
    except Exception as e:
        print(e)

    print('Done...')


def main():
<<<<<<< HEAD
    project_arn='arn:aws:rekognition:us-east-1:671261739394:project/acneDetection/1618752126590'
    model_arn='arn:aws:rekognition:us-east-1:671261739394:project/acneDetection/version/acneDetection.2021-04-18T09.41.55/1618753315574'
    min_inference_units=1 
    version_name='acneDetection.2021-04-18T09.41.55'


    start_model(project_arn, model_arn, version_name, min_inference_units)


if __name__ == "__main__":
    main()
