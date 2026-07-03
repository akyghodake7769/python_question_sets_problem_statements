# AWS EC2 (Windows Server) Basics: Navigation, Environment Variables & File Operations

**Difficulty Level:** Medium

**Duration:** 60 Minutes

## Scenario

As a Windows System Administrator, you are tasked with setting up a baseline environment on a newly provisioned Windows Server in the cloud. You need to spin up a Windows Server EC2 instance, establish a workspace folder layout, configure system-wide environment variables, capture basic server metadata, and locate system log files.

## Task Objectives

Perform the following actions in the AWS cloud and guest OS environment:

### 1. Provision EC2 Instance (Windows Server)

- **Instance Name:** `labskraft-windows-basics-<your-labskraft-username>` (replace `<your-labskraft-username>` with your actual username, e.g. `labs-kraft-demo106`)
- **AMI (Operating System):** Microsoft Windows Server 2022 Base (or newer)
- **Instance Type:** `t2.micro`
- **Region:** `eu-west-2` (Europe - London)

### 2. Configure Directory Layout

On the running Windows Server instance, create the following directory structure:
- `C:\workspace\logs`
- `C:\workspace\backups`

### 3. Set Up System Environment Variables

Configure a system-wide environment variable named `APP_ENVIRONMENT` and assign it the value `production`.
- The variable must be set at the **System (Machine)** level so that it persists across reboots and is accessible by all user accounts.

### 4. System Metadata and Log Auditing

- Retrieve the computer hostname and operating system details, and write this information to `C:\workspace\sysinfo.txt`.
- Locate all log files ending in `.log` within the `C:\Windows` directory (non-recursively, just inside the root `C:\Windows` folder) and write their absolute paths (one path per line) to `C:\workspace\log_files.txt`.

## Verification

Once you have performed the tasks, you can run the verification script. The verification script will check the configuration of your EC2 resources via the AWS client and connect via Systems Manager (SSM) inside the Windows Guest OS to verify directory pathways, environment variables, and file content.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Validation | Marks |
| --------- | ----------- | ---------- | ----- |
| **TC1**   | **EC2 Instance Provisioning** | Running `t2.micro` Windows Server instance named `labskraft-windows-basics-<username>` in `eu-west-2` region. | 5 Marks |
| **TC2**   | **Directory Structure** | Folders `C:\workspace\logs` and `C:\workspace\backups` exist on the instance. | 5 Marks |
| **TC3**   | **System Environment Variables** | System environment variable `APP_ENVIRONMENT` is set permanently to `production`. | 5 Marks |
| **TC4**   | **Metadata & Log Auditing** | Files `sysinfo.txt` and `log_files.txt` exist in `C:\workspace` with correct contents. | 5 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure the instance name matches exactly: `labskraft-windows-basics-<your-labskraft-username>`.
- The instance must be a Windows Server machine of type `t2.micro`.
- Make sure to set the environment variable at the Machine level (e.g. using `[Environment]::SetEnvironmentVariable("APP_ENVIRONMENT", "production", "Machine")` or Windows GUI).
- File paths inside `log_files.txt` must be absolute paths (e.g., `C:\Windows\setupact.log`) separated by newlines.
