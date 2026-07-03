# DevOps Lab: Linux File Operations & Security Permissions

Duration : 60 Min.

## Scenario

As a DevOps engineer at LabsKraft, you are responsible for securing sensitive configuration files on a Linux web server hosted on an EC2 instance to prevent unauthorized access. You must use file permission and ownership commands to restrict access.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username and exam code, e.g. `labs-kraft-demo106-1123`)
- **AMI (Operating System):** Ubuntu Server (e.g., 22.04 LTS)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. User Creation

Log in to the EC2 instance via SSM Session Manager and perform the following operations:
- Create a new user named `appuser`.

### 3. File and Directory Setup

- Create a directory named `/home/ubuntu/secure_data` and two empty files inside it:
  - `passwords.txt`
  - `config.ini`

### 4. File Permissions Configuration

- Secure the files inside `/home/ubuntu/secure_data`:
  - Set the permissions of `passwords.txt` so that only the owner has read-only access (`400`).
  - Set the permissions of `config.ini` so that everyone has read, write, and execute access (`755`).

### 5. Ownership Change

- Change the ownership of `/home/ubuntu/secure_data/config.ini` to `appuser` (keep the group as default/ubuntu).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `<username>-<exam_code>`) | 4 Marks |
| **TC2**   | User `appuser` created successfully | 4 Marks |
| **TC3**   | Directory `secure_data` and files (`passwords.txt`, `config.ini`) created | 4 Marks |
| **TC4**   | Permissions applied (`400` on passwords.txt, `755` on config.ini) | 4 Marks |
| **TC5**   | Ownership of `config.ini` changed to `appuser` | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name matches one of the expected formats in the validation script.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
- Ensure the EC2 instance has the `Ec2_instance_SSM` IAM role attached for verification.
