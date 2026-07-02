# Testing Guide: AWS_LX_03_M (Linux Monitoring & Basic Troubleshooting)

This guide provides the exact steps required to solve and verify the problem statement successfully.

## Step 1: Provision Infrastructure
1. Log in to the AWS Management Console.
2. Launch an EC2 Instance with the following specifications:
   - **Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username, e.g. `labs-kraft-demo106`)
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
# 1. CPU and Process Monitoring
top -b -n 1 > /home/ubuntu/cpu_monitor.txt

# 2. Memory Monitoring
free -m > /home/ubuntu/memory.txt

# 3. Disk Monitoring
df -h > /home/ubuntu/disk.txt

# 4. Network Monitoring
netstat -tuln > /home/ubuntu/network.txt
```

## Step 4: Verification
To verify your solution, ensure the python test environment is set up with `boto3`, then run the driver script or automated evaluator provided in the problem structure.
- The evaluation script will remotely execute SSM commands to verify that these troubleshooting log files exist and contain actual data (file size > 0).
