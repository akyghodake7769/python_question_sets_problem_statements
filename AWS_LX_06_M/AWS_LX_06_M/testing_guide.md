# Testing Guide: AWS_LX_06_M (Linux Monitoring & Troubleshooting - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
Run appropriate Linux commands in the terminal to achieve the following:
1. **Monitor CPU & Processes:** Save a snapshot of active processes sorted by CPU usage to `/home/ubuntu/cpu_monitor.txt`.
2. **Monitor Memory Usage:** Check memory statistics in megabytes and save the output to `/home/ubuntu/memory.txt`.
3. **Run Disk Diagnostics:** Verify capacity and space on all mounted filesystems and save it to `/home/ubuntu/disk.txt`.
4. **Analyze Network Connections:** Check listening ports and active network connections, and save to `/home/ubuntu/network.txt`.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local diagnostics logs under `/home/ubuntu`, then display your score.
