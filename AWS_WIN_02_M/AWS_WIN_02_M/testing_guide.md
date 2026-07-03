# Testing Guide: AWS_WIN_02_M (Windows Server Monitoring & IIS - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open PowerShell as Administrator
Open PowerShell on your local Windows system with Administrator privileges.

## Step 2: Execute PowerShell Commands
Run appropriate PowerShell commands to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Windows VM environment.
2. **Install IIS:** Enable the Web-Server (IIS) role on the server and start the `W3SVC` service automatically.
3. **Configure Scheduled Task:** Create a Scheduled Task named `MemoryMonitorTask` that runs a command every 5 minutes to write system date and free memory to `C:\workspace\monitor\mem_usage.log`.
4. **Disk & CPU Diagnostics:** Generate disk utilization details for drive `C:` and top 5 processes by CPU consumption, logging them to `disk_report.txt` and `cpu_process_report.txt` under `C:\workspace\monitor`.
5. **Network & System Diagnostics:** Test local TCP port 80 connectivity and extract the last 5 System Event Log errors, writing them to `network_status.txt` and `event_errors.txt` under `C:\workspace\monitor`.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Open terminal/PowerShell and run `python student_workspace/run.py` from the root workspace directory.
- The evaluation script will execute PowerShell checks locally to verify IIS service status, scheduled tasks, and performance logs are set up correctly.
