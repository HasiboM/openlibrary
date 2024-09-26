import os
import string
import random

import requests

books = {
    "hobbit": "/works/OL31542973W",
    "Lord of the Manor": "/works/OL8028461W",
}


# Function to log in and create a session
def login_and_create_session(username, password):
    base_url = os.getenv("BASE_URL")
    login_endpoint = base_url + os.getenv("LOGIN_ENDPOINT")

    _session = requests.Session()

    # Log in to Open Library
    login_payload = {
        "username": username,
        "password": password,
        "redirect": "/",
        "debug": "true"
    }

    response = _session.post(login_endpoint, data=login_payload)
    if response.status_code != 200:
        raise Exception(f"Login failed with status code: {response.status_code}")

    return _session


def generate_random_string():
    # Generate a random length between 5 and 10
    length = random.randint(5, 10)
    # Generate a random string of uppercase/lowercase letters of the given length
    random_letters = ''.join(random.choices(string.ascii_letters, k=length))
    return random_letters


def create_list(_session):
    base_url = os.getenv("BASE_URL")
    user_name = os.getenv("USER_ACCOUNT")

    """Create a new list using the Open Library API."""
    url = f"{base_url}/people/{user_name}/lists"
    headers = {"content-type": "application/json"}
    payload = {
        "name": f"automation_list_{generate_random_string()}",
        "description": "Studies of architectural practice, mainly English works",
        "tags": ["Architecture", "18th Century", "Drawings", "Buildings"],
        "seeds": [
            books['hobbit'],
            books['Lord of the Manor']
        ]
    }

    response = _session.post(url, json=payload, headers=headers)
    response.raise_for_status()
    list_id = response.json()['key'].split('/')[-1]
    return list_id


def add_seeds_to_list(_session, list_id, books):
    user_name = os.getenv("USER_ACCOUNT")
    base_url = os.getenv("BASE_URL")
    """Add seeds to an existing list using the Open Library API."""
    url = f"{base_url}/people/{user_name}/lists/{list_id}/seeds"
    headers = {"Content-Type": "application/json"}
    payload = {
        "add": [{"key": seed} for seed in books]
    }
    response = _session.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to add seeds to list. Status code: {response.status_code}, Response: {response.text}")


def delete_seeds_from_list(_session, list_id, seeds_to_remove):
    base_url = os.getenv("BASE_URL")
    user_name = os.getenv("USER_ACCOUNT")
    """Delete seeds from an existing list using the Open Library API."""
    url = f"{base_url}/people/{user_name}/lists/{list_id}/seeds"
    headers = {"Content-Type": "application/json"}
    payload = {
        "remove": [{"key": seed} for seed in seeds_to_remove]
    }

    response = _session.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to delete seeds from list. Status code: {response.status_code}, Response: {response.text}")


def delete_list(_session, list_id):
    """Delete a list by its URL."""
    base_url = os.getenv("BASE_URL")
    user_name = os.getenv("USER_ACCOUNT")
    headers = {"content-type": "application/json"}
    list_url = f"{base_url}/people/{user_name}/lists/{list_id}/delete.json"
    response = _session.post(list_url, headers=headers)

    if response.status_code == 200:
        return response.status_code
    else:
        raise Exception(f"Failed to delete list. Status code: {response.status_code}, Response: {response.text}")


def get_user_lists(_session):
    base_url = os.getenv("BASE_URL")
    user_name = os.getenv("USER_ACCOUNT")
    """Fetches all the lists created by a user."""
    url = f"{base_url}/people/{user_name}/lists.json"
    response = _session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to fetch lists for user {user_name}. Status code: {response.status_code}, Response: {response.text}")


def get_lists_containing_seed(_session):
    """
    Fetches all the lists containing a specific book seed using a session.

    Parameters:
    session (requests.Session): An active session object
    book_seed (str): The Open Library book identifier (seed)

    Returns:
    dict: A dictionary containing the lists that include the book seed
    """
    base_url = os.getenv("BASE_URL")
    # Construct the full URL for the request
    url = f"{base_url}{books['hobbit']}/lists.json"

    response = _session.get(url)
    if response.status_code == 200:
        # Parse and return the JSON response
        return response.json()['entries']
    else:
        raise Exception(f"Failed to fetch lists for book seed {books['hobbit']}. Status code: {response.status_code}")


def get_seeds_of_a_list(_session, list_id):
    base_url = os.getenv("BASE_URL")
    """Read a list by its ID using the Open Library API."""
    url = f"{base_url}/people/michaelhasibo/lists/{list_id}.json"
    response = _session.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to read list. Status code: {response.status_code}, Response: {response.text}")


def get_subjects_of_list(_session, list_id, limit=5):
    base_url = os.getenv("BASE_URL")
    user_name = os.getenv("USER_ACCOUNT")
    """Get subjects of a list by its ID using the Open Library API."""
    url = f"{base_url}/people/{user_name}/lists/{list_id}/subjects.json?limit={limit}"
    response = _session.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get subjects for list. Status code: {response.status_code}, Response: {response.text}")


def search_lists(_session, query, limit=20, offset=0):
    base_url = os.getenv("BASE_URL")
    """Search for lists using the Open Library API."""
    url = f"{base_url}/search/lists.json"
    params = {
        "q": query,
        "limit": limit,
        "offset": offset
    }

    response = _session.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to search lists. Status code: {response.status_code}, Response: {response.text}")

