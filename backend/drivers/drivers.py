# selenium
from selenium import webdriver

def chromium_driver(options):
    try: 
        print('Attempting to run chromium driver...')
        options.binary_location = '/usr/bin/chromium-browser'
        driver = webdriver.Chrome('chromedriver', options=options)
    except Exception as e:
        print('Error: Failed to run chromium chrome driver.')
        driver = None
    finally:
        return driver


def google_chrome_driver(options):
    try: 
        print('Attempting to run google chrome driver...')
        options.binary_location = '/usr/bin/google-chrome-stable'
        driver = webdriver.Chrome('chromedriver', options=options)
    except Exception as e:
        print('Error: Failed to run chromium chrome driver.')
        driver = None
    finally:
        return driver