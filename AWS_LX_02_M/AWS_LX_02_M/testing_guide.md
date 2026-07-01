# Testing Guide: AWS_LX_02_M (Linux File Operations & Security Permissions)

This guide provides the exact steps required to solve and verify the problem statement successfully.

## Step 1: Provision Infrastructure
1. Log in to the AWS Management Console.
2. Launch an EC2 Instance with the following specifications:
   - **Name:** `labskraft-ubuntu-ec2-<your-username>`
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
# 1. Create User
sudo useradd appuser

# 2. Create Files and Directories
mkdir -p /home/ubuntu/secure_data
touch /home/ubuntu/secure_data/passwords.txt
touch /home/ubuntu/secure_data/config.ini

# 3. Set Permissions
chmod 400 /home/ubuntu/secure_data/passwords.txt
chmod 755 /home/ubuntu/secure_data/config.ini

# 4. Set Ownership
sudo chown appuser /home/ubuntu/secure_data/config.ini
```

## Step 4: Verification
To verify your solution, ensure the python test environment is set up with `boto3`, then run the driver script or automated evaluator provided in the problem structure.
- The evaluation script will remotely execute SSM commands using `stat` to verify the exact octal permissions and ownership applied to the files.
