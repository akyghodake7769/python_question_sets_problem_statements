# AWS EC2 (Windows Server) Basics: Navigation, Environment Variables & File Operations

**Difficulty Level:** Medium

**Duration:** 60 Minutes

## Scenario

As a Windows System Administrator, you are tasked with setting up a baseline environment on a newly provisioned Windows Server in the cloud. You need to spin up a Windows Server EC2 instance, establish a workspace folder layout, configure system-wide environment variables, capture basic server metadata, and locate system log files.

## Task Objectives

Perform the following actions in the AWS cloud and guest OS environment:

### 1. Provision EC2 Instance (Windows Server)

- **Instance Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username and exam code, e.g. `labs-kraft-demo106-1123`)
- **AMI (Operating System):** Microsoft Windows Server 2022 Base (or newer)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)
- **IAM Role:** `Ec2_instance_SSM`

### 2. Configure Directory Layout

Log in to the Windows Server instance and perform the following operations:
- Create the target directories `C:\workspace\logs` and `C:\workspace\backups`.

### 3. Set Up System Environment Variables

- Configure a system-wide environment variable named `APP_ENVIRONMENT` and assign it the value `production`.
- The variable must be set permanently so that it persists across reboots and is accessible by all user accounts.

### 4. System Metadata Auditing

- Retrieve the computer hostname and operating system name (caption) of the instance, and save this information to `C:\workspace\sysinfo.txt`.

### 5. System Log Auditing

- Locate all log files ending in `.log` directly inside the root `C:\Windows` directory (non-recursively) and write their absolute paths (one path per line) to `C:\workspace\log_files.txt`.

## Verification

Once you have performed the tasks, you can run the verification script. The verification script will check the configuration of your EC2 resources via the AWS client and connect via Systems Manager (SSM) inside the Windows Guest OS to verify directory pathways, environment variables, and file content.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Windows Server, named `<username>-<exam_code>`) | 4 Marks |
| **TC2**   | Directory structure (`C:\workspace\logs` and `C:\workspace\backups`) created successfully | 4 Marks |
| **TC3**   | System environment variable `APP_ENVIRONMENT` set permanently to `production` | 4 Marks |
| **TC4**   | Hostname and OS details successfully saved to `C:\workspace\sysinfo.txt` | 4 Marks |
| **TC5**   | Path list of `.log` files successfully saved to `C:\workspace\log_files.txt` | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name matches exactly: `<your-labskraft-username>-<your-exam-code>`.
- The instance must be a Windows Server machine of type `t2.micro`.
- Make sure the environment variable is set permanently.
- File paths inside `log_files.txt` must be absolute paths (e.g., `C:\Windows\setupact.log`) separated by newlines.
- Ensure the EC2 instance has the `Ec2_instance_SSM` IAM role attached for verification.
