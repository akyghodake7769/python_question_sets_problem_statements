# Testing Guide: AWS_WIN_01_M (AWS EC2 Windows Basics)

This guide provides instructions on how to solve and verify the problem statement successfully.

## Step 1: Provision Infrastructure
1. Log in to the AWS Management Console.
2. Launch an EC2 Instance with the following specifications:
   - **Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username and exam code, e.g. `labs-kraft-demo106-1123`)
   - **OS:** Windows Server (e.g. 2022 Base)
   - **Instance Type:** `t2.micro`
   - **IAM Role:** `Ec2_instance_SSM`

## Step 2: Connect to the Instance
1. Go to the EC2 console and select your instance.
2. Click **Connect** and choose the **Session Manager (SSM)** tab.
3. Click **Connect** to open the terminal/PowerShell session.

## Step 3: Execute PowerShell Commands
Run appropriate PowerShell commands in the terminal to achieve the following:
1. **Provision EC2 Instance:** Launch the Windows Server matching naming standards.
2. **Directory Structure:** Create the target folders `C:\workspace\logs` and `C:\workspace\backups` on the system.
3. **Configure Environment Variables:** Permanently define the system environment variable `APP_ENVIRONMENT` and set it to `production`.
4. **Metadata Auditing:** Query the computer hostname and operating system caption, saving them to `C:\workspace\sysinfo.txt`.
5. **Log Auditing:** Search for all `.log` files directly under `C:\Windows` (non-recursively) and save their absolute paths to `C:\workspace\log_files.txt`.

## Step 4: Verification
To verify your solution, ensure the python test environment is set up with `boto3`, then run the driver script or automated evaluator provided in the problem structure.
- The evaluation script will remotely execute SSM commands to verify that the directory layout, environment variable, and diagnostic log files are set up correctly.
