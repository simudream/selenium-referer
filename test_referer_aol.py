# -*- coding: utf-8 -*-
import utils
from base_with_proxy import ProxyBase


class TestAolReferer(ProxyBase):
    """
    Sets the referer header to AOL.
    """

    proxy_referer = 'http://www.aol.com'

    def test_referer_and_cookie(self):
        """
        Go to URL with AOL referer.
        """
        cookies = utils.navigate_and_read_cookies(
            self.driver, self.base_url)

        # Find the cookie that was set to track referer.
        # Facebook sets a cookie called 'reg_ext_ref'.
        ref_cookie = [c for c in cookies if c['name'] == 'reg_ext_ref'][0]

        # Make sure the cookie contains aol.com.
        self.assertTrue('www.aol.com' in ref_cookie['value'])
