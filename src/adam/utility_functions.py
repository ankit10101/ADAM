from google.oauth2 import service_account
from selenium import webdriver
from typing import Optional


def get_gcp_service_account_credentials(
    service_account_json: str, scopes: Optional[list[str]] = None
) -> service_account.Credentials:
    """
    Loads GCP service account credentials from a JSON file.

    Args:
        service_account_json (str): Path to the service account JSON file.
        scopes (Optional[list[str]]): List of OAuth scopes (optional).

    Returns:
        service_account.Credentials: Authenticated GCP credentials object.
    """
    if scopes is not None:
        return service_account.Credentials.from_service_account_file(
            service_account_json, scopes=scopes
        )
    else:
        return service_account.Credentials.from_service_account_file(
            service_account_json
        )


def get_webdriver_options() -> webdriver.ChromeOptions:
    """
    Configures and returns Chrome WebDriver options for headless, automated browsing.

    Returns:
        webdriver.ChromeOptions: Configured Chrome options for Selenium.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("lang=en")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return options
