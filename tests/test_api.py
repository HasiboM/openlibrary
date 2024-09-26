
from src.api.api_interaction import (
    create_list,
    get_user_lists,
    delete_list,
    add_seeds_to_list,
    delete_seeds_from_list,
    get_seeds_of_a_list,
    search_lists,
    get_subjects_of_list,
    get_lists_containing_seed
)

USERNAME = "michaelhasibo@gmail.com"
PASSWORD = "zxcvbn"
USER = "michaelhasibo"
BOOKS = {
    "hobbit": "/works/OL31542973W",
    "Lord of the Manor": "/works/OL8028461W"
}


def test_create_list(setup_session):
    """Test: Create a new list via the API."""
    list_id = create_list(setup_session)
    assert list_id is not None, "Failed to create a list: list_id is None"
    delete_list(setup_session, list_id)


def test_get_user_lists(setup_session):
    """Test: Fetch user lists."""
    lists = get_user_lists(setup_session, USER)
    # print(f"user_lists: {json.dumps(lists)}")
    assert isinstance(lists, dict), "Response should be a dictionary"


def test_add_seeds_to_list(setup_session):
    """Test: Add seeds to the created list."""
    list_id = create_list(setup_session)
    seeds_to_add = ["/books/OL25083437M"]
    response = add_seeds_to_list(setup_session, list_id, seeds_to_add)
    assert response, "Failed to add seeds to the list"
    delete_list(setup_session, list_id)


def test_get_seeds_of_a_list(setup_session):
    """Test: Get seeds of a list."""
    list_id = create_list(setup_session)
    seeds_to_add = ["/books/OL25083437M"]
    response = add_seeds_to_list(setup_session, list_id, seeds_to_add)
    assert response, "Failed to add seeds to the list"
    seeds_data = get_seeds_of_a_list(setup_session, list_id)
    assert isinstance(seeds_data, dict), "Response should be a dictionary"
    assert seeds_data.get('seed_count', None) == 3, "Seeds count mismatch"
    delete_list(setup_session, list_id)


def test_delete_seeds_from_list(setup_session):
    list_id = create_list(setup_session)
    seeds_to_add = ["/books/OL25083437M"]
    response = add_seeds_to_list(setup_session, list_id, seeds_to_add)
    assert response, "Failed to add seeds to the list"
    delete_status = delete_seeds_from_list(setup_session, list_id, seeds_to_add)
    assert delete_status, "Failed to delete seeds from the list"
    delete_list(setup_session, list_id)


def test_search_lists(setup_session):
    """Test: Search for lists."""
    query = "automation"
    response = search_lists(setup_session, query)
    assert isinstance(response, dict), "Response should be a dictionary"


def test_get_subjects_of_list(setup_session):
    """Test: Get subjects of a list."""
    list_id = create_list(setup_session)
    subjects = get_subjects_of_list(setup_session, list_id)
    assert isinstance(subjects, dict), "Response should be a dictionary"
    delete_list(setup_session, list_id)


def test_get_lists_containing_seed(setup_session):
    """Test: Get lists containing a specific book seed."""
    response = get_lists_containing_seed(setup_session)
    assert isinstance(response, list), "Response should be a list"


def test_delete_list(setup_session):
    list_id = create_list(setup_session)
    assert list_id is not None, "Failed to create a list: list_id is None"
    delete_list(setup_session, list_id)