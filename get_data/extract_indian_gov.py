#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
from bs4 import BeautifulSoup
import re
from urllib.parse import urlsplit
from glob import glob

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <dir>" % (__file__))
        sys.exit()

    data = dict()
    key = False
    keys = set()
    keys.add('mpcode')
    for g in glob(sys.argv[1] + "/detail-*.html"):
        m = re.match(r'.*?-(\d+).html', g)
        mpcode = m.group(1)
        data[mpcode] = dict()
        # Detail
        try:
            with open(g, encoding='utf-8') as m:
                html = m.read()
        except:
            html = ""
        soup = BeautifulSoup(html)
        table1 = soup.find('table', {'class': 'table1'})
        for td in table1.find_all('td'):
            std = td.find('strong')
            if std:
                if key:
                    raise()
                key = True
                cur_key = std.text.strip()
                keys.add(cur_key)
            else:
                if not key:
                    raise
                key = False
                data[mpcode][cur_key] = td.text.strip()
                #print(td.text)
        # Bio
        try:
            with open(sys.argv[1] + "/bio-%s.html" % mpcode, encoding='utf-8') as m:
                html = m.read()
        except:
            html = ""
        soup = BeautifulSoup(html)
        table1 = soup.find('table', {'class': 'table1'})
        for tr in table1.find_all('tr'):
            tds = []
            for td in tr.find_all('td'):
                tds.append(td)
            rowspan = False
            std = tds[0].find('strong')
            if std:
                cur_key = std.text.strip()
                keys.add(cur_key)
            elif tds[0].has_attr('align'):
                rowspan = True
                data[mpcode][cur_key] += "\n%s|%s" % (tds[0].texti.strip(), tds[1].text.strip())
            if not rowspan:
                data[mpcode][cur_key] = tds[1].text.strip()

    o = open("%s-out.csv" % sys.argv[1].strip('/'), "wt", encoding='utf-8', newline='')
    writer = csv.DictWriter(o, fieldnames=sorted(list(keys)), dialect='excel')
    writer.writeheader()
    for d in data:
        data[d]['mpcode'] = d
        r = data[d]
        writer.writerow(r)
    o.close()
