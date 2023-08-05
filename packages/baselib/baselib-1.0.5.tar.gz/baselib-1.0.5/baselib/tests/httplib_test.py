# from baselib.py.httplib import httplib
from six.moves import http_client as httplib

class TestHttplib(object):

    def test_request(self):
        conn = httplib.HTTPConnection("www.baidu.com")
        conn.request('get', '/', {'user-agent':'test'})
        rsp = conn.getresponse()
        print(rsp)

if __name__ == "__main__":
    TestHttplib().test_request()