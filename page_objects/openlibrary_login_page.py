from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class OpenLibraryLoginPage:
    """Page Object Model for the Open Library login page."""

    def __init__(self, driver):
        self.driver = driver
        self.login_url = "https://openlibrary.org/account/login"

    def go_to_login_page(self):
        """Navigate to the Open Library login page."""
        self.driver.get(self.login_url)

    def login(self, username, password):
        """Log in to the Open Library."""
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
