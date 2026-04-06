import boto3

# Connect to AWS EC2 in Frankfurt region
ec2 = boto3.client('ec2', region_name='eu-central-1')


def create_ec2():
    """Launch a t2.micro EC2 instance using the latest Amazon Linux 2 AMI."""

    # Find the latest Amazon Linux 2 image (the "OS" for our server)
    response = ec2.describe_images(
        Owners=['amazon'],
        Filters=[
            {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    ami_id = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)[0]['ImageId']
    print(f"  Using AMI: {ami_id}")

    # Launch the EC2 instance
    result = ec2.run_instances(
        ImageId=ami_id,
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'demo-instance'}]
        }]
    )
    instance_id = result['Instances'][0]['InstanceId']
    print(f"  EC2 created: {instance_id}")

    # Wait until it's fully running before moving on
    print("  Waiting for EC2 to reach RUNNING state...")
    ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
    print("  EC2 is now RUNNING")

    return instance_id


def get_root_volume(instance_id):
    """Get the EBS volume ID that is attached to the EC2 instance."""
    response = ec2.describe_instances(InstanceIds=[instance_id])
    volume_id = response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    print(f"  Root volume: {volume_id}")
    return volume_id


def delete_ec2(instance_id):
    """Terminate (permanently delete) an EC2 instance."""
    ec2.terminate_instances(InstanceIds=[instance_id])
    print(f"  Terminating EC2: {instance_id}")

    # Wait until fully gone
    print("  Waiting for EC2 to reach TERMINATED state...")
    ec2.get_waiter('instance_terminated').wait(InstanceIds=[instance_id])
    print("  EC2 is now TERMINATED")


# --- Run this file directly to test EC2 create/delete on its own ---
if __name__ == '__main__':
    print("Testing EC2 operations...")
    iid = create_ec2()
    vol = get_root_volume(iid)
    input("\nPress Enter to terminate the instance...")
    delete_ec2(iid)
