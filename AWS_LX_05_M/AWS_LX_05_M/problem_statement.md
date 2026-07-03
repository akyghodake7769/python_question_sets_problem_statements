# DevOps Lab: Linux File Operations & Security Permissions (Local VM)

Duration : 60 Min.

## Scenario

As a DevOps engineer at LabsKraft, you are responsible for securing sensitive configuration files on a Linux web server hosted on a local Ubuntu server/VM to prevent unauthorized access. You must use file permission and ownership commands to restrict access.

## Task Objectives

Perform the following actions inside the default home directory (`/home/ubuntu`) of the local Ubuntu system:

### 1. User Creation

- Create a new user named `appuser`.

### 2. File and Directory Setup

- Create a directory named `/home/ubuntu/secure_data` and two empty files inside it:
  - `passwords.txt`
  - `config.ini`

### 3. File Permissions Configuration

- Secure the files inside `/home/ubuntu/secure_data`:
  - Set the permissions of `passwords.txt` so that only the owner has read-only access (`400`).
  - Set the permissions of `config.ini` so that everyone has read, write, and execute access (`755`).

### 4. Ownership Change

- Change the ownership of `/home/ubuntu/secure_data/config.ini` to `appuser` (keep the group as default/ubuntu).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | User `appuser` created successfully | 5 Marks |
| **TC2**   | Directory `secure_data` and files (`passwords.txt`, `config.ini`) created | 5 Marks |
| **TC3**   | Permissions applied (`400` on passwords.txt, `755` on config.ini) | 5 Marks |
| **TC4**   | Ownership of `config.ini` changed to `appuser` | 5 Marks |

**Total Score: 20 Marks**
