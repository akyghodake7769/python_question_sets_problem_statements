import boto3
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self):
        """Initialize S3 client for us-east-1"""
        self.s3 = boto3.client('s3', region_name='us-east-1')

    def create_logging_bucket(self, bucket_name):
        """
        Creates an S3 bucket with Versioning and Public Access Block enabled.
        """
        try:
            # 1. Create Bucket
            self.s3.create_bucket(Bucket=bucket_name)
            
            # 2. Enable Versioning
            self.s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
            
            # 3. Block Public Access
            self.s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            return True
        except ClientError as e:
            print(f"Error: {e}")
            return False

    def get_bucket_status(self, bucket_name):
        """
        Returns the configuration status of the bucket.
        """
        status = {
            "Exists": False,
            "VersioningEnabled": False,
            "PublicAccessBlocked": False
        }
        try:
            # Check Existence
            self.s3.head_bucket(Bucket=bucket_name)
            status["Exists"] = True
            
            # Check Versioning
            ver = self.s3.get_bucket_versioning(Bucket=bucket_name)
            status["VersioningEnabled"] = ver.get('Status') == 'Enabled'
            
            # Check Public Access Block
            pab = self.s3.get_public_access_block(Bucket=bucket_name)
            conf = pab.get('PublicAccessBlockConfiguration', {})
            status["PublicAccessBlocked"] = all([
                conf.get('BlockPublicAcls'),
                conf.get('IgnorePublicAcls'),
                conf.get('BlockPublicPolicy'),
                conf.get('RestrictPublicBuckets')
            ])
            
        except ClientError:
            pass
            
        return status
