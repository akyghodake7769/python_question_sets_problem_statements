# Windows Server Monitoring, Logging & Service Management (Local VM)

**Difficulty Level:** Medium

**Duration:** 120 Minutes

## Scenario

As a Windows Cloud Ops Engineer, you are responsible for maintaining server availability, configuring automated administrative scripts, monitoring CPU/memory/disk performance, validating network connectivity, and diagnosing server health issues on a local Windows Server/VM. You need to host a web service using IIS, schedule a memory monitoring task, generate disk and CPU process utilization reports, test local network connectivity, and audit critical system event errors.

## Task Objectives

Perform the following actions inside the local Windows guest OS:

### 1. Environment Verification
- Ensure the local Windows Server environment is active and running.

### 2. Install and Manage Web Server (IIS)

- Install the **Web-Server (IIS)** role on the server.
- Ensure that the World Wide Web Publishing Service (`W3SVC`) is enabled, configured to start automatically, and running.

### 3. Configure Scheduled Memory Monitoring

- Create a Windows Scheduled Task named `MemoryMonitorTask` configured to run every 5 minutes.
- The task should execute a command or script that appends the current system date and free memory statistics to the log file `C:\workspace\monitor\mem_usage.log` (create the directory if it does not exist).

### 4. Disk & CPU Diagnostics

Generate performance snapshots under the `C:\workspace\monitor\` folder:
- **Disk Auditing:** Check disk space for the primary `C:` drive and save the utilization report to `C:\workspace\monitor\disk_report.txt`.
- **CPU & Process Monitoring:** List the top 5 CPU-consuming processes on the system and save this list to `C:\workspace\monitor\cpu_process_report.txt`.

### 5. Network & System Log Diagnostics

Generate network and error diagnostics under `C:\workspace\monitor\`:
- **Network Validation:** Validate connectivity on the local web server port (port 80) and save the TCP connection test output to `C:\workspace\monitor\network_status.txt`.
- **Event Log Diagnostics:** Extract the description/messages of the latest 5 error entries from the system event log and write them to `C:\workspace\monitor\event_errors.txt`.

## Verification

Once you have performed the tasks, you can run the verification script. The verification script will check the configuration on your local Windows system to check IIS service status, scheduled tasks, CPU/disk reports, network connection status, and event log files.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local Windows VM Environment active and verified | 4 Marks |
| **TC2**   | Web-Server (IIS) role installed and the `W3SVC` service running | 4 Marks |
| **TC3**   | Scheduled Task `MemoryMonitorTask` created and configured | 4 Marks |
| **TC4**   | Disk and CPU diagnostics reports generated under `C:\workspace\monitor` | 4 Marks |
| **TC5**   | Network and System Log diagnostics reports generated under `C:\workspace\monitor` | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- The scheduled task name must be exactly `MemoryMonitorTask`.
- Ensure all diagnostics files are written to the correct folder: `C:\workspace\monitor`.
