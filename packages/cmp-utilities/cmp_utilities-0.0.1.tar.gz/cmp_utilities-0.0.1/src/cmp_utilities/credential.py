import os
from google.auth import default
from google.auth.transport.requests import Request


class GoogleCredentials:
    def __init__(
            self, scopes=None, api_quota_project=None, credential_file=None
    ) -> None:
        if scopes is not None:
            self.scopes = scopes
        else:
            self.scopes = [
                "https://www.googleapis.com/auth/cloud-platform",
            ]
        if credential_file is not None:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_file
        self.api_quota_project = api_quota_project
        self.__credentials = None
        self.__auth_token = None
        self.__auth_header = None

    def get_default_credentials(self):
        self.__credentials, project = default(
            quota_project_id=self.api_quota_project, scopes=self.scopes
        )
        return self.__credentials

    def get_auth_header(self):
        self.__credentials.refresh(Request())
        self.__auth_token = self.__credentials.token
        self.__auth_header = {"Authorization": f"Bearer {self.__auth_token}"}
        return self.__auth_header, self.__auth_token
