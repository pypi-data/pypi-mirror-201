import json
from google.cloud import secretmanager


class GoogleSecretManager:
    def __init__(self, credentials) -> None:
        self.__credentials = credentials
        self.__client = secretmanager.SecretManagerServiceClient(credentials=self.__credentials)

    def get_secret(self, secret_id):
        response = self.__client.access_secret_version(request={"name": secret_id})
        payload = response.payload.data.decode("UTF-8")
        return payload

    def get_secret_json(self, secret_id):
        response = self.__client.access_secret_version(request={"name": secret_id})
        payload = response.payload.data.decode("UTF-8").replace("\'", "\"")
        return json.loads(payload)
