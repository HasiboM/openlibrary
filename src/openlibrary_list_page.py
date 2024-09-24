from selenium.webdriver.common.by import By


class OpenLibraryPage:
    """Page Object Model for the Open Library Lists page."""

    def __init__(self, driver):
        self.driver = driver
        self.list_page_url = "https://openlibrary.org/account/lists"

    def go_to_list_page(self):
        """Navigate to the user's Lists page."""
        self.driver.get(self.list_page_url)

    def verify_list_exists(self, list_name):
        """Check if the specified list exists in the UI."""
        return self.driver.find_element(By.XPATH, f"//a[text()='{list_name}']").is_displayed()
