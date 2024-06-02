import json
import boto3

def sendEmail(subject, body):
    # Create a SNS client object
    sns_client = boto3.client('sns', region_name='us-east-1')

    # Send email
    try:
        response = sns_client.publish(
            TopicArn='PROVIDE_YOUR_SNS_TOPIC',
            Subject=subject,
            Message=body
        )

        print("Email Sent Successfully")

    except Exception as e:
        print(f"Error sending email: {e}")

    
def lambda_handler(event, context):

    # Variables
    instance_id = 'Provide the instance ID where the script file is present'

    # Create SSM client object
    ssm_client = boto3.client('ssm')

    try:
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={
                'commands': [
                    'sh /Path/to/script/file.sh'
                ]
            }
        )

        # Get command ID
        command_id = response['Command']['CommandId']

        # Wait for command execution to complete
        waiter = ssm_client.get_waiter('command_executed')
        waiter.config.max_attempts = 50
        waiter.wait(CommandId=command_id, InstanceId=instance_id)

        # Get command execution details
        command_output = ssm_client.get_command_invocation(CommandId=command_id, InstanceId=instance_id)

        # Send email notification
        subject = "Deployment is Successful"
        body = "Latest changes is been deployed successfully"
        sendEmail(subject=subject, body=body)

        # fetching command output
        json_output = {
            'StatusCode': 200,
            'body': command_output['StandardOutputContent']
        }

        print(json_output) 

    except Exception as e:

        # Send email notification
        subject = "Deployment is Failed"
        body = "Due to technical issues deployment is failed."
        sendEmail(subject=subject, body=body)

        print("Exception during deployment: ", e)
