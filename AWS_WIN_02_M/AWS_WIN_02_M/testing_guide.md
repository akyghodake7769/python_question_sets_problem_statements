# Testing Guide: AWS_WIN_02_M (AWS EC2 Windows Monitoring & IIS)

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
2. **Install IIS:** Enable the Web-Server (IIS) role on the server and start the `W3SVC` service automatically.
3. **Configure Scheduled Task:** Create a Scheduled Task named `MemoryMonitorTask` that runs a command every 5 minutes to write system date and free memory to `C:\workspace\monitor\mem_usage.log`.
4. **Disk & CPU Diagnostics:** Generate disk utilization details for drive `C:` and top 5 processes by CPU consumption, logging them to `disk_report.txt` and `cpu_process_report.txt` under `C:\workspace\monitor`.
5. **Network & System Diagnostics:** Test local TCP port 80 connectivity and extract the last 5 System Event Log errors, writing them to `network_status.txt` and `event_errors.txt` under `C:\workspace\monitor`.

## Step 4: Verification
To verify your solution, ensure the python test environment is set up with `boto3`, then run the driver script or automated evaluator provided in the problem structure.
- The evaluation script will remotely execute SSM commands to verify that the IIS service status, scheduled task, and performance logs are set up correctly.
