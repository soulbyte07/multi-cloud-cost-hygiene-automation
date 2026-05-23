import boto3 
import json
import argparse


# Scan the AWS 
def scan_aws_resources():
    # Create a session using your AWS credentials
    session = boto3.Session(
        # TODO: Replace with Sops 
        aws_access_key_id="YOUR_ACCESS",
    )
    # Create a client for the AWS service to scan for Resources
    ec2_client = session.client('ec2')
    # Scan for EC2 instances
    response = ec2_client.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance['InstanceId'],
                'State': instance['State']['Name'],
                'LaunchTime': instance['LaunchTime']
            })

    # Scan for EBS volumes
    ebs_client = session.client('ec2')
    response = ebs_client.describe_volumes()
    volumes = []
    for volume in response['Volumes']:
        volumes.append({
            'VolumeId': volume['VolumeId'],
            'State': volume['State'],
            'CreateTime': volume['CreateTime']
        })


    # Scan for EIP
    eip_client = session.client('ec2')
    response = eip_client.describe_addresses()
    eips = []
    for address in response['Addresses']:
        eips.append({
            'PublicIp': address['PublicIp'],
            'AllocationId': address.get('AllocationId', 'N/A'),
            'AssociationId': address.get('AssociationId', 'N/A') })

    return {
        'instances': instances,
        'volumes': volumes,
        'eips': eips
    }


# Filter resources based on criteria state
def filter_resources_state(resources):
    filtered_instances = [instance for instance in resources['instances'] if instance['State'] == 'stopped' and tags.get('Environment') != 'Protection']
    filtered_volumes = [volume for volume in resources['volumes'] if volume['State'] == 'available' and tags.get('Environment') != 'Protection']
    filtered_eips = [eip for eip in resources['eips'] if eip['AssociationId'] == 'N/A' and tags.get('Environment') != 'Protection']

    return {
        'instances': filtered_instances,
        'volumes': filtered_volumes,
        'eips': filtered_eips
    }


# return report.json with the filtered resources 
def generate_filtered_report(filtered_resources):
    with open('report.json', 'w') as f:
        json.dump(filtered_resources, f, default=str, indent=4)


# Dry run 
def dry_run(filtered_resources):
    print("Dry Run: The following resources would be deleted:")
    generate_filtered_report(filter_resources_state(scan_aws_resources()))



# Delete the filtered Resources
def delete_resources(filtered_resources):
    # get report.json and delete the resources 
    with open('report.json', 'r') as f:
        # if file not found
        if f is None:
            print("report.json not found. Please run the script with `--dry-run` to generate the report first.")
            return

        # File found, load the resources to delete
        resources_to_delete = json.load(f)
        print("Deleting the following resources:")
        print(json.dumps(resources_to_delete, indent=4))
        # Delete 
        session = boto3.Session(
            aws_access_key_id="access_key",
        )
        ec2_client = session.client('ec2')
        for instance in resources_to_delete['instances']:
            ec2_client.terminate_instances(InstanceIds=[instance['InstanceId']])
        for volume in resources_to_delete['volumes']:
            ec2_client.delete_volume(VolumeId=volume['VolumeId'])
        for eip in resources_to_delete['eips']:
            ec2_client.release_address(AllocationId=eip['AllocationId'])

        print("Resources deleted successfully.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='AWS Resource Janitor')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run and generate report.json without deleting resources')
    parser.add_argument('--delete', action='store_true', help='Delete resources based on report.json')
    args = parser.parse_args()

    if args.dry_run:
        dry_run(filter_resources_state(scan_aws_resources()))
    elif args.delete:
        delete_resources(filter_resources_state(scan_aws_resources()))
    else:
        print("Please specify either --dry-run or --delete")


















