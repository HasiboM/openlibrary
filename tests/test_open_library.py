import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.openlibrary_list_page import OpenLibraryPage
from src.openlibrary_login_page import OpenLibraryLoginPage

API_KEY = "your_api_key"  # Replace with your Open Library API key
USERNAME = "michaelhasibo@gmail.com"
PASSWORD = "zxcvbn"


@pytest.fixture
def driver():
    """Selenium WebDriver fixture."""
    # Get the environment variable
    environment = os.getenv('ENVIRONMENT', 'local')  # Default to 'local'

    if environment == 'production':
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',  # Connect to Selenium service
            options=chrome_options
        )
    else:
        driver = webdriver.Chrome()  # Use local Chrome for development
    yield driver
    driver.quit()


def test_create_and_verify_list(driver):
    """Test: Log in, create a list via API, verify it in the UI, and delete it."""
    # 0. login with backend -> get cookie with fixure
    # 0b. delete list "xyz" in order for cicd to work
    # 1. create list with backend
    # 2. login with selenium, test list exists
    # 3. delete with backend

    # Step 1: Log in to Open Library via the UI
    login_page = OpenLibraryLoginPage(driver)
    login_page.go_to_login_page()
    login_page.login(USERNAME, PASSWORD)

    # Step 2: Create a list via the API
    list_name = "Test Automation List"
    # list_data = create_list(API_KEY, list_name)
    # list_id = list_data["id"]

    # Step 3: Verify the list exists in the UI
    open_library_page = OpenLibraryPage(driver)
    open_library_page.go_to_list_page()
    assert open_library_page.verify_list_exists(list_name), "List not found in UI"

    # Step 4: Delete the list via the API
    # delete_status = delete_list(API_KEY, list_id)
    # assert delete_status == 204, "Failed to delete the list"
