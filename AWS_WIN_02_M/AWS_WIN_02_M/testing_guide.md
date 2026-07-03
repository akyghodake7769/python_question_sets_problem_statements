================================================================================
AWS_WIN_02_M: ec2_windows_monitoring - STUDENT IMPLEMENTATION & TESTING GUIDE
================================================================================

🎯 GOAL: AWS EC2 (Windows Server) Monitoring, Logging & Service Management

This guide details the exact steps a learner must perform for AWS_WIN_02_M.

--------------------------------------------------------------------------------
STEP-BY-STEP IMPLEMENTATION
--------------------------------------------------------------------------------

STEP 1: AWS CONSOLE LOGIN
- Log into AWS Console.
- Ensure you are in the eu-west-2 Region.

STEP 2: CREATE EC2 INSTANCE (PASSES TC1)
- Navigate to EC2 -> "Launch Instance".
- Name: `labskraft-windows-monitor-<your-labskraft-username>` (replace <your-labskraft-username> with your actual username, e.g. labs-kraft-demo106).
- Select Microsoft Windows Server 2022 Base AMI.
- Select t2.micro Instance Type.

STEP 3: INSTALL IIS ROLE & START SERVICE (PASSES TC2)
- Connect via RDP or SSM Session Manager.
- Open PowerShell as Administrator.
- Install the Web Server (IIS) role:
  Install-WindowsFeature -name Web-Server -IncludeManagementTools
- Ensure the W3SVC service is enabled and Running:
  Set-Service -Name W3SVC -StartupType Automatic
  Start-Service -Name W3SVC

STEP 4: AUTOMATE MEMORY MONITORING TASK (PASSES TC3)
- Create the monitor directory:
  New-Item -ItemType Directory -Path "C:\workspace\monitor" -Force
- Write a monitoring script or run a task schedule to append memory logs.
- Create a Scheduled Task named `MemoryMonitorTask` to run every 5 minutes:
  $action = New-ScheduledTaskAction -Execute 'Powershell.exe' -Argument '-NoProfile -WindowStyle Hidden -Command "$date = Get-Date -Format s; $freeMem = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory; \"$date - Free Memory: $freeMem KB\" | Out-File -FilePath C:\workspace\monitor\mem_usage.log -Append -Encoding ascii"'
  $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
  $principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType Service
  Register-ScheduledTask -TaskName "MemoryMonitorTask" -Action $action -Trigger $trigger -Principal $principal -Force

STEP 5: DISK AUDITING, PROCESS LOGGING, EVENT DIAGNOSTICS (PASSES TC4)
- Generate a disk utilization report for the C: drive:
  Get-PSDrive C | Select-Object Name, Used, Free | Out-File -FilePath "C:\workspace\monitor\disk_report.txt" -Encoding ascii -Force
- Generate the top 5 CPU-consuming processes report:
  Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 | Out-File -FilePath "C:\workspace\monitor\cpu_process_report.txt" -Encoding ascii -Force
- Test local TCP connectivity on port 80:
  Test-NetConnection -Port 80 | Out-File -FilePath "C:\workspace\monitor\network_status.txt" -Encoding ascii -Force
- Audit Windows System event logs for the latest 5 error messages:
  Get-EventLog -LogName System -EntryType Error -Newest 5 | Select-Object Message | Out-File -FilePath "C:\workspace\monitor\event_errors.txt" -Encoding ascii -Force

--------------------------------------------------------------------------------
HOW TO VERIFY LOCALLY
--------------------------------------------------------------------------------
- Switch to the student workspace terminal.
- Run local evaluation:
  python student_workspace/run.py
