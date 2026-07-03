# Testing Guide: AWS_WIN_01_M (Windows Server Basics - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open PowerShell as Administrator
Open PowerShell on your local Windows system with Administrator privileges.

## Step 2: Execute PowerShell Commands
Run appropriate PowerShell commands to achieve the following:
1. **Local VM Environment:** Make sure you are working on the local Windows VM environment.
2. **Directory Structure:** Create the target folders `C:\workspace\logs` and `C:\workspace\backups` on the system.
3. **Configure Environment Variables:** Permanently define the system environment variable `APP_ENVIRONMENT` and set it to `production`.
4. **Metadata Auditing:** Query the computer hostname and operating system caption, saving them to `C:\workspace\sysinfo.txt`.
5. **Log Auditing:** Search for all `.log` files directly under `C:\Windows` (non-recursively) and save their absolute paths to `C:\workspace\log_files.txt`.

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Open terminal/PowerShell and run `python student_workspace/run.py` from the root workspace directory.
- The evaluation script will execute PowerShell checks locally to verify directory layout, environment variable, and diagnostic log files.
