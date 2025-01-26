import requests
from unittest.mock import Mock

class UserClient:
    def __init__(self, base_url, use_mock=False):
        """
        Initialize the UserClient.

        :param base_url: The base URL of the API (e.g., http://localhost:8000)
        :param use_mock: If True, use mock responses instead of making actual API calls
        """
        self.base_url = base_url
        self.use_mock = use_mock
        if use_mock:
            self._setup_mock()

    def _setup_mock(self):
        """
        Set up mock responses for the client.
        """
        self.mock_post_user = Mock()

        # Mock for successful user creation
        self.mock_post_user.return_value = {
            "status_code": 201,
            "json": lambda: {
                "userId": "12345",
                "username": "mockuser"
            }
        }

    def create_user(self, username):
        """
        Create a new user.

        :param username: The username of the user to create
        :return: Response object (or mock response if use_mock is True)
        """
        url = f"{self.base_url}/users"
        payload = {"username": username}

        if self.use_mock:
            print("Using mock response.")
            return self.mock_post_user(payload)

        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response
