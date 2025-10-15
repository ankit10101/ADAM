from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from time import sleep

from crewai.tools import tool

from selenium.webdriver.chrome.options import Options


@tool
def run_a_js_code_on_a_web_page(web_page: str, sleep_time: int, js_code: str) -> str:
    """
    Use this tool to run/execute a JS code on a web page. It will help you run/execute any JS code on any web page.

    It takes in the following parameters:
    * web_page (str): A complete URL of the web page where we need to run the JS code. The URL should comprise the protocol (HTTP or HTTPS)
    * sleep_time (int): Number of seconds to wait after loading the web page and before executing the JS code
    * js_code (str): The JS code to run/execute on the web page. Ensure that the code returns a value via the "return" statement. Otherwise, no output will get captured via Selenium.

    It returns a string specifying whether the tool ran successfully or encountered an exception. You should stop in either scenario and respond accordingly.
    """

    options = Options()

    # Run in headless mode (no GUI)
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=ChromeService("/usr/bin/chromedriver"), options=options
    )

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
        """
        },
    )
    driver.set_page_load_timeout(60)

    try:
        driver.get(web_page)
        sleep(sleep_time)
        return f"Congratulations! The tool ran successfully.\n\nHere is the JS code output:\n{driver.execute_script(js_code)}"
    except Exception as e:
        return f"An exception occurred while using the tool!\nHere it is. {e}\n\nStop here and respond with the exception summary."
    finally:
        driver.quit()
