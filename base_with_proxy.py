# -*- coding: utf-8 -*-
import os
import sys
import pexpect
import unittest

from selenium.webdriver.common.proxy import Proxy, ProxyType

import utils


class ProxyBase(unittest.TestCase):
    """
    We have to use our own proxy server to set a Referer header, because Selenium does not
    allow to interfere with request headers.

    This is the base class. Change `proxy_referer` to set different referers.
    """

    base_url = 'http://www.facebook.com'

    proxy_server = None

    proxy_address = '127.0.0.1'
    proxy_port = 8888
    proxy_referer = None
    proxy_command = '{0} {1} --referer {2} --port {3}'

    def setUp(self):
        """
        Create the environment.
        """
        print('\nSetting up.')
        self.start_proxy()
        self.driver = utils.create_driver(proxy=self.proxy())

    def tearDown(self):
        """
        Cleanup the environment.
        """
        print('\nTearing down.')
        utils.close_driver(self.driver)
        self.stop_proxy()

    def proxy(self):
        """
        Create proxy settings for our Firefox profile.
        :return: Proxy
        """
        proxy_url = '{0}:{1}'.format(self.proxy_address, self.proxy_port)

        p = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy_url,
            'ftpProxy': proxy_url,
            'sslProxy': proxy_url,
            'noProxy': 'localhost, 127.0.0.1'
        })

        return p

    def start_proxy(self):
        """
        Start the proxy process.
        """
        if not self.proxy_referer:
            raise Exception('Set the proxy_referer in child class!')

        python_path = sys.executable
        current_dir = os.path.dirname(__file__)
        proxy_file = os.path.normpath(os.path.join(current_dir, 'referer_proxy.py'))

        command = self.proxy_command.format(
            python_path, proxy_file, self.proxy_referer, self.proxy_port)

        print('Running the proxy command:')
        print(command)

        self.proxy_server = pexpect.spawnu(command)
        self.proxy_server.expect_exact(u'Running...', 2)

    def stop_proxy(self):
        """
        Override in child class to use a proxy.
        """
        print('Stopping proxy server...')
        self.proxy_server.close(True)
        print('Proxy server stopped.')
