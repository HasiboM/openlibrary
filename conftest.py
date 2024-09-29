import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.api.api_interaction import login_and_create_session
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env_config():
    # Get the environment variable
    environment = os.getenv('ENVIRONMENT', 'local')  # Default to 'local'

    if environment == 'production':
        load_dotenv('config/.env.production')
    else:
        load_dotenv('config/.env.local')


@pytest.fixture(scope='session', autouse=True)
def setup_session():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    """Setup code that runs before all tests."""
    print("\nSetting up session resources...")
    session = login_and_create_session(username, password)
    yield session
    print("\nTearing down session resources...")


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
