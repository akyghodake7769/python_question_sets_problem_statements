# DevOps Lab: Linux File System & Directory Navigation (Local VM)

Duration : 60 Min.

## Scenario

As a DevOps engineer at LabsKraft, you are tasked with setting up a specific directory hierarchy for an application on a newly provisioned local Ubuntu Linux server/VM. This involves utilizing Linux directory navigation commands and file operations.

## Task Objectives

Perform the following actions inside the default home directory (`/home/ubuntu`) of the local Ubuntu system:

### 1. Directory Hierarchy Creation

- Create a directory hierarchy inside the home directory (`/home/ubuntu`) containing:
  - `/home/ubuntu/app/config`
  - `/home/ubuntu/app/logs`

### 2. Initial File Creation

- Create the following blank files inside the newly created directories:
  - `app.conf` inside `/home/ubuntu/app/config`
  - `error.log` inside `/home/ubuntu/app/logs`

### 3. File Copy, Rename, and Search Operations

- Perform the following file operations:
  - Copy the `app.conf` file from `/home/ubuntu/app/config` to `/home/ubuntu/app/` directory.
  - Rename or move the copied file `/home/ubuntu/app/app.conf` to `/home/ubuntu/app/app.conf.backup`.
  - Search recursively within the `/home/ubuntu` directory for all files or lines containing the string `"app"`, and save/append the search results to `/home/ubuntu/search_results.txt`.

### 4. Disk Space Analysis

- Perform disk analysis to check current disk space utilization, and save the formatted, human-readable report to `/home/ubuntu/disk_usage.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Directory hierarchy (`app/config`, `app/logs`) created successfully | 5 Marks |
| **TC2**   | Initial files (`app.conf` in config, `error.log` in logs) created successfully | 5 Marks |
| **TC3**   | File operations (`cp`, `mv`/rename) and keyword search results generated | 5 Marks |
| **TC4**   | Disk usage output (`disk_usage.txt`) generated correctly | 5 Marks |

**Total Score: 20 Marks**
