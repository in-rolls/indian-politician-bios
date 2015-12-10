#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import argparse
import logging
import time
import re
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from csv import DictWriter

logging.getLogger("requests").setLevel(logging.WARNING)


def setup_logger():
    """ Set up logging
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='india_mps_women.log',
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def get_html(url):
    # FIXME: should have maximum retry count
    while True:
        try:
            r = requests.get(url)
            return r
        except Exception as e:
            logging.error('{0}'.format(e))
            time.sleep(5)


def get_state_assemblies():
    links = {}
    r = get_html('http://www.myneta.info/')
    soup = BeautifulSoup(r.text, "lxml")
    for div in soup.find_all('div', {'class': 'item'}):
        for a in div.find_all('a'):
            href = a['href']
            m = re.match('.*state_assembly\.php\?state\=(.*)', href)
            if m:
                state = m.group(1)
                links[state] = href
    return links


def get_elections(url):
    links = {}
    r = get_html(url)
    soup = BeautifulSoup(r.text, "lxml")
    for div in soup.select('h3.title.yellow'):
        election = div.text
        for a in div.parent.select('a'):
            if a.text.lower().strip() == 'all candidates':
                href = a['href']
                links[election] = href
    return links


def get_nation_elections(url):
    links = {}
    r = get_html(url)
    soup = BeautifulSoup(r.text, "lxml")
    for div in soup.select('h3.title.blue'):
        election = div.text
        if election == 'Lok Sabha Election':
            for div2 in div.parent.select('div.item'):
                election_year = div2.contents[0].strip()
                for a in div2.select('a'):
                    if a.text.lower().strip() == 'all candidates':
                        href = a['href']
                        links[election_year] = href
            break
    return links


def get_local_elections(url):
    links = {}
    r = get_html(url)
    soup = BeautifulSoup(r.text, "lxml")
    for div in soup.select('h3.title.blue'):
        election = div.text
        if election == 'Local Body Elections':
            for div2 in div.parent.select('div.item'):
                election_year = div2.contents[0].strip()
                for a in div2.select('a'):
                    if a.text.lower().strip() == 'all candidates':
                        href = a['href']
                        links[election_year] = href
            break
    return links


def get_women_candidates(url):
    cans = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all('a', href=re.compile('.*women_candidate.*'))
    if len(a):
        m = re.match(r'.*=\s+(\d+)\s+.*', a[0].text)
        if m:
            total = int(m.group(1))
        else:
            total = 0
        women_url = url + a[0].attrs['href']
        r = requests.get(women_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        count = 0
        for a in soup.find_all('a', href=re.compile(r'.*candidate_id=.*')):
            pol_url = url + a.attrs['href']
            cans.append({'politician_url': pol_url})
            count += 1
        logging.info("Count = {0}, Total = {1}".format(count, total))
        if count != total:
            raise
    return cans


if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser(description='India MPs Women candidates to CSV')
    parser.add_argument('-o', '--output', default='output-women.csv',
                        help='Output CSV file name')
    parser.add_argument('-t', '--type', default='all',
                        help='Type (all|state|nation|local)')
    parser.add_argument('--no-header', dest='header', action='store_false',
                        help='Output without header at the first row')
    parser.set_defaults(header=True)

    args = parser.parse_args()

    logging.info('Output file: {0}'.format(args.output))
    of = open(args.output, 'wb')

    headers = ['politician_url']
    writer = DictWriter(of, fieldnames=headers)
    if args.header:
        writer.writeheader()

    count = 0

    if args.type in ['all', 'nation']:
        # Get Nation
        elections = get_nation_elections('http://www.myneta.info/')
        for e in sorted(elections):
            logging.info(e)
            year = e.split()[-1]
            logging.info("Year: {0}".format(year))
            url = elections[e]
            cans = get_women_candidates(url)
            writer.writerows(cans)
            count += len(cans)
            #break

    if args.type in ['all', 'local']:
       # Get Local
        elections = get_local_elections('http://www.myneta.info/')
        for e in sorted(elections):
            print e
            year = e.split()[-1]
            logging.info("Year: {0}".format(year))
            url = elections[e]
            cans = get_women_candidates(url)
            writer.writerows(cans)
            count += len(cans)
            #break

    if args.type in ['all', 'state']:
        # Get state
        states = get_state_assemblies()
        for s in sorted(states):
            logging.info("State: '{0}'".format(s))
            href = states[s]
            elections = get_elections(href)
            for e in sorted(elections):
                year = e.split()[-1]
                logging.info("Year: {0}".format(year))
                url = elections[e]
                cans = get_women_candidates(url)
                writer.writerows(cans)
                count += len(cans)
                #break
            #break
    of.close()
    logging.info("Total: {0}".format(count))
