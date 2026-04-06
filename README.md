# AWS Cloud Optimization Project

A Python + boto3 project that automates AWS cost optimization by cleaning up idle snapshots and reporting unattached EBS volumes.

Each AWS component (EC2, Volumes, Snapshots) lives in its own folder so you can clearly see what each part does. `main.py` ties them all together.

---

## Project Structure

```
cloud-optimization-project/
│
├── ec2/
│   └── ec2_ops.py          # Create and delete EC2 instances
│
├── volumes/
│   └── volume_ops.py       # Find unattached (wasted) EBS volumes
│
├── snapshots/
│   └── snapshot_ops.py     # Create snapshots, find idle ones, delete them
│
├── main.py                 # Runs the full flow — start here
└── architecture_animated.svg
```

---

## What Each Component Does

| Component | File | What it does |
|-----------|------|--------------|
| **EC2** | `ec2/ec2_ops.py` | Launches a t2.micro instance, waits for it to run, then terminates it |
| **Volumes** | `volumes/volume_ops.py` | Scans for EBS volumes that are not attached to any EC2 (wasted money) |
| **Snapshots** | `snapshots/snapshot_ops.py` | Takes a snapshot backup, then finds and deletes orphaned snapshots |
| **Main** | `main.py` | Interactive 3-stage flow — brings all 3 together |

---

## How to Run

### Full demo (recommended — start here)
```bash
python main.py
```
Walks you through 3 stages with yes/no prompts at each step.

### Test each component individually
```bash
python ec2/ec2_ops.py         # Test EC2 only
python volumes/volume_ops.py  # Scan for unattached volumes
python snapshots/snapshot_ops.py  # Scan and clean idle snapshots
```

---

## Requirements

```bash
pip install boto3
```

AWS credentials must be configured:
```bash
aws configure
```

---

## Region

All scripts use **eu-central-1 (Frankfurt)**. Edit the `region_name` in each file to change it.

---

## Architecture

Open `architecture_animated.svg` in a browser to view the animated diagram.
