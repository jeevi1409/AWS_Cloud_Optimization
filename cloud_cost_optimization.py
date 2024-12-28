import boto3
import pandas as pd

# Set up AWS session
aws_session = boto3.Session(
    aws_access_key_id="AKIAZ5TC5DKP76HV3E7Q",
    aws_secret_access_key=" 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",
    region_name="global"
)

ec2_client = aws_session.client('ec2')

# Function to find idle EC2 instances
def get_idle_instances(ec2_client):
    response = ec2_client.describe_instances()
    idle_instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == 'stopped':
                idle_instances.append(instance['InstanceId'])
    return idle_instances

# Function to find unattached EBS volumes
def get_unattached_volumes(ec2_client):
    response = ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    unattached_volumes = [volume['VolumeId'] for volume in response['Volumes']]
    return unattached_volumes

# Function to find unused Elastic IPs
def get_unused_elastic_ips(ec2_client):
    response = ec2_client.describe_addresses()
    unused_ips = [address['PublicIp'] for address in response['Addresses'] if 'InstanceId' not in address]
    return unused_ips

# Function to generate a report
def generate_report(idle_instances, unattached_volumes, unused_ips):
    data = {
        "Resource Type": ["EC2 Instances", "EBS Volumes", "Elastic IPs"],
        "Unused Resources": [len(idle_instances), len(unattached_volumes), len(unused_ips)],
        "Details": [', '.join(idle_instances), ', '.join(unattached_volumes), ', '.join(unused_ips)]
    }
    df = pd.DataFrame(data)
    df.to_csv("cloud_cost_optimization_report.csv", index=False)
    print("Report saved as cloud_cost_optimization_report.csv")

# Main script execution
idle_instances = get_idle_instances(ec2_client)
unattached_volumes = get_unattached_volumes(ec2_client)
unused_ips = get_unused_elastic_ips(ec2_client)

generate_report(idle_instances, unattached_volumes, unused_ips)
