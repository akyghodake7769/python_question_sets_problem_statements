# DevOps Lab: Linux File Operations & Security Permissions

Duration : 60 Min.

## Scenario

As a DevOps engineer at LabsKraft, you are responsible for securing sensitive configuration files on a Linux web server hosted on an EC2 instance to prevent unauthorized access. You must use file permission and ownership commands to restrict access.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `<your-labskraft-username>-AWS-LX-02-M` (replace `<your-labskraft-username>` with your actual LabsKraft username, e.g. `labs-kraft-demo106-AWS-LX-02-M`)
- **AMI (Operating System):** Ubuntu Server (e.g., 22.04 LTS)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Linux User Management & Directory Setup

Log in to the EC2 instance via SSM Session Manager and perform the following operations:
- Create a new user named `appuser`.
- Create a directory named `/home/ubuntu/secure_data`.
- Create two empty files inside `/home/ubuntu/secure_data`:
  - `passwords.txt`
  - `config.ini`

### 3. File Operations & Permissions Configuration

- Set the permissions of `passwords.txt` so that only the owner has read-only access (`400`).
- Set the permissions of `config.ini` so that everyone has read, write, and execute access (`755`).
- Change the ownership of `config.ini` to `appuser` (keep the group as default/ubuntu).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                          | Marks   |
| --------- | ------------------------------------------------------------------------------------ | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `<username>-AWS-LX-02-M`)           | 5 Marks |
| **TC2**   | User `appuser` and directories/files created successfully                            | 5 Marks |
| **TC3**   | `passwords.txt` permissions set to `400` and `config.ini` set to `755`               | 5 Marks |
| **TC4**   | Ownership of `config.ini` changed to `appuser`                                       | 5 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name is exactly `<your-labskraft-username>-AWS-LX-02-M`.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
- Ensure the EC2 instance has the `Ec2_instance_SSM` IAM role attached for verification.
