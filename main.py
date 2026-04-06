"""
main.py — The Orchestrator
Ties together EC2, Volumes, and Snapshots into one full demo flow.

Run:  python main.py
"""

from ec2.ec2_ops import create_ec2, get_root_volume, delete_ec2
from volumes.volume_ops import find_unattached_volumes
from snapshots.snapshot_ops import create_snapshot, find_idle_snapshots, delete_idle_snapshots


def ask(question):
    return input(f"\n{question} (y/n): ").strip().lower() == 'y'


def main():
    print("=" * 55)
    print("   AWS Cloud Optimization Demo")
    print("   EC2  →  Volumes  →  Snapshots")
    print("=" * 55)

    instance_id = None

    # ── STAGE 1: Create EC2 + snapshot ──────────────────────────
    if ask("Stage 1: Create an EC2 instance and take a snapshot?"):

        print("\n[EC2] Launching instance...")
        instance_id = create_ec2()

        print("\n[Volumes] Getting root volume attached to the EC2...")
        volume_id = get_root_volume(instance_id)

        print("\n[Snapshots] Taking a backup snapshot of the volume...")
        create_snapshot(volume_id)

    # ── STAGE 2: Delete the EC2 ──────────────────────────────────
    if instance_id and ask("\nStage 2: Delete the EC2 instance?"):

        print("\n[EC2] Deleting instance...")
        delete_ec2(instance_id)

    # ── STAGE 3: Find waste and clean up ────────────────────────
    if ask("\nStage 3: Scan for idle snapshots and unattached volumes?"):

        print("\n[Volumes] Checking for unattached EBS volumes...")
        find_unattached_volumes()

        print("\n[Snapshots] Scanning for idle (orphaned) snapshots...")
        idle = find_idle_snapshots()

        if idle and ask(f"\nFound {len(idle)} idle snapshot(s). Delete them to save costs?"):
            delete_idle_snapshots(idle)

    print("\n" + "=" * 55)
    print("   Done!")
    print("=" * 55)


if __name__ == '__main__':
    main()
