# DevOps Lab: Linux Monitoring & Basic Troubleshooting

Duration : 60 Min.

## Scenario

As a DevOps engineer at LabsKraft, you are tasked with troubleshooting a cloud server experiencing high resource utilization. You must provision an EC2 instance and generate diagnostic reports on system performance using various Linux monitoring commands.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `<your-labskraft-username>-<your-exam-code>` (replace `<your-labskraft-username>-<your-exam-code>` with your actual LabsKraft username, e.g. `labs-kraft-demo106`)
- **AMI (Operating System):** Ubuntu Server (e.g., 22.04 LTS)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. CPU and Process Monitoring

Log in to the EC2 instance via SSM Session Manager and perform the following operations:
- Display active processes, sort them by CPU usage, and log the snapshot output to a file named `/home/ubuntu/cpu_monitor.txt`. (e.g., using `top -b -n 1` or `ps`)

### 3. Memory Monitoring

- Check the system's memory usage (total, used, free) in megabytes and log the output to `/home/ubuntu/memory.txt`. (e.g., using `free -m` or `vmstat`)

### 4. Disk and Network Troubleshooting

- Check the total disk capacity and free space on all mounted filesystems and log it to `/home/ubuntu/disk.txt`. (e.g., using `df -h`)
- List all active network connections and listening ports on the server and log them to `/home/ubuntu/network.txt`. (e.g., using `netstat -tuln` or `ss -tuln`)

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the AWS cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                          | Marks   |
| --------- | ------------------------------------------------------------------------------------ | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `<username>-<exam_code>`) | 5 Marks |
| **TC2**   | CPU/process monitoring snapshot output `cpu_monitor.txt` generated successfully       | 5 Marks |
| **TC3**   | Memory monitoring snapshot output `memory.txt` generated successfully                | 5 Marks |
| **TC4**   | Disk and Network diagnostics output `disk.txt` and `network.txt` generated           | 5 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name is exactly `<your-labskraft-username>-<your-exam-code>`.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
- Ensure the EC2 instance has the `Ec2_instance_SSM` IAM role attached for verification.
