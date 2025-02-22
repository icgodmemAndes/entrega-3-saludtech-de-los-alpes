import os
import json
from google.cloud import storage
from google.oauth2 import service_account
from ..utils_secrets.secrets import SecretManagerUtil
from .exceptions import StorageException

class CloudStorageRepository:
    def __init__(self):
        self.project_id = os.environ.get('GCLOUD_PROJECT')
        self.bucket_name = os.environ.get('GCLOUD_BUCKET')

        if not self.project_id or not self.bucket_name:
            raise StorageException("Missing required environment variables: GCLOUD_PROJECT or GCLOUD_BUCKET")

        self._init_client()

    def _init_client(self):
        try:
            # Get credentials from Secret Manager
            secret_name = "projects/616996447568/secrets/storage-credentials/versions/3"
            credentials_json = SecretManagerUtil.get_secret(secret_name)

            if not credentials_json:
                raise StorageException("Failed to retrieve storage credentials from Secret Manager")

            # Initialize credentials
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(credentials_json)
            )

            # Create storage client
            self.client = storage.Client(
                project=self.project_id,
                credentials=credentials
            )

            # Get bucket
            self.bucket = self.client.bucket(self.bucket_name)

        except Exception as e:
            raise StorageException(f"Failed to initialize storage client: {str(e)}")

    def upload_file(self, source_file_path: str, destination_blob_name: str) -> None:
        """
        Upload a file to Google Cloud Storage

        Args:
            source_file_path (str): Path to the local file to upload
            destination_blob_name (str): Name of the file in Cloud Storage

        Raises:
            StorageException: If upload fails
        """
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_path)
        except Exception as e:
            raise StorageException(f"Failed to upload file: {str(e)}")

    def download_file(self, source_blob_name: str, destination_file_path: str) -> None:
        """
        Download a file from Google Cloud Storage

        Args:
            source_blob_name (str): Name of the file in Cloud Storage
            destination_file_path (str): Path where to save the downloaded file

        Raises:
            StorageException: If download fails
        """
        try:
            blob = self.bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_path)
        except Exception as e:
            raise StorageException(f"Failed to download file: {str(e)}")

    def delete_file(self, blob_name: str) -> None:
        """
        Delete a file from Google Cloud Storage

        Args:
            blob_name (str): Name of the file to delete in Cloud Storage

        Raises:
            StorageException: If deletion fails
        """
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
        except Exception as e:
            raise StorageException(f"Failed to delete file: {str(e)}")

    def list_files(self, prefix: str = None) -> list:
        """
        List files in the bucket

        Args:
            prefix (str, optional): Filter results to files starting with this prefix

        Returns:
            list: List of file names in the bucket

        Raises:
            StorageException: If listing fails
        """
        try:
            blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)
            return [blob.name for blob in blobs]
        except Exception as e:
            raise StorageException(f"Failed to list files: {str(e)}")
