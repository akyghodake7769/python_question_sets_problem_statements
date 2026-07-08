# AWS RDS Lab: Provisioning a Secure RDS MySQL Database (Local Verification)

##  Duration : 90 Min.
## Scenario
You are a Cloud Engineer tasked with setting up a highly secure and cost-efficient MySQL database instance on AWS RDS for a new retail web application. To optimize costs and comply with security audits, the database must use the minimum cost tier, have storage autoscaling disabled, and be completely hidden from the public internet.

## Task Objectives
Perform the following configuration steps inside your AWS environment using the Console or AWS CLI:

### Task 1: RDS DB Instance Creation
- Provision an RDS DB instance named **`retail-mysql-db-<username>`** (where `<username>` is your platform username in lowercase, e.g. `retail-mysql-db-candidate123`) using the **MySQL** engine (compatible version `8.0` - e.g. `8.0.35`).

### Task 2: Instance Configuration
- Configure the instance to use the **`db.t3.micro`** class with **`20` GiB** of Allocated Storage (General Purpose SSD - `gp2` or `gp3`).
- Set **Publicly Accessible** to **No** (Disable public IP assignment).

### Task 3: Default Database Initialization
- Specify the initial database name as **`retaildb`** during setup.

### Task 4: Security Group Configuration
- Associate a Security Group with the RDS instance that explicitly allows inbound TCP traffic on port **`3306`** (standard MySQL port).

### Task 5: Storage Autoscaling Disabling
- Ensure **Storage Autoscaling** is disabled (the maximum storage threshold should not be enabled or set to `20` GiB).

---

## Verification
Run the verification script to check your progress:
`python3 student_workspace/run.py`

---

## Grading Criteria
Your configuration will be evaluated on the following criteria:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | AWS Environment active and validated | 0 Marks |
| **TC2** | Task 1 Completed: DB Instance exists with identifier `retail-mysql-db-<username>` and MySQL 8.0 engine | 4 Marks |
| **TC3** | Task 2 Completed: DB Instance class is `db.t3.micro`, storage is 20 GiB, and public access is disabled | 4 Marks |
| **TC4** | Task 3 Completed: Default database `retaildb` is created inside the instance | 4 Marks |
| **TC5** | Task 4 Completed: Attached Security Group allows inbound TCP traffic on port 3306 | 4 Marks |
| **TC6** | Task 5 Completed: Storage autoscaling is disabled | 4 Marks |

**Total Score: 20 Marks**
