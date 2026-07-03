# DevOps Lab: Linux Monitoring & Basic Troubleshooting

Duration : 60 Min.

## Scenario

As a System Engineer in a technology firm, you are tasked with troubleshooting a cloud server experiencing high resource utilization. You must provision an EC2 instance and generate diagnostic reports on system performance using various Linux monitoring commands.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username and exam code, e.g. `labs-kraft-demo106-1123`)
- **AMI (Operating System):** Ubuntu Server (e.g., 22.04 LTS)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. CPU and Process Monitoring

Log in to the EC2 instance via SSM Session Manager and perform the following operations:
- Display active processes, sort them by CPU usage, and log the snapshot output to `/home/ubuntu/cpu_monitor.txt`.

### 3. Memory Monitoring

- Check the system's memory usage in megabytes and log the output to `/home/ubuntu/memory.txt`.

### 4. Disk Diagnostics

- Check the total disk capacity and free space on all mounted filesystems and log it to `/home/ubuntu/disk.txt`.

### 5. Network Troubleshooting

- List all active network connections and listening ports on the server and log them to `/home/ubuntu/network.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `<username>-<exam_code>`) | 4 Marks |
| **TC2**   | CPU/process monitoring snapshot output `cpu_monitor.txt` generated successfully | 4 Marks |
| **TC3**   | Memory monitoring snapshot output `memory.txt` generated successfully | 4 Marks |
| **TC4**   | Disk diagnostics output `disk.txt` generated successfully | 4 Marks |
| **TC5**   | Network diagnostics output `network.txt` generated successfully | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name matches one of the expected formats in the validation script.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
- Ensure the EC2 instance has the `Ec2_instance_SSM` IAM role attached for verification.
