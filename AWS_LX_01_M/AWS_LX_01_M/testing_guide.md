# Testing Guide: AWS_LX_01_M (Linux File System & Directory Navigation)

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
1. **Create the directories:**
   Create the target folders `/home/ubuntu/app/config` and `/home/ubuntu/app/logs` inside the `/home/ubuntu` home directory structure.
2. **Create target files:**
   Create empty configuration and error files in the respective folders (`app.conf` inside the config folder, and `error.log` inside the logs folder).
3. **Backup configuration:**
   Copy `app.conf` to `/home/ubuntu/app/` and rename it to `app.conf.backup`.
4. **Keyword search:**
   Find all files or content containing the keyword `"app"` inside `/home/ubuntu` and redirect/append the output to `/home/ubuntu/search_results.txt`.
5. **Disk analysis:**
   Run the command to show human-readable file system disk usage and save the output directly to `/home/ubuntu/disk_usage.txt`.

## Step 4: Verification
To verify your solution, ensure the python test environment is set up with `boto3`, then run the driver script or automated evaluator provided in the problem structure.
- The evaluation script will remotely execute SSM commands to verify that the directories and files exist and that the disk usage log was generated successfully.
