# example_usage.py
from seedwork.infrastructure.storage.repositories import CloudStorageRepository
from seedwork.infrastructure.storage.exceptions import StorageException

def main():
    try:
        # Initialize the storage repository
        storage_repo = CloudStorageRepository()

        # Example operations
        storage_repo.upload_file('local_file.txt', 'remote_file.txt')
        storage_repo.download_file('remote_file.txt', 'downloaded_file.txt')

        # List files
        files = storage_repo.list_files()
        print("Files in bucket:", files)

    except StorageException as e:
        print(f"Storage operation failed: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
