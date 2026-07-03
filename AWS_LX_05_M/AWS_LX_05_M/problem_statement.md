# DevOps Lab: Linux File Operations & Security Permissions (Local VM)

Duration : 60 Min.

## Scenario

As a System Engineer in a technology firm, you are responsible for securing sensitive configuration files on a Linux web server hosted on a local Ubuntu server/VM to prevent unauthorized access. You must use file permission and ownership commands to restrict access.

## Task Objectives

Perform the following actions inside the default home directory (`/home/ubuntu`) of the local Ubuntu system:

### 1. Environment Verification
- Ensure the local VM environment is running Ubuntu Linux with default `/home/ubuntu` workspace.

### 2. User Creation

- Create a new user named `appuser`.

### 3. File and Directory Setup

- Create a directory named `/home/ubuntu/secure_data` and two empty files inside it:
  - `passwords.txt`
  - `config.ini`

### 4. File Permissions Configuration

- Secure the files inside `/home/ubuntu/secure_data`:
  - Set the permissions of `passwords.txt` so that only the owner has read-only access (`400`).
  - Set the permissions of `config.ini` so that everyone has read, write, and execute access (`755`).

### 5. Ownership Change

- Change the ownership of `/home/ubuntu/secure_data/config.ini` to `appuser` (keep the group as default/ubuntu).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 4 Marks |
| **TC2**   | User `appuser` created successfully | 4 Marks |
| **TC3**   | Directory `secure_data` and files (`passwords.txt`, `config.ini`) created | 4 Marks |
| **TC4**   | Permissions applied (`400` on passwords.txt, `755` on config.ini) | 4 Marks |
| **TC5**   | Ownership of `config.ini` changed to `appuser` | 4 Marks |

**Total Score: 20 Marks**
