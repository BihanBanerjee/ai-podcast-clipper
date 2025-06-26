import boto3

class S3Utils:
    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.bucket_name = "ai-podcast-clipping"

    def download_file(self, s3_key, local_path):
        """Download file from S3"""
        self.s3_client.download_file(self.bucket_name, s3_key, local_path)

    def upload_file(self, local_path, s3_key):
        """Upload file to S3"""
        self.s3_client.upload_file(local_path, self.bucket_name, s3_key)