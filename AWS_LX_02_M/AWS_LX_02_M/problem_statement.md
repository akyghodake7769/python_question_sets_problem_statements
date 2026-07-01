# Linux File Operations & Security Permissions

# Duration : 60 Min.

## Scenario

You are responsible for securing sensitive configuration files on a Linux web server hosted on an EC2 instance to prevent unauthorized access. You must use Linux permissions correctly to ensure data security.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `labskraft-ubuntu-ec2-<your-labskraft-username>` (replace `<your-labskraft-username>` with your actual LabsKraft username)
- **AMI (Operating System):** Ubuntu Server (e.g., Ubuntu Server 24.04 LTS (HVM))
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Create Secure Data and Users

Log in to the EC2 instance via SSH:
- Create a secure directory: `/home/ubuntu/secure_data`.
- Create files `passwords.txt` and `config.ini` inside `/home/ubuntu/secure_data`.
- Add dummy content to both files using the `echo` command (e.g., `echo "secret123" > passwords.txt`).

### 3. File Permissions (chmod)

- Set restrictive permissions on `passwords.txt` so that only the owner can read it, and no one else can read, write, or execute it (`chmod 400`).
- Set permissions on `config.ini` so the owner has full permissions, and the group and others can only read and execute (`chmod 755`).

### 4. Ownership (chown)

- Create a new Linux test user named `appuser` (you can use `sudo useradd appuser`).
- Change the ownership of `config.ini` so that `appuser` is the owner of the file (`chown appuser config.ini`).
- Run `ls -l /home/ubuntu/secure_data > /home/ubuntu/permissions.txt` to verify the permissions and ownerships.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                          | Marks   |
| --------- | ------------------------------------------------------------------------------------ | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `labskraft-ubuntu-ec2-<username>`) | 5 Marks |
| **TC2**   | Directory, files (`passwords.txt`, `config.ini`), and user `appuser` created         | 5 Marks |
| **TC3**   | Proper permissions (`chmod 400` & `755`) applied                                     | 5 Marks |
| **TC4**   | Ownership (`chown user`) correctly configured and output to `permissions.txt`        | 5 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name is exactly `labskraft-ubuntu-ec2-<your-labskraft-username>`.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
