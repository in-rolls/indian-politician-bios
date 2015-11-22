#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.cookiejar
import os
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error

cookie_filename = "cookies"


class SimpleScraper():
    def __init__(self):
        self.cj = http.cookiejar.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib.request.build_opener()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(debuglevel=0),
            urllib.request.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/5.0 (Windows NT 5.1; rv:24.0) Gecko/20100101 Firefox/24.0'))
        ]
        self.cj.save()

    def get(self, url):
        try:
            response = self.opener.open(url)
            text = ''.join(v.decode('utf-8') for v in response.readlines())
            return text
        except:
            return False

    def post(self, url, data):
        try:
            post_data = urllib.parse.urlencode(dict([k, v.encode('utf-8')]
                                               for k, v in list(data.items())))
            response = self.opener.open(url, post_data.encode())
            text = ''.join(v.decode('utf-8') for v in response.readlines())
            return text
        except:
            return False
