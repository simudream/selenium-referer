# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def create_driver(proxy=None):
    """
    Driver convenience method.
    :param proxy:
    :return:
    """
    driver = webdriver.Firefox(proxy=proxy)
    driver.delete_all_cookies()
    return driver


def close_driver(driver):
    """
    Driver convenience method.
    :param driver: webdriver
    """
    assert isinstance(driver, webdriver.Firefox)
    driver.close()


def read_cookies(driver):
    """
    Get all cookies.
    :param driver: webdriver
    :return: set of dicts
    """
    assert isinstance(driver, webdriver.Firefox)

    cookies = driver.get_cookies()

    print('\nCookies:')
    for cookie in cookies:
        print(cookie)
    return cookies


def navigate_and_read_cookies(driver, url, params=None):
    """
    Navigate to the page and wait for it being loaded.
    When loaded, read and return cookies.
    :param driver: webdriver
    :param url: url
    :param params: dict
    :return: set of dicts
    """
    navigate_and_wait(driver, url, params)
    return read_cookies(driver)


def navigate_and_wait(driver, url, params=None):
    """
    Navigate to the page and wait for it being loaded.
    :param driver: webdriver
    :param url: url
    :param params: dict
    """
    assert isinstance(driver, webdriver.Firefox)

    url = url_with_params(url, params)

    print('\nNavigating to page:')
    print(url)

    driver.get(url)

    wait_page_load(driver)
    print('Page loaded.')


def wait_page_load(driver):
    """
    Wait for page being loaded.
    :param driver: webdriver
    """
    assert isinstance(driver, webdriver.Firefox)

    WebDriverWait(driver, 10) \
        .until(lambda d: d.execute_script(
            'return document.readyState') == 'complete')


def url_with_params(url, params=None):
    """
    Create URL with param1=value1&param2=value2...
    :param url: url
    :param params: dict
    :return: string
    """
    if params and len(params) > 0:
        ps = '&'.join("{0}={1}".format(k, v) for k, v in params.items())
        return '{0}{1}{2}'.format(url, '?', ps)

    return url
