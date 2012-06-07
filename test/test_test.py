import time, logging
import libpry
import requests
from libpathod import test, version, utils

logging.disable(logging.CRITICAL)

class uDaemonManual(libpry.AutoTree):
    def test_startstop(self):
        d = test.Daemon()
        rsp = requests.get("http://localhost:%s/p/202"%d.port)
        assert rsp.ok
        assert rsp.status_code == 202
        d.shutdown()
        libpry.raises(requests.ConnectionError, requests.get, "http://localhost:%s/p/202"%d.port)

    def test_startstop_ssl(self):
        d = test.Daemon(ssl=True)
        rsp = requests.get("https://localhost:%s/p/202"%d.port, verify=False)
        assert rsp.ok
        assert rsp.status_code == 202
        d.shutdown()
        libpry.raises(requests.ConnectionError, requests.get, "http://localhost:%s/p/202"%d.port)

    def test_startstop_ssl_explicit(self):
        ssloptions = dict(
             keyfile = utils.data.path("resources/server.key"),
             certfile = utils.data.path("resources/server.crt"),
        )
        d = test.Daemon(ssl=ssloptions)
        rsp = requests.get("https://localhost:%s/p/202"%d.port, verify=False)
        assert rsp.ok
        assert rsp.status_code == 202
        d.shutdown()
        libpry.raises(requests.ConnectionError, requests.get, "http://localhost:%s/p/202"%d.port)


class uDaemon(libpry.AutoTree):
    def setUpAll(self):
        self.d = test.Daemon()

    def tearDownAll(self):
        self.d.shutdown()

    def test_info(self):
        assert tuple(self.d.info()["version"]) == version.IVERSION



tests = [
    uDaemonManual(),
    uDaemon()
]