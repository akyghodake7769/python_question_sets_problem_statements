# Testing Guide: AWS_LX_01_M (Linux File System & Directory Navigation)

This guide provides the exact steps required to solve and verify the problem statement successfully.

## Step 1: Provision Infrastructure
1. Log in to the AWS Management Console.
2. Launch an EC2 Instance with the following specifications:
   - **Name:** `labskraft-ubuntu-ec2-<your-username>`
   - **OS:** Ubuntu Server
   - **Instance Type:** `t2.micro`
   - **IAM Role:** `Ec2_instance_SSM`

## Step 2: Connect to the Instance
1. Go to the EC2 console and select your instance.
2. Click **Connect** and choose the **Session Manager (SSM)** tab.
3. Click **Connect** to open the terminal. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 3: Execute Linux Commands
Run the following commands to satisfy the test cases:

```bash
# 1. Create Directory Hierarchy
mkdir -p /home/ubuntu/app/config
mkdir -p /home/ubuntu/app/logs

# 2. File Operations
touch /home/ubuntu/app/app.conf.backup
touch /home/ubuntu/search_results.txt

# 3. Disk Space Analysis
df -h > /home/ubuntu/disk_usage.txt
```

## Step 4: Verification
To verify your solution, ensure the python test environment is set up with `boto3`, then run the driver script or automated evaluator provided in the problem structure.
- The evaluation script will remotely execute SSM commands to verify that the directories and files exist and that the disk usage log was generated successfully.
