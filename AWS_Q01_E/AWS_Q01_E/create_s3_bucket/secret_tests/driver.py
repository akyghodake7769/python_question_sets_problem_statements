import boto3
import os
import sys

# 1. Setup AWS Client (Credentials are picked up automatically from Environment)
def get_s3_client():
    try:
        return boto3.client('s3')
    except Exception as e:
        print(f"FAILED: Could not connect to AWS. Error: {e}")
        sys.exit(1)

def verify_task():
    s3 = get_s3_client()
    username = os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')
    import sys
    exam_code = sys.argv[3] if len(sys.argv) > 3 else 'UNKNOWN'
    import sys
    exam_code = sys.argv[3] if len(sys.argv) > 3 else 'UNKNOWN'
    target_bucket = f"{username}-{exam_code}" 
    
    print("-" * 40)
    print("AWS RESOURCE VERIFICATION REPORT")
    print("-" * 40)

    # --- TEST CASE 1: BUCKET EXISTENCE ---
    try:
        s3.head_bucket(Bucket=target_bucket)
        print("TC1 [Bucket Creation] (5/5) - Success: Bucket found in AWS.")
    except:
        print("TC1 [Bucket Creation] (0/5) - Failed: Bucket not found.")
        return # Stop if bucket doesn't exist

    # --- TEST CASE 2: PUBLIC ACCESS BLOCK ---
    try:
        pab = s3.get_public_access_block(Bucket=target_bucket)
        config = pab.get('PublicAccessBlockConfiguration', {})
        if config.get('BlockPublicAcls') and config.get('BlockPublicPolicy'):
            print("TC2 [Public Access Blocked] (5/5) - Success: Security configured.")
        else:
            print("TC2 [Public Access Blocked] (0/5) - Failed: Public access is still allowed.")
    except:
        print("TC2 [Public Access Blocked] (0/5) - Failed: Security settings not found.")

    # --- TEST CASE 3: REGION CHECK ---
    try:
        location = s3.get_bucket_location(Bucket=target_bucket)
        region = location.get('LocationConstraint') or 'us-east-1'
        if region in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
            print(f"TC3 [Region Check] (5/5) - Success: Correct region '{region}' used.")
        else:
            print(f"TC3 [Region Check] (0/5) - Failed: Found in {region}.")
    except:
        print("TC3 [Region Check] (0/5) - Failed: Error retrieving location.")

    print("-" * 40)

if __name__ == "__main__":
    verify_task()

    print("-" * 40)
    print("--- AUTOMATED TEARDOWN ---")
    try:
        if 's3' in locals() and 'target_bucket' in locals():
            objects = s3.list_objects_v2(Bucket=target_bucket)
            if 'Contents' in objects:
                for obj in objects['Contents']:
                    s3.delete_object(Bucket=target_bucket, Key=obj['Key'])
            s3.delete_bucket(Bucket=target_bucket)
            print("Success: S3 Bucket cleanly deleted for the next run.")
        if 'ec2' in locals() and 'target_instance' in locals():
            # Assume instance teardown is more complex, just placeholder
            pass
    except Exception as e:
        print(f"Cleanup Warning (Normal if resource didn't exist): {e}")
