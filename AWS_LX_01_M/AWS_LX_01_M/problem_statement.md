# DevOps Lab: Linux File System & Directory Navigation

Duration : 60 Min.

## Scenario

As a DevOps engineer at LabsKraft, you are tasked with setting up a specific directory hierarchy for an application on a newly provisioned AWS EC2 instance. This involves utilizing Linux directory navigation commands and file operations.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username and exam code, e.g. `labs-kraft-demo106-1123`)
- **AMI (Operating System):** Ubuntu Server (e.g., 22.04 LTS)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Directory Hierarchy Creation

Log in to the EC2 instance via SSM Session Manager and perform the following operations:
- Create a directory hierarchy inside the default home directory (`/home/ubuntu`) containing:
  - `/home/ubuntu/app/config`
  - `/home/ubuntu/app/logs`

### 3. Initial File Creation

- Create the following blank files inside the newly created directories:
  - `app.conf` inside `/home/ubuntu/app/config`
  - `error.log` inside `/home/ubuntu/app/logs`

### 4. File Copy, Rename, and Search Operations

- Perform the following file operations on the instance:
  - Copy the `app.conf` file from `/home/ubuntu/app/config` to `/home/ubuntu/app/` directory.
  - Rename or move the copied file `/home/ubuntu/app/app.conf` to `/home/ubuntu/app/app.conf.backup`.
  - Search recursively within the `/home/ubuntu` directory for all files or lines containing the string `"app"`, and save/append the search results to `/home/ubuntu/search_results.txt`.

### 5. Disk Space Analysis

- Perform disk analysis to check current disk space utilization, and save the formatted, human-readable report to `/home/ubuntu/disk_usage.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `<username>-<exam_code>`) | 4 Marks |
| **TC2**   | Directory hierarchy (`app/config`, `app/logs`) created successfully | 4 Marks |
| **TC3**   | Initial files (`app.conf` in config, `error.log` in logs) created successfully | 4 Marks |
| **TC4**   | File operations (`cp`, `mv`/rename) and keyword search results generated | 4 Marks |
| **TC5**   | Disk usage output (`disk_usage.txt`) generated correctly | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name matches one of the expected formats in the validation script.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
- Ensure the EC2 instance has the `Ec2_instance_SSM` IAM role attached for verification.
