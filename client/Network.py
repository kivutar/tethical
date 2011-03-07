import urllib2
from urllib import urlencode
import cookielib
import json

class ServerConnection():

    def __init__(self):
        self.cookies = cookielib.CookieJar()
        self.cookies.clear()
        self.opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(self.opener)

    def Send(self, handler, values=None):
        try:
            if values:
                rsp = self.opener.open('http://localhost:3000/'+handler, urlencode(values))
            else:
                rsp = self.opener.open('http://localhost:3000/'+handler)
        except IOError, e:
            print e.code
            print e.read()
        else:
            retval = json.loads(rsp.read())
            rsp.close()
            return retval

