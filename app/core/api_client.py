# api_client.py

import requests


class ApiClient:
    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        """
        Initialize the API client with a base URL.

        :param base_url: The base URL of the API (default is jsonplaceholder).
        """
        self.base_url = base_url

    def get(self, endpoint, params=None):
        """
        Send a GET request to the specified API endpoint.

        :param endpoint: The path of the API endpoint (excluding the base URL).
        :param params: Optional dictionary of query parameters.
        :return: Returns the response JSON data or None if the request fails.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx status codes)
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
