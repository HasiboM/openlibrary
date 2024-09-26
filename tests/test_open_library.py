import os
from src.api.api_interaction import create_list, login_and_create_session, delete_list, get_user_lists
from src.openlibrary_list_page import OpenLibraryPage
from src.openlibrary_login_page import OpenLibraryLoginPage


def test_create_and_verify_list(driver, setup_session):
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    """Test: Log in, create a list via API, verify it in the UI, and delete it."""

    # Create a list via the API
    login_and_create_session(username, password)
    list_id = create_list(setup_session)
    assert list_id is not None, "Failed to create a list: list_id is None"

    # Step 1: Log in to Open Library via the UI
    login_page = OpenLibraryLoginPage(driver)
    login_page.go_to_login_page()
    login_page.login(username, password)

    # Verify the list exists in the UI
    open_library_page = OpenLibraryPage(driver)
    open_library_page.go_to_list_page()
    assert open_library_page.verify_list_id_exists(list_id), "List not found in UI"

    # Delete the list via the API
    delete_status = delete_list(setup_session, list_id)
    assert delete_status == 200, "Failed to delete the list"
