import string
import random

import requests

BASE_URL = "https://openlibrary.org"

books = {
    "hobbit": "/works/OL31542973W",
    "Lord of the Manor": "/works/OL8028461W",
}

LOGIN_ENDPOINT = "/account/login"
USERNAME = "michaelhasibo@gmail.com"
PASSWORD = "zxcvbn"


# Function to log in and create a session
def login_and_create_session(username, password):
    _session = requests.Session()

    # Log in to Open Library
    login_payload = {
        "username": username,
        "password": password,
        "redirect": "/",
        "debug": "true"
    }

    response = _session.post(BASE_URL + LOGIN_ENDPOINT, data=login_payload)
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
    """Create a new list using the Open Library API."""
    url = f"{BASE_URL}/people/michaelhasibo/lists"
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
    print(f"Response from: {response.json()}")
    print(f"return list id: {response.json()['key'].split('/')[-1]}")
    list_id = response.json()['key'].split('/')[-1]
    return list_id


def add_seeds_to_list(_session, list_id, books):
    """Add seeds to an existing list using the Open Library API."""
    url = f"{BASE_URL}/people/michaelhasibo/lists/{list_id}/seeds"
    headers = {"Content-Type": "application/json"}
    payload = {
        "add": [{"key": seed} for seed in books]
    }
    print(f"payload: {payload}")
    response = _session.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to add seeds to list. Status code: {response.status_code}, Response: {response.text}")


def delete_seeds_from_list(_session, list_id, seeds_to_remove):
    """Delete seeds from an existing list using the Open Library API."""
    url = f"{BASE_URL}/people/michaelhasibo/lists/{list_id}/seeds"
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
    headers = {"content-type": "application/json"}
    list_url = f"{BASE_URL}/people/michaelhasibo/lists/{list_id}/delete.json"
    # Send the DELETE request
    print(f"list_url: {list_url}")
    response = _session.post(list_url, headers=headers)

    if response.status_code == 200:
        print(f"Successfully deleted the list: {list_url}")
        return response.status_code
    else:
        raise Exception(f"Failed to delete list. Status code: {response.status_code}, Response: {response.text}")


def get_user_lists(_session, username):
    """Fetches all the lists created by a user."""
    url = f"{BASE_URL}/people/{username}/lists.json"
    response = _session.get(url)
    print(f"user_lists response: {response.text}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to fetch lists for user {username}. Status code: {response.status_code}, Response: {response.text}")


def get_lists_containing_seed(_session):
    """
    Fetches all the lists containing a specific book seed using a session.

    Parameters:
    session (requests.Session): An active session object
    book_seed (str): The Open Library book identifier (seed)

    Returns:
    dict: A dictionary containing the lists that include the book seed
    """
    # Construct the full URL for the request
    url = f"{BASE_URL}{books['hobbit']}/lists.json"

    response = _session.get(url)
    if response.status_code == 200:
        # Parse and return the JSON response
        return response.json()['entries']
    else:
        raise Exception(f"Failed to fetch lists for book seed {books['hobbit']}. Status code: {response.status_code}")


def get_seeds_of_a_list(_session, list_id):
    """Read a list by its ID using the Open Library API."""
    url = f"{BASE_URL}/people/michaelhasibo/lists/{list_id}.json"
    response = _session.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to read list. Status code: {response.status_code}, Response: {response.text}")


def get_subjects_of_list(_session, list_id, limit=5):
    """Get subjects of a list by its ID using the Open Library API."""
    url = f"{BASE_URL}/people/michaelhasibo/lists/{list_id}/subjects.json?limit={limit}"
    response = _session.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get subjects for list. Status code: {response.status_code}, Response: {response.text}")


def search_lists(_session, query, limit=20, offset=0):
    """Search for lists using the Open Library API."""
    url = f"{BASE_URL}/search/lists.json"
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



# session = login_and_create_session(USERNAME, PASSWORD)
# lists = get_lists_containing_seed(session)
# print(f"list: {list}")
# create_list(session)
