#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import os
import re
from scraper import SimpleScraper
from bs4 import BeautifulSoup

HOUSE = ['rajyasabha', 'loksabha']

BASE_URL = 'http://www.archive.india.gov.in/govt/'

if __name__ == "__main__":
    scraper = SimpleScraper()
    for h in HOUSE:
        print("House type: {0!s}".format(h))
        if not os.path.exists('./{0!s}'.format(h)):
            os.mkdir('./{0!s}'.format(h))

        html = scraper.get(BASE_URL + '{0!s}.php?alpha=all'.format(h))

        soup = BeautifulSoup(html)
        i = 0
        for a in soup.find_all("a", href=True):
            link = a['href']
            m = re.match(r".*?mpcode=(\d+)", link)
            if m:
                i += 1
                mpcode = m.group(1)
                print(i, link)
                html2 = scraper.get(BASE_URL + link)
                if html2:
                    with open('{0!s}/detail-{1!s}.html'.format(h, mpcode), "wb") as f:
                        f.write(str.encode(html2))
                html3 = scraper.get(BASE_URL + '{0!s}mpbiodata.php?mpcode={1!s}'.format(h, mpcode))
                if html3:
                    with open('{0!s}/bio-{1!s}.html'.format(h, mpcode), "wb") as f:
                        f.write(str.encode(html3))
                #break
        print("Found: {0:d}".format(i))
