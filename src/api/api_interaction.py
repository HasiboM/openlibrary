import requests

BASE_URL = "https://openlibrary.org"

books = {
    "hobbit": "/works/OL31542973W",
    "Lord of the Manor": "/works/OL8028461W"
}

LOGIN_ENDPOINT = "/account/login"


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

    # Check if login is successful
    if response.status_code != 200:
        raise Exception(f"Login failed with status code: {response.status_code}")

    return _session


def create_list(_session):
    """Create a new list using the Open Library API."""
    url = f"{BASE_URL}/people/michaelhasibo/lists"
    headers = {"content-type": "application/json"}
    payload = {
        "name": f"automation_list",
        "description": "Studies of architectural practice, mainly English works",
        "tags": ["Architecture", "18th Century", "Drawings", "Buildings"],
        "seeds": [
            books['hobbit'],
            books['Lord of the Manor']
        ]
    }

    response = _session.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return BASE_URL + response.json()['key']


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

    # Send the GET request using the session object
    response = _session.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse and return the JSON response
        return response.json()['entries']
    else:
        # Handle errors and raise an exception if needed
        raise Exception(f"Failed to fetch lists for book seed {book_seed}. Status code: {response.status_code}")



def delete_list(api_key, list_id):
    """Delete an existing list using the Open Library API."""
    url = f"{BASE_URL}/account/lists/{list_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code  # Return the status code (204 means success)

#lists = get_lists_containing_seed(session)
#create_list(session)