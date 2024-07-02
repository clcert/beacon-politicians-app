# selenium
from selenium import webdriver
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def chromium_driver(options):
    try: 
        logger.info('Attempting to run chromium driver...')
        options.binary_location = '/usr/bin/chromium-browser'
        driver = webdriver.Chrome(options=options)
        logger.info('Chromium driver successfully loaded.')
    except Exception as e:
        logger.error('Failed to run chromium web driver.')
        driver = None
    finally:
        return driver


def google_chrome_driver(options):
    try: 
        logger.info('Attempting to run google chrome driver...')
        options.binary_location = '/usr/bin/google-chrome-stable'
        driver = webdriver.Chrome(options=options)
        logger.info('Google chrome driver successfully loaded.')
    except Exception as e:
        logger.error('Failed to run google chrome web driver.')
        driver = None
    finally:
        return driver


def get_driver():
    """
    Function that returns a driver to be used in the parsing process.
    :return: Returns a driver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless") # We don't need a GUI

    driver = chromium_driver(options)
    if driver:
        return driver
    else:
        return google_chrome_driver(options)