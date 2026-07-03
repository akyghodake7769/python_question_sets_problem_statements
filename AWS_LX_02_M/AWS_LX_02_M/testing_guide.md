# Testing Guide: AWS_LX_02_M (Linux File Operations & Security Permissions)

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
2. **Create Linux User:** Create a new user named `appuser` on the system.
3. **Setup Directory and Files:** Create a directory `/home/ubuntu/secure_data` containing blank `passwords.txt` and `config.ini` files.
4. **Configure Permissions:** Apply `400` (read-only by owner) on `passwords.txt` and `755` (read/write/execute by all) on `config.ini`.
5. **Update Ownership:** Change the owner of `config.ini` to `appuser`.

## Step 4: Verification
To verify your solution, ensure the python test environment is set up with `boto3`, then run the driver script or automated evaluator provided in the problem structure.
- The evaluation script will remotely execute SSM commands to verify that the user, directories, and files exist with correct permissions and ownership.
