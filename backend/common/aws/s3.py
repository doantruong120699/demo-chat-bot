from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from django.conf import settings
import logging


class S3Storage:
    def __init__(self):
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        self.logger = logging.getLogger(__name__)

    def upload_file(self, content: BytesIO, file_path: str, file_name: str):
        """Upload a file to an S3 bucket"""
        path = file_path + "/" + file_name
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=path,
            Body=content,
        )
        return path

    def download_file(self, object_name, file_name=None):
        """Download a file from an S3 bucket"""
        if file_name is None:
            file_name = object_name
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_name)
            print(
                f"File {object_name} downloaded from {self.bucket_name} to {file_name}"
            )
        except ClientError as e:
            print(f"Error occurred: {e}")

    def delete_file(self, object_name):
        """Delete a file from an S3 bucket"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error occurred: {e}")

    def list_files(self):
        """List files in an S3 bucket"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if "Contents" in response:
                for obj in response["Contents"]:
                    print(obj["Key"])
            else:
                print("No files found in the bucket.")
        except ClientError as e:
            print(f"Error occurred: {e}")

    def get_object(self, object_name):
        """Get an object from an S3 bucket"""
        return self.s3_client.get_object(Bucket=self.bucket_name, Key=object_name)
