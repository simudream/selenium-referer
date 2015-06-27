# -*- coding: utf-8 -*-
"""
Proxy server to add a specified Referer: header to the request.
"""
from optparse import OptionParser
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer


class RefererMaster(controller.Master):
    """
    Adds a specified referer header to the request.
    """

    def __init__(self, server, referer):
        """
        Init the proxy master.
        :param server: ProxyServer
        :param referer: string
        """
        controller.Master.__init__(self, server)
        self.referer = referer

    def run(self):
        """
        Basic run method.
        """
        try:
            print('Running...')
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, flow):
        """
        Adds a Referer header.
        """
        flow.request.headers['referer'] = [self.referer]
        flow.reply()

    def handle_response(self, flow):
        """
        Does not do anything extra.
        """
        flow.reply()


def start_proxy_server(port, referer):
    """
    Start proxy server and return an instance.
    :param port: int
    :param referer: string
    :return: RefererMaster
    """
    config = proxy.ProxyConfig(port=port)
    server = ProxyServer(config)
    m = RefererMaster(server, referer)
    m.run()


if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option("-r", "--referer", dest="referer",
                      help="Referer URL.")

    parser.add_option("-p", "--port", dest="port", type="int",
                      help="Port number (int) to run the server on.")

    popts, pargs = parser.parse_args()

    start_proxy_server(popts.port, popts.referer)
