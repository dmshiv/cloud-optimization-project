import boto3

# Connect to AWS EC2 in Frankfurt region
ec2 = boto3.client('ec2', region_name='eu-central-1')


def find_unattached_volumes():
    """Find EBS volumes that exist but are NOT attached to any EC2 instance.
    These are wasting money — you're paying for storage no one is using.
    """

    # 'available' status = volume exists but has no EC2 attached to it
    response = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    volumes = response['Volumes']

    if not volumes:
        print("  No unattached volumes found. Nothing to worry about!")
        return []

    print(f"  Found {len(volumes)} unattached volume(s) wasting money:")
    for v in volumes:
        cost = v['Size'] * 0.10  # gp2 costs ~$0.10 per GB per month
        print(f"    - {v['VolumeId']} | {v['Size']} GB | ~${cost:.2f}/month wasted")

    return [v['VolumeId'] for v in volumes]


# --- Run this file directly to scan for unattached volumes ---
if __name__ == '__main__':
    print("Scanning for unattached EBS volumes...")
    find_unattached_volumes()
