import boto3

# Connect to AWS EC2 in Frankfurt region
ec2 = boto3.client('ec2', region_name='eu-central-1')


def create_snapshot(volume_id, name="demo-snapshot"):
    """Take a snapshot (backup copy) of an EBS volume and save it to S3."""

    response = ec2.create_snapshot(
        VolumeId=volume_id,
        Description=name,
        TagSpecifications=[{
            'ResourceType': 'snapshot',
            'Tags': [{'Key': 'Name', 'Value': name}]
        }]
    )
    snapshot_id = response['SnapshotId']
    print(f"  Snapshot started: {snapshot_id}")

    # Wait until the snapshot is fully saved before moving on
    print("  Waiting for snapshot to complete...")
    ec2.get_waiter('snapshot_completed').wait(SnapshotIds=[snapshot_id])
    print(f"  Snapshot COMPLETE: {snapshot_id}")

    return snapshot_id


def find_idle_snapshots():
    """Find snapshots whose original volume no longer exists.
    These are 'orphaned' — there's no reason to keep paying for them.
    """

    # Use your own account ID so we don't scan public/AWS snapshots
    account_id = boto3.client('sts').get_caller_identity()['Account']
    all_snapshots = ec2.describe_snapshots(OwnerIds=[account_id])['Snapshots']

    # Get the list of volumes that currently exist
    existing_volume_ids = {
        v['VolumeId'] for v in ec2.describe_volumes()['Volumes']
    }

    idle = []
    for snap in all_snapshots:
        vol_id = snap.get('VolumeId', '')
        # If the snapshot's source volume is gone, the snapshot is idle
        if vol_id not in existing_volume_ids:
            idle.append(snap['SnapshotId'])
            cost = snap.get('VolumeSize', 0) * 0.05  # ~$0.05 per GB per month
            print(f"  Idle snapshot: {snap['SnapshotId']} | {snap.get('VolumeSize', 0)} GB | ~${cost:.2f}/month")

    if not idle:
        print("  No idle snapshots found.")

    return idle


def delete_idle_snapshots(snapshot_ids):
    """Delete a list of idle snapshots to stop paying for them."""

    if not snapshot_ids:
        print("  Nothing to delete.")
        return

    for snap_id in snapshot_ids:
        ec2.delete_snapshot(SnapshotId=snap_id)
        print(f"  Deleted: {snap_id}")

    print(f"  Cleaned up {len(snapshot_ids)} idle snapshot(s)")


# --- Run this file directly to scan and clean idle snapshots ---
if __name__ == '__main__':
    print("Scanning for idle snapshots...")
    idle = find_idle_snapshots()

    if idle:
        confirm = input(f"\nDelete {len(idle)} idle snapshot(s)? (y/n): ")
        if confirm.lower() == 'y':
            delete_idle_snapshots(idle)
