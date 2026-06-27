# DevOps Lab: AWS EC2 (Windows DB Server) & Advanced Storage Management

Duration : 30 Min.

## Scenario

As a DevOps engineer at LabsKraft, you need to configure a comprehensive Windows-based compute and storage solution for a database. Your task involves setting up a Windows Server EC2 instance, creating a high-performance EBS volume, attaching it, and initializing/formatting it for database storage using Windows Disk Management.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Windows Server)

- **Instance Name:** `labskraft-db-server-<your-labskraft-username>` (replace `<your-labskraft-username>` with your actual LabsKraft username, e.g. `labs-kraft-demo106`)
- **AMI (Operating System):** Microsoft Windows Server (e.g., 2022 Base)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Create and Attach EBS Volume

- **Volume Size:** `20 GB`
- **Volume Type:** `io2` (Provisioned IOPS SSD) with 500 IOPS
- **Attach Volume:** Attach the created EBS volume to the Windows EC2 instance created in the previous step.

### 3. Initialize and Format the EBS Volume in Windows

- **Initialization:** Bring the newly attached disk online and initialize it.
- **File System:** Format the attached volume with the `NTFS` filesystem.
- **Drive Letter/Mount:** Assign the volume the drive letter `F:` (or mount it to a specific folder if preferred by your DB setup, but for this lab, assigning drive `F:` is expected).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                         | Marks   |
| --------- | ----------------------------------------------------------------------------------- | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Windows, named `labskraft-db-server-<username>`)| 5 Marks |
| **TC2**   | EBS Volume Created (20 GB, `io2` with 500 IOPS) and Attached to EC2                 | 5 Marks |
| **TC3**   | EBS Volume Formatted as `NTFS` and Assigned Drive Letter `F:`                       | 5 Marks |

**Total Score: 15 Marks**

## Important Notes

- Ensure the instance name is exactly `labskraft-db-server-<your-labskraft-username>`.
- The instance must be a Windows Server machine of type `t2.micro`.
- You will need to connect to the instance (via RDP) to use Disk Management or PowerShell to initialize and format the disk.
