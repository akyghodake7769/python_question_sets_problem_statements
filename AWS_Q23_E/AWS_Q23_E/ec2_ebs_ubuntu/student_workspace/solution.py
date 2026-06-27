import boto3
from botocore.exceptions import ClientError

class EC2Manager:
    def __init__(self):
        # Initializes EC2 client using default AWS credential resolution (configured locally)
        self.ec2 = boto3.client('ec2', region_name='eu-west-2')

    def provision(self, instance_name):
        try:
            print(f"[INFO] Provisioning Ubuntu EC2 instance: {instance_name}...")
            # 1. Launch EC2 instance (Ubuntu 22.04 LTS AMI in eu-west-2 region)
            # Standard Ubuntu 22.04 LTS AMI for eu-west-2 (London) is ami-0b9932f4918a00c4f
            response = self.ec2.run_instances(
                ImageId='ami-0b9932f4918a00c4f', 
                InstanceType='t2.micro',
                MinCount=1,
                MaxCount=1,
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': instance_name}]
                }]
            )
            instance = response['Instances'][0]
            instance_id = instance['InstanceId']
            availability_zone = instance['Placement']['AvailabilityZone']
            
            print(f"[SUCCESS] Instance launched: {instance_id} in {availability_zone}. Waiting for instance to run...")
            
            # Wait for instance to enter running state so we can attach volume
            waiter = self.ec2.get_waiter('instance_running')
            waiter.wait(InstanceIds=[instance_id])
            
            # 2. Create EBS volume (10 GB, gp3 type, in the same AZ)
            print("[INFO] Creating 10 GB gp3 EBS volume...")
            vol_resp = self.ec2.create_volume(
                AvailabilityZone=availability_zone,
                Size=10,
                VolumeType='gp3',
                TagSpecifications=[{
                    'ResourceType': 'volume',
                    'Tags': [{'Key': 'Name', 'Value': f"{instance_name}-volume"}]
                }]
            )
            volume_id = vol_resp['VolumeId']
            
            # Wait for volume to become available
            vol_waiter = self.ec2.get_waiter('volume_available')
            vol_waiter.wait(VolumeIds=[volume_id])
            print(f"[SUCCESS] EBS Volume created: {volume_id}")
            
            # 3. Attach volume to EC2 instance
            print(f"[INFO] Attaching volume {volume_id} to instance {instance_id}...")
            self.ec2.attach_volume(
                Device='/dev/sdf',
                InstanceId=instance_id,
                VolumeId=volume_id
            )
            
            # Wait for volume to show as attached
            print(f"[SUCCESS] Infrastructure provisioned successfully!")
            return instance_id, volume_id
            
        except ClientError as e:
            print(f"[ERROR] AWS Provisioning failed: {e}")
            raise e
