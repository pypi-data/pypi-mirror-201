from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from django.conf import settings

def get_webdriver():
    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.headless = True
    path = settings.BROWSER_PATH
    driver = webdriver.Firefox(firefox_binary=FirefoxBinary(path)
                               , options=firefoxOptions
                               )
    # chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # chromeOptions.add_argument("--no-sandbox")
    # chromeOptions.add_argument("--disable-setuid-sandbox")
    # chromeOptions.add_argument("--disable-dev-shm-usage")
    # chromeOptions.add_argument("--disable-extensions")
    # chromeOptions.add_argument("--disable-gpu")
    # chromeOptions.add_argument("start-maximized")
    # chromeOptions.add_argument("disable-infobars")
    # chromeOptions.add_argument("--headless")
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
    #                           options=chromeOptions)
    return driver
