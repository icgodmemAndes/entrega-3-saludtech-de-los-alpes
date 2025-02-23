from google.cloud import secretmanager
from typing import Optional

class SecretManagerUtil:
    @staticmethod
    def get_secret(secret_name: str) -> Optional[str]:
        try:
            client = secretmanager.SecretManagerServiceClient()
            response = client.access_secret_version(request={"name": secret_name})
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            # You might want to create a custom exception
            raise Exception(f"Error retrieving secret: {str(e)}")
