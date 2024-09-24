import pytest
from selenium import webdriver
from api_interaction import create_list, delete_list
from page_objects.openlibrary_login_page import OpenLibraryLoginPage
from page_objects.openlibrary_list_page import OpenLibraryPage

API_KEY = "your_api_key"  # Replace with your Open Library API key
USERNAME = "mishahasibo@icloud.com"
PASSWORD = "Evaliam.413"


@pytest.fixture
def driver():
    """Selenium WebDriver fixture."""
    driver = webdriver.Chrome()  # Make sure you have the correct browser driver installed
    yield driver
    driver.quit()


def test_create_and_verify_list(driver):
    """Test: Log in, create a list via API, verify it in the UI, and delete it."""

    # Step 1: Log in to Open Library via the UI
    login_page = OpenLibraryLoginPage(driver)
    login_page.go_to_login_page()
    login_page.login(USERNAME, PASSWORD)

    # Step 2: Create a list via the API
    list_name = "Test Automation List"
    list_data = create_list(API_KEY, list_name)
    list_id = list_data["id"]

    # Step 3: Verify the list exists in the UI
    open_library_page = OpenLibraryPage(driver)
    open_library_page.go_to_list_page()
    assert open_library_page.verify_list_exists(list_name), "List not found in UI"

    # Step 4: Delete the list via the API
    delete_status = delete_list(API_KEY, list_id)
    assert delete_status == 204, "Failed to delete the list"
