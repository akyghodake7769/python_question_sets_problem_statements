# DevOps Lab: Automated S3 Bucket Provisioning

## Scenario
As a DevOps engineer at KodeArena, you are tasked with automating the provisioning of infrastructure components. Your first task is to create a robust Python script that provisions an AWS S3 bucket with specific security and availability configurations.

## Objectives
Implement the `S3Manager` class in `solution.py` with the following requirements:

### 1. Create Logging Bucket
Implement `create_logging_bucket(bucket_name: str)`:
- **Provisioning:** Create an S3 bucket with the provided name.
- **Region:** Use `us-east-1` (North Virginia).
- **Versioning:** Enable versioning on the bucket to ensure object history is maintained.
- **Public Access Block:** Implement a strict "Block All Public Access" configuration (BlockPublicAcls, IgnorePublicAcls, BlockPublicPolicy, RestrictPublicBuckets).

### 2. Verify Status
Implement `get_bucket_status(bucket_name: str) -> dict`:
- Return a dictionary with the following keys:
    - `"Exists"`: Boolean (True if bucket exists)
    - `"VersioningEnabled"`: Boolean (True if versioning is 'Enabled')
    - `"PublicAccessBlocked"`: Boolean (True if all 4 block settings are enabled)

## Constraints
- Use the `boto3` library.
- Do not hardcode credentials.
- Handle potential errors (e.g., bucket name already exists) gracefully.

## Grading Criteria
- **Bucket Creation:** 5 Marks
- **Versioning Configuration:** 5 Marks
- **Public Access Block Configuration:** 5 Marks
- **Status Reporting Logic:** 5 Marks
- **Total:** 20 Marks
