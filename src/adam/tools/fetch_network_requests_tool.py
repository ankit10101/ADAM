from time import sleep
import re
from urllib.parse import unquote_plus
from crewai.tools import tool

from selenium.webdriver.chrome.service import Service as ChromeService
import seleniumwire.webdriver
from seleniumwire.webdriver import ChromeOptions


@tool
def fetch_the_network_requests_on_page_load(
    web_page: str, sleep_time: int, regex_filter_string: str
) -> str:
    """
    Use this tool to fetch/get all the network/HTTP requests to a specific URL on a web page load. It will help you fetch/get all the network/HTTP requests to any particular URL on any web page load.

    It takes in the following parameters:
    * web_page (str): A complete URL of the web page where we need to fetch/get the network/HTTP requests from. The URL should comprise the protocol (HTTP or HTTPS)
    * sleep_time (int): Number of seconds to wait after loading the web page and before fetching/getting the network requests
    * regex_filter_string (str): A regex filter string to filter only the requests to a specific URL

    It returns a string specifying whether the tool ran successfully or encountered an exception. You should stop in either scenario and respond accordingly.
    """
    options = ChromeOptions()

    # Run in headless mode (no GUI)
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = seleniumwire.webdriver.Chrome(
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

        filtered_requests = list(
            filter(
                lambda request: re.search(
                    regex_filter_string, request.url, re.IGNORECASE
                ),
                driver.requests,
            )
        )
        output = ""
        for i, request in enumerate(filtered_requests):
            output += f"{i + 1}. URL: {unquote_plus(request.url)}\n\ta. Method: {request.method}\n\tb. Response Status Code: {request.response.status_code}\n\t"
            if request.method == "GET":
                qsp = request.url.split("?")
                qsp = (
                    unquote_plus(qsp[1])
                    if len(qsp) > 1
                    else "No Query String Parameters"
                )
                output += f"c. Query String Parameters:\n\t\t{qsp}\n\n"
            else:
                body = request.body.decode()
                body = unquote_plus(body) if body else "No Parameters/Empty Body"
                output += f"c. Body:\n\t\t{body}\n\n"

        return f"Congratulations! The tool ran successfully.\n\nTotal network/HTTP requests with regex filter ({regex_filter_string}) are {len(filtered_requests)}. You can see the details of all these requests here: {output}. Stop here and convey accordingly."

    except Exception as e:
        return f"An exception occurred while using the tool!\nHere it is. {e}\n\nStop here and respond with the exception summary."
    finally:
        if driver:
            driver.quit()
