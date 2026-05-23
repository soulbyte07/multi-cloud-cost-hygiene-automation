import boto3 


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
    filtered_instances = [instance for instance in resources['instances'] if instance['State'] == 'stopped']
    filtered_volumes = [volume for volume in resources['volumes'] if volume['State'] == 'available']
    filtered_eips = [eip for eip in resources['eips'] if eip['AssociationId'] == 'N/A']

    return {
        'instances': filtered_instances,
        'volumes': filtered_volumes,
        'eips': filtered_eips
    }





















