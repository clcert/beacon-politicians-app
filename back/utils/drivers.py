# selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_driver():
    firefox_driver = get_firefox_driver()
    if firefox_driver:
        return firefox_driver
    else:
        return get_chrome_driver()


def get_firefox_driver():
    try:
        logger.info('attempting to run firefox driver...')
        options = Options()
        firefox_profile = FirefoxProfile()
        options.profile = firefox_profile
        options.add_argument("--headless") # We don't need a GUI

        options.binary_location = '/usr/bin/firefox'
        driver = webdriver.Firefox(options=options)
        logger.info('Firefox driver successfully loaded.')
    except Exception as e:
        logger.error(f'failed to run firefox web driver:\n{e}')
        driver = None
    finally:
        return driver


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless") # We don't need a GUI

    driver = chromium_driver(options)
    if driver:
        return driver
    else:
        return google_chrome_driver(options)


def get_chromium_driver(options):
    try: 
        logger.info('attempting to run Chromium driver...')
        options.binary_location = '/usr/bin/chromium-browser'
        driver = webdriver.Chrome(options=options)
        logger.info('Chromium driver successfully loaded.')
    except Exception as e:
        logger.error(f'failed to run Chromium web driver:\n{e}')
        driver = None
    finally:
        return driver


def get_google_chrome_driver(options):
    try: 
        logger.info('attempting to run Google Chrome driver...')
        options.binary_location = '/usr/bin/google-chrome-stable'
        driver = webdriver.Chrome(options=options)
        logger.info('Google Chrome driver successfully loaded.')
    except Exception as e:
        logger.error(f'failed to run Google Chrome web driver:\n{e}')
        driver = None
    finally:
        return driver