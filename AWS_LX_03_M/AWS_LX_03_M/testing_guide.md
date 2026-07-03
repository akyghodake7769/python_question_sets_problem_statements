# Testing Guide: AWS_LX_03_M (Linux Monitoring & Basic Troubleshooting)

This guide provides instructions on how to solve and verify the problem statement successfully.

## Step 1: Provision Infrastructure
1. Log in to the AWS Management Console.
2. Launch an EC2 Instance with the following specifications:
   - **Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username and exam code, e.g. `labs-kraft-demo106-1123`)
   - **OS:** Ubuntu Server
   - **Instance Type:** `t2.micro`
   - **IAM Role:** `Ec2_instance_SSM`

## Step 2: Connect to the Instance
1. Go to the EC2 console and select your instance.
2. Click **Connect** and choose the **Session Manager (SSM)** tab.
3. Click **Connect** to open the terminal. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 3: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Provision EC2 Instance:** Launch the Ubuntu server matching naming standards.
2. **Monitor CPU & Processes:** Save a snapshot of active processes sorted by CPU usage to `/home/ubuntu/cpu_monitor.txt`.
3. **Monitor Memory Usage:** Check memory statistics in megabytes and save the output to `/home/ubuntu/memory.txt`.
4. **Run Disk Diagnostics:** Verify capacity and space on all mounted filesystems and save it to `/home/ubuntu/disk.txt`.
5. **Analyze Network Connections:** Check listening ports and active network connections, and save to `/home/ubuntu/network.txt`.

## Step 4: Verification
To verify your solution, ensure the python test environment is set up with `boto3`, then run the driver script or automated evaluator provided in the problem structure.
- The evaluation script will remotely execute SSM commands to verify that these troubleshooting log files exist and contain actual data.
