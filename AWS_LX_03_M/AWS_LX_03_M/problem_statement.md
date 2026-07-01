# Linux Monitoring & Basic Troubleshooting

# Duration : 60 Min.

## Scenario

A cloud server is experiencing high resource utilization. You must provision an EC2 instance and generate diagnostic reports on system performance using various Linux monitoring tools to simulate a basic troubleshooting scenario.

## Task Objectives

Perform the following actions in the AWS environment:

### 1. Create EC2 Instance (Ubuntu Linux)

- **Instance Name:** `labskraft-ubuntu-ec2-<your-labskraft-username>` (replace `<your-labskraft-username>` with your actual LabsKraft username)
- **AMI (Operating System):** Ubuntu Server (e.g., Ubuntu Server 24.04 LTS (HVM))
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. CPU and Process Monitoring

Log in to the EC2 instance via SSH:
- Identify running processes and CPU usage using `top` or `ps`.
- Redirect the top 10 running processes (based on memory or CPU) to a log file: `ps aux --sort=-%cpu | head -n 11 > /home/ubuntu/cpu_monitor.txt`.

### 3. Memory Monitoring

- Check the system's memory usage using `free` or `vmstat`.
- Redirect the human-readable memory output to a log file: `free -m > /home/ubuntu/memory.txt`.

### 4. Disk and Network Troubleshooting

- Check the current disk capacity using `df -h` and directory sizes using `du -sh /var/*` and append both to a file: `df -h > /home/ubuntu/disk.txt && sudo du -sh /var/* >> /home/ubuntu/disk.txt`.
- Perform a network connectivity check using `ping` (e.g., to `google.com`) and view open ports using `netstat` (or `ss`), saving the open listening ports output to `network.txt`: `ss -tuln > /home/ubuntu/network.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                                                          | Marks   |
| --------- | ------------------------------------------------------------------------------------ | ------- |
| **TC1**   | EC2 Instance Existence (`t2.micro`, Ubuntu, named `labskraft-ubuntu-ec2-<username>`) | 5 Marks |
| **TC2**   | CPU and process logs (`cpu_monitor.txt`) successfully generated                      | 5 Marks |
| **TC3**   | Memory logs (`memory.txt`) successfully generated                                    | 5 Marks |
| **TC4**   | Disk logs (`disk.txt`) and Network logs (`network.txt`) successfully generated       | 5 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name is exactly `labskraft-ubuntu-ec2-<your-labskraft-username>`.
- The instance must be an Ubuntu Linux machine of type `t2.micro`.
