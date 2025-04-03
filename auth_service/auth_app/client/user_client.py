from unittest.mock import Mock

import requests

from auth_app.settings import CA_CERT


class MockResponse:
    """
    A mock response object to mimic requests.Response.
    """

    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


class UserClient:
    def __init__(self, base_url, use_mock=False, mock_search_data=None):
        """
        Initialize the UserClient.

        :param base_url: The base URL of the API (e.g., http://localhost:8000)
        :param use_mock: If True, use mock responses instead of making actual API calls
        """
        self.base_url = base_url
        self.use_mock = use_mock
        self.mock_search_data = mock_search_data
        if use_mock:
            self._setup_mock()

    def _setup_mock(self):
        """
        Set up mock responses for the client.
        """
        self.mock_post_user = Mock()
        self.mock_get_user = Mock()

        # Mock for successful user creation
        self.mock_post_user.return_value = MockResponse(
            json_data={"userId": "12345", "username": "mockuser"},
            status_code=201,
        )

        if self.mock_search_data:
            self.mock_get_user.return_value = MockResponse(
                json_data=self.mock_search_data,
                status_code=200,
            )
        else:
            # Default mock for search_users
            self.mock_get_user.return_value = MockResponse(
                json_data=[{"error": "User not found."}],
                status_code=404,
            )

    def create_user(self, username, api_key: str):
        """
        Create a new user.

        :param username: The username of the user to create
        :return: Response object (or mock response if use_mock is True)
        """
        url = f"{self.base_url}/users"
        payload = {"username": username}
        headers = {"x-api-key": api_key}

        if self.use_mock:
            print("Using mock response.")
            return self.mock_post_user(payload)

        response = requests.post(url, json=payload, headers=headers, verify=CA_CERT)
        response.raise_for_status()
        return response

    def search_users(self, query):
        """
        Search for users by username or userid.

        :param query: A dictionary with a single key ('username' or 'userid') and its value
        :return: Response object (or mock response if use_mock is True)
        """
        url = f"{self.base_url}/users"

        if not isinstance(query, dict) or len(query) != 1:
            raise ValueError(
                "Query must be a dictionary with exactly one key: 'username' or 'userid'."
            )

        if self.use_mock:
            print("Using mock response for search_users.")
            return self.mock_get_user(query)

        response = requests.get(url, params=query, verify=CA_CERT)
        return response
