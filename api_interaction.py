import requests

BASE_URL = "https://openlibrary.org"


def create_list(api_key, list_name):
    """Create a new list using the Open Library API."""
    url = f"{BASE_URL}/account/lists"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"name": list_name, "description": "Test List created via API"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()  # Return the list details


def delete_list(api_key, list_id):
    """Delete an existing list using the Open Library API."""
    url = f"{BASE_URL}/account/lists/{list_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code  # Return the status code (204 means success)
