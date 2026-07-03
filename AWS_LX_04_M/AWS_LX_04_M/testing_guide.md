# Testing Guide: AWS_LX_04_M (Linux File System & Directory Navigation - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Step 1: Open the Terminal
Open the terminal on your local Linux machine/VM. Switch to the ubuntu user if needed (`sudo su - ubuntu`).

## Step 2: Execute Linux Commands
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

## Step 3: Verification
To verify your solution, run the local verification script provided in the problem structure:
- Run `python3 student_workspace/run.py` from the root workspace directory.
- The evaluation script will check your local `/home/ubuntu` directory structure, files, permissions, and logs, then display your score.
