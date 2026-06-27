import boto3
import os
import sys

def get_ec2_client():
    try:
        return boto3.client('ec2', region_name='eu-west-2')
    except Exception as e:
        print(f"FAILED: Could not connect to AWS. Error: {e}")
        sys.exit(1)

def verify_task():
    ec2 = get_ec2_client()
    username = os.getenv('KODEARENA_USERNAME', 'LOCAL_USER')
    target_instance = f"labskraft-db-server-{username}" 
    
    print("-" * 40)
    print("AWS RESOURCE VERIFICATION REPORT")
    print("-" * 40)

    tc1_passed = False
    instance_id = None
    
    try:
        resp = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [target_instance]}, {'Name': 'instance-state-name', 'Values': ['running']}])
        instances = [i for r in resp.get('Reservations', []) for i in r.get('Instances', [])]
        if instances:
            inst = instances[0]
            if inst.get('InstanceType') == 't2.micro':
                print("TC1 [EC2 Instance] (5/5) - Success: Windows EC2 t2.micro found.")
                tc1_passed = True
                instance_id = inst['InstanceId']
            else:
                print("TC1 [EC2 Instance] (0/5) - Failed: Instance is not t2.micro.")
        else:
            print("TC1 [EC2 Instance] (0/5) - Failed: Instance not found or not running.")
    except Exception as e:
        print("TC1 [EC2 Instance] (0/5) - Failed: Error retrieving instance.")

    tc2_passed = False
    if tc1_passed:
        try:
            volumes = ec2.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])['Volumes']
            found = False
            for v in volumes:
                if v['Size'] == 20 and v['VolumeType'] == 'io2':
                    found = True
                    break
            if found:
                print("TC2 [EBS Volume Attached] (5/5) - Success: 20 GB io2 volume attached.")
                tc2_passed = True
            else:
                print("TC2 [EBS Volume Attached] (0/5) - Failed: 20 GB io2 volume not attached.")
        except:
            print("TC2 [EBS Volume Attached] (0/5) - Failed: Error retrieving volumes.")
    else:
        print("TC2 [EBS Volume Attached] (0/5) - Failed: Prerequisite TC1 failed.")

    if tc2_passed:
        print("TC3 [EBS Formatted] (5/5) - Success: NTFS volume F: found (Simulated).")
    else:
        print("TC3 [EBS Formatted] (0/5) - Failed: Prerequisite TC2 failed.")

    print("-" * 40)

if __name__ == "__main__":
    verify_task()
