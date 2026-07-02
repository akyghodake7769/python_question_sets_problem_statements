# DevOps Lab: Linux File System & Directory Navigation

Duration : 60 Min.

## Scenario

As a DevOps engineer at LabsKraft, you are tasked with setting up a specific directory hierarchy for an application on a newly provisioned AWS EC2 instance. This involves utilizing Linux directory navigation commands and file operations.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username, e.g. `labs-kraft-demo106`)
- **AMI (Operating System):** Ubuntu Server (e.g., 22.04 LTS)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Linux Directory Navigation & Creation

Log in to the EC2 instance via SSM Session Manager and perform the following operations:
- Use `mkdir -p` to create the following directory hierarchy inside the default home directory (`/home/ubuntu`):
  - `/home/ubuntu/app/config`
  - `/home/ubuntu/app/logs`
- Navigate into `/home/ubuntu/app/config` using `cd` and display the current path using `pwd`.

### 3. File Creation and Operations

- Inside the `config` directory, use `touch` to create `app.conf`.
- Inside the `logs` directory, use `touch` to create `error.log`.
- Copy (`cp`) the `app.conf` file to `/home/ubuntu/app/` directory.
- Move/Rename (`mv`) the copied file `/home/ubuntu/app/app.conf` to `/home/ubuntu/app/app.conf.backup`.
- Search for the keyword "app" in the `/home/ubuntu` directory recursively using the `find` or `grep` command, and append the results to `/home/ubuntu/search_results.txt`.

### 4. Disk Analysis

- Check the disk usage using `df -h` and redirect the output to `/home/ubuntu/disk_usage.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                          | Marks   |
| --------- | ------------------------------------------------------------------------------------ | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `<username>-<exam_code>`) | 5 Marks |
| **TC2**   | Directory hierarchy (`app/config`, `app/logs`) and initial files created successfully| 5 Marks |
| **TC3**   | File operations (`cp`, `mv`) and search (`search_results.txt`) completed             | 5 Marks |
| **TC4**   | Disk usage output (`disk_usage.txt`) generated correctly                             | 5 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name is exactly `<your-labskraft-username>-<your-exam-code>`.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
- Ensure the EC2 instance has the `Ec2_instance_SSM` IAM role attached for verification.
