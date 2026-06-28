# AWS EC2 (Ubuntu) & Storage Infrastructure Provisioning

Duration : 120 Min.

## Scenario

As a Cloud Engineer, you are tasked with provisioning compute and storage infrastructure. Your objective is to create an Ubuntu Linux EC2 instance, provision an EBS volume, attach it to the instance, and mount the storage using standard Linux commands.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `labskraft-ubuntu-ec2-<your-labskraft-username>` (replace `<your-labskraft-username>` with your actual LabsKraft username, e.g. `labs-kraft-demo106`)
- **AMI (Operating System):** Ubuntu Server (e.g., 22.04 LTS)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Create and Attach EBS Volume

- **Volume Size:** `10 GB`
- **Volume Type:** `gp3` (General Purpose SSD)
- **Attach Volume:** Attach the created EBS volume to the Ubuntu EC2 instance created in the previous step.

### 3. Mount the EBS Volume in Linux

- **File System:** Format the attached volume with the `ext4` filesystem.
- **Mount Point:** Mount the volume to the directory `/mnt/data-store`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                          | Marks   |
| --------- | ------------------------------------------------------------------------------------ | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `labskraft-ubuntu-ec2-<username>`) | 5 Marks |
| **TC2**   | EBS Volume Created (10 GB, `gp3`) and Attached to EC2                                | 5 Marks |
| **TC3**   | EBS Volume Mounted at `/mnt/data-store` (`ext4`)                                     | 5 Marks |

**Total Score: 15 Marks**

## Important Notes

- Ensure the instance name is exactly `labskraft-ubuntu-ec2-<your-labskraft-username>`.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
- Ensure the EBS volume is mounted persistently so it survives a reboot (e.g., configured in `/etc/fstab`).
