import argparse
import json
import re
from datetime import datetime, timezone
import boto3


def _tags_to_dict(tags_list):
    if not tags_list:
        return {}
    return {tag.get("Key"): tag.get("Value") for tag in tags_list}


def _is_protected(tags):
    return tags.get("Protected", "false").lower() == "true"


def _parse_stop_time(reason):
    if not reason:
        return None
    match = re.search(r"\(([^)]+)\)", reason)
    if not match:
        return None
    value = match.group(1).replace(" GMT", "")
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# Scan the AWS
def scan_aws_resources():
    session = boto3.Session()
    ec2_client = session.client("ec2")
    # Scan for EC2 instances
    response = ec2_client.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            tags = _tags_to_dict(instance.get("Tags", []))
            instances.append({
                "InstanceId": instance["InstanceId"],
                "State": instance["State"]["Name"],
                "LaunchTime": instance["LaunchTime"],
                "StateTransitionReason": instance.get("StateTransitionReason"),
                "Tags": tags,
            })

    # Scan for EBS volumes
    response = ec2_client.describe_volumes()
    volumes = []
    for volume in response['Volumes']:
        tags = _tags_to_dict(volume.get("Tags", []))
        volumes.append({
            "VolumeId": volume["VolumeId"],
            "State": volume["State"],
            "CreateTime": volume["CreateTime"],
            "Tags": tags,
        })


    # Scan for EIP
    response = ec2_client.describe_addresses()
    eips = []
    for address in response['Addresses']:
        tags = _tags_to_dict(address.get("Tags", []))
        eips.append({
            "PublicIp": address["PublicIp"],
            "AllocationId": address.get("AllocationId", "N/A"),
            "AssociationId": address.get("AssociationId", "N/A"),
            "Tags": tags,
        })

    return {
        'instances': instances,
        'volumes': volumes,
        'eips': eips
    }


def _is_stopped_long_enough(instance, days):
    stop_time = _parse_stop_time(instance.get("StateTransitionReason"))
    if stop_time is None:
        stop_time = instance.get("LaunchTime")
        if stop_time is None:
            return False
    age_days = (datetime.now(timezone.utc) - stop_time).days
    return age_days >= days


# Filter resources based on criteria state
def filter_resources_state(resources, days):
    filtered_instances = [
        instance
        for instance in resources["instances"]
        if instance["State"] == "stopped"
        and _is_stopped_long_enough(instance, days)
        and not _is_protected(instance.get("Tags", {}))
    ]
    filtered_volumes = [
        volume
        for volume in resources["volumes"]
        if volume["State"] == "available"
        and not _is_protected(volume.get("Tags", {}))
    ]
    filtered_eips = [
        eip
        for eip in resources["eips"]
        if eip["AssociationId"] == "N/A"
        and not _is_protected(eip.get("Tags", {}))
    ]

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
    generate_filtered_report(filtered_resources)



# Delete the filtered Resources
def delete_resources():
    try:
        with open("report.json", "r") as f:
            resources_to_delete = json.load(f)
    except FileNotFoundError:
        print("report.json not found. Please run the script with `--dry-run` to generate the report first.")
        return

    print("Deleting the following resources:")
    print(json.dumps(resources_to_delete, indent=4))

    session = boto3.Session()
    ec2_client = session.client("ec2")
    for instance in resources_to_delete.get("instances", []):
        if _is_protected(instance.get("Tags", {})):
            continue
        ec2_client.terminate_instances(InstanceIds=[instance["InstanceId"]])
    for volume in resources_to_delete.get("volumes", []):
        if _is_protected(volume.get("Tags", {})):
            continue
        ec2_client.delete_volume(VolumeId=volume["VolumeId"])
    for eip in resources_to_delete.get("eips", []):
        if _is_protected(eip.get("Tags", {})):
            continue
        if eip.get("AllocationId") and eip["AllocationId"] != "N/A":
            ec2_client.release_address(AllocationId=eip["AllocationId"])

    print("Resources deleted successfully.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='AWS Resource Janitor')
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run and generate report.json without deleting resources")
    parser.add_argument("--delete", action="store_true", help="Delete resources based on report.json")
    parser.add_argument("--days", type=int, default=14, help="Days threshold for stopped instances")
    args = parser.parse_args()

    resources = scan_aws_resources()
    filtered = filter_resources_state(resources, args.days)

    if args.delete:
        generate_filtered_report(filtered)
        delete_resources()
    else:
        dry_run(filtered)

















