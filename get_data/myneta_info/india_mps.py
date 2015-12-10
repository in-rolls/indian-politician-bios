#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import argparse
import logging
import time
import re
from collections import defaultdict
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from csv import DictWriter
from multiprocessing import Pool

logging.getLogger("requests").setLevel(logging.WARNING)


def setup_logger():
    """ Set up logging
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='india_mps.log',
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def table_to_list(table):
    dct = table_to_2d_dict(table)
    return list(iter_2d_dict(dct))


def table_to_2d_dict(table):
    result = defaultdict(lambda: defaultdict(unicode))
    for row_i, row in enumerate(table.find_all('tr')):
        for col_i, col in enumerate(row.find_all(['td', 'th'])):
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            col_data = col.text
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    result[i][j] = col_data
    return result


def iter_2d_dict(dct):
    for i, row in sorted(dct.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col)
        yield cols


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


def get_constituencies(url, groupby='district'):
    links = {}
    dist = ''
    r = get_html(url)
    soup = BeautifulSoup(r.text, "lxml")
    for div in soup.select('tr'):
        title = div.select_one('h5.title')
        if not title:
            for i in div.select('div.items'):
                href = url + i.a['href']
                m = re.match(r'.*constituency_id=(\d+).*', href)
                if m:
                    cid = int(m.group(1))
                    con = i.a.text.strip()
                    links[cid] = {groupby: dist, 'url': href, 'base': url, 'name': con}
        else:
            dist = title.text.strip()
    return links


def get_candidates(base, url):
    headers = []
    links = {}
    r = get_html(url)
    soup = BeautifulSoup(r.text, "lxml")
    for table in soup.select('table#table1'):
        for tr in table.select('tr'):
            if tr.a:
                href = base + tr.a['href']
                can = {'url': href}
                i = 0
                name = ''
                for td in tr.select('td'):
                    can[headers[i]] = td.text
                    if name == '':
                        name = td.text.strip()
                    i += 1
                m = re.match(r'.*candidate_id=(\d+).*', href)
                if m:
                    cid = int(m.group(1))
                    can['name'] = name
                    links[cid] = can
            else:
                for th in tr.select('th'):
                    headers.append(th.text)
    return links


def _get_candidate(url, parser='lxml'):
    # url = 'http://www.myneta.info/karnataka2013/candidate.php?candidate_id=279'
    data = {}
    try:
        r = get_html(url)
        #with open('candidate.html', 'wb') as f:
        #    f.write(r.text)
        soup = BeautifulSoup(r.text, parser)

        # Extract data from Yellow box
        for h2 in soup.select('h2.main-title'):
            name = h2.text
            con = h2.parent.h5
            if con:
                con = con.text.strip()
            data['name'] = name
            data['constituency'] = con
            for f in h2.parent.find_all('b'):
                name = f.text.strip()
                value = f.next_sibling
                if value:
                    try:
                        value = value.strip()
                    except:
                        value = ''
                        pass
                else:
                    value = ''
                data[name] = value

        for h3 in soup.select('h3'):
            # Education details
            if h3.text.find('Educational Details') != -1:
                try:
                    data['education'] = h3.parent.select('div')[0].text
                    data['education_detail'] = h3.parent.select('div')[1].text
                except:
                    pass
                break

        # Extract data from tables
        for h3 in soup.select('h3.title.blue'):
            table_name = h3.text
            # Income Tax return
            if table_name.find('Income Tax return') != -1:
                for t in h3.find_all_next('table'):
                    table = table_to_list(t)
                    #pprint(table)
                    col_total = 0
                    for c in table[0]:
                        if c.find('Total Income') != -1:
                            break
                        col_total += 1
                    for r in table[1:]:
                        if r[0] == 'self':
                            data['self_total_income'] = r[col_total]
                        elif r[0] == 'spouse':
                            data['spouse_total_income'] = r[col_total]
                    break
            # Movable Assets
            elif table_name.find('Movable Assets') != -1:
                for t in h3.find_all_next('table'):
                    table = table_to_list(t)
                    #pprint(table)
                    for r in table[1:]:
                        if r[1].startswith('Cash'):
                            data['self_movable_assets_cash'] = r[2]
                            data['spouse_movable_assets_cash'] = r[3]
                        elif r[1].startswith('Jewellery'):
                            data['self_movable_assets_jewellery'] = r[2]
                            data['spouse_movable_assets_jewellery'] = r[3]
                        elif r[1].startswith('Totals'):
                            data['self_movable_assets_totals'] = r[2]
                            data['spouse_movable_assets_totals'] = r[3]
                    break
            # Immovable Assets
            elif table_name.find('Immovable Assets') != -1:
                for t in h3.find_all_next('table'):
                    table = table_to_list(t)
                    #pprint(table)
                    for r in table[1:]:
                        if r[1].startswith('Totals'):
                            data['self_immovable_assets_totals'] = r[2]
                            data['spouse_immovable_assets_totals'] = r[3]
                    break
            # Liabilities
            elif table_name.find('Liabilities') != -1:
                for t in h3.find_all_next('table'):
                    table = table_to_list(t)
                    #pprint(table)
                    if table[0][2].startswith('Amount'):
                       for r in table[1:]:
                            if r[1].startswith('Totals'):
                                data['self_liabilities_totals'] = r[3]
                    else:
                        for r in table[1:]:
                            if r[1].startswith('Totals'):
                                data['self_liabilities_totals'] = r[2]
                                data['spouse_liabilities_totals'] = r[3]
                    break
    except Exception as e:
        logging.warn("Error to parse URL '{0}'".format(url))
        logging.warn("Error to detail :-\nParser: '{0}'\n'{1}'".format(parser, traceback.format_exc()))
        if parser == 'lxml':
            # Fallback to 'html.parser'
            data = _get_candidate(url, 'html.parser')
    return data


def get_candidate(can):
    url = can['url']
    data = _get_candidate(url)
    data['politician_url'] = url
    data['criminal_cases'] = can['Criminal Cases']
    return data


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

if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser(description='India MPs scrape and parse to CSV')
    parser.add_argument('-o', '--output', default='output.csv',
                        help='Output CSV file name')
    parser.add_argument('-n', '--max-conn', type=int, default=10,
                        help='Max concurrent connections')
    parser.add_argument('-s', '--from-state', default=None,
                        help='Start from a specific state')
    parser.add_argument('-y', '--from-year', default=None,
                        help='Start from a specific election year')
    parser.add_argument('-c', '--from-constituency', default=None,
                        help='Start from a specific constituency')
    parser.add_argument('-t', '--type', default='all',
                        help='Type (all|state|nation|local)')
    parser.add_argument('--no-header', dest='header', action='store_false',
                        help='Output without header at the first row')
    parser.set_defaults(header=True)

    args = parser.parse_args()

    pool = Pool(processes=args.max_conn)

    logging.info('Output file: {0}'.format(args.output))
    of = open(args.output, 'wb')

    headers = ['type', 'politician_name', 'politician_url', 'age', 'address', 'party', 'criminal_cases', 'education', 'education_detail', 's/o|d/o|w/o', 'contact_number', 'email', 'name_enrolled_as_voter_in', 'self_profession', 'spouse_profession', 'state', 'state_url', 'district', 'constituency', 'constituency_url','election_year', 'election_url', 'winner', 'self_total_income', 'spouse_total_income', 'self_movable_assets_cash', 'spouse_movable_assets_cash', 'self_movable_assets_jewellery', 'spouse_movable_assets_jewellery', 'self_movable_assets_totals', 'spouse_movable_assets_totals', 'self_immovable_assets_totals', 'spouse_immovable_assets_totals', 'self_liabilities_totals', 'spouse_liabilities_totals'] 
    writer = DictWriter(of, fieldnames=headers)
    if args.header:
        writer.writeheader()

    skip = True
    count = 0

    if args.type in ['all', 'nation']:
        # Get Nation
        data = {}
        data['type'] = 'nation'
        elections = get_nation_elections('http://www.myneta.info/')
        for e in sorted(elections):
            year = e.split()[-1]
            logging.info("Year: {0}".format(year))
            if skip and args.from_year and year != args.from_year:
                continue
            data['election_year'] = year
            data['election_url'] = elections[e]
            cons = get_constituencies(elections[e], 'state')
            for c in sorted(cons):
                s = cons[c]['state']
                logging.info("State: '{0}'".format(s))
                if skip and args.from_state and s != args.from_state:
                    continue
                logging.info("Constituency: '{0}'"
                             .format(cons[c]['name'].encode('utf-8')))
                if skip and args.from_constituency and cons[c]['name'] != args.from_constituency:
                    continue
                if skip:
                    skip = False
                    logging.info("Start now...")
                base = cons[c]['base']
                url = cons[c]['url']
                data['constituency'] = cons[c]['name']
                data['constituency_url'] = url
                data['state'] = cons[c]['state']
                cans = get_candidates(base, url)
                results = pool.map(get_candidate, cans.values())
                for data2 in results:
                    data2.update(data)
                    for k in data2:
                        new_k = '_'.join(k.strip().strip(':').lower()
                                         .split(' '))
                        data2[new_k] = data2.pop(k)
                    if data2['name'].find('(Winner)') != -1:
                        data2['winner'] = 'yes'
                    else:
                        data2['winner'] = 'no'
                    data2['politician_name'] = data2.pop('name')
                    for k in data2:
                        data2[k] = data2[k].encode('utf-8')
                    #pprint(data2)
                    try:
                        writer.writerow(data2)
                    except Exception as e:
                        url = data2['politician_url']
                        logging.warn("Invalid parse on URL: {0}".format(url))
                        msg = e.message
                        if msg.startswith('dict contains fields not in fieldnames:'):
                            msg = msg.replace('dict contains fields not in fieldnames: ', '')
                            cols = eval('[' + msg + ']')
                            for c in cols:
                                logging.warn("Cannot write '{0}' = '{1}'"
                                             .format(c.encode('utf-8'),
                                                     data2[c].encode('utf-8')))
                                del data2[c]
                            writer.writerow(data2)
                    count += 1
                    logging.info("{0}: '{1}'"
                                 .format(count, data2['politician_name']))
                #break
            #break

    skip = True

    if args.type in ['all', 'local']:
        # Get Local
        data = {}
        data['type'] = 'local'
        elections = get_local_elections('http://www.myneta.info/')
        for e in sorted(elections):
            year = e.split()[-1]
            logging.info("Year: {0}".format(year))
            if skip and args.from_year and year != args.from_year:
                continue
            data['election_year'] = year
            data['election_url'] = elections[e]
            cons = get_constituencies(elections[e], 'state')
            for c in sorted(cons):
                s = cons[c]['state']
                logging.info("State: '{0}'".format(s))
                if skip and args.from_state and s != args.from_state:
                    continue
                logging.info("Constituency: '{0}'"
                             .format(cons[c]['name'].encode('utf-8')))
                if skip and args.from_constituency and cons[c]['name'] != args.from_constituency:
                    continue
                if skip:
                    skip = False
                    logging.info("Start now...")
                base = cons[c]['base']
                url = cons[c]['url']
                data['constituency'] = cons[c]['name']
                data['constituency_url'] = url
                data['state'] = cons[c]['state']
                cans = get_candidates(base, url)
                results = pool.map(get_candidate, cans.values())
                for data2 in results:
                    data2.update(data)
                    for k in data2:
                        new_k = '_'.join(k.strip().strip(':').lower()
                                         .split(' '))
                        data2[new_k] = data2.pop(k)
                    if data2['name'].find('(Winner)') != -1:
                        data2['winner'] = 'yes'
                    else:
                        data2['winner'] = 'no'
                    data2['politician_name'] = data2.pop('name')
                    for k in data2:
                        data2[k] = data2[k].encode('utf-8')
                    #pprint(data2)
                    try:
                        writer.writerow(data2)
                    except Exception as e:
                        url = data2['politician_url']
                        logging.warn("Invalid parse on URL: {0}".format(url))
                        msg = e.message
                        if msg.startswith('dict contains fields not in fieldnames:'):
                            msg = msg.replace('dict contains fields not in fieldnames: ', '')
                            cols = eval('[' + msg + ']')
                            for c in cols:
                                logging.warn("Cannot write '{0}' = '{1}'"
                                             .format(c.encode('utf-8'),
                                                     data2[c].encode('utf-8')))
                                del data2[c]
                            writer.writerow(data2)
                    count += 1
                    logging.info("{0}: '{1}'"
                                 .format(count, data2['politician_name']))
                #break
            #break

    skip = True

    if args.type in ['all', 'state']:
        # Get state
        data = {}
        states = get_state_assemblies()
        data['type'] = 'state'
        for s in sorted(states):
            logging.info("State: '{0}'".format(s))
            if skip and args.from_state and s != args.from_state:
                continue
            data['state'] = s
            href = states[s]
            data['state_url'] = href
            elections = get_elections(href)
            for e in sorted(elections):
                year = e.split()[-1]
                logging.info("Year: {0}".format(year))
                if skip and args.from_year and year != args.from_year:
                    continue
                data['election_year'] = year
                data['election_url'] = elections[e]
                cons = get_constituencies(elections[e])
                for c in sorted(cons):
                    logging.info("Constituency: '{0}'"
                                 .format(cons[c]['name'].encode('utf-8')))
                    if skip and args.from_constituency and cons[c]['name'] != args.from_constituency:
                        continue
                    if skip:
                        skip = False
                        logging.info("Start now...")
                    base = cons[c]['base']
                    url = cons[c]['url']
                    data['constituency'] = cons[c]['name']
                    data['constituency_url'] = url
                    data['district'] = cons[c]['district']
                    cans = get_candidates(base, url)
                    results = pool.map(get_candidate, cans.values())
                    for data2 in results:
                        data2.update(data)
                        for k in data2:
                            new_k = '_'.join(k.strip().strip(':').lower()
                                             .split(' '))
                            data2[new_k] = data2.pop(k)
                        if data2['name'].find('(Winner)') != -1:
                            data2['winner'] = 'yes'
                        else:
                            data2['winner'] = 'no'
                        data2['politician_name'] = data2.pop('name')
                        for k in data2:
                            data2[k] = data2[k].encode('utf-8')
                        #pprint(data2)
                        try:
                            writer.writerow(data2)
                        except Exception as e:
                            url = data2['politician_url']
                            logging.warn("Invalid parse on URL: {0}"
                                         .format(url))
                            msg = e.message
                            if msg.startswith('dict contains fields not in fieldnames:'):
                                msg = msg.replace('dict contains fields not in fieldnames: ', '')
                                cols = eval('[' + msg + ']')
                                for c in cols:
                                    logging.warn("Cannot write '{0}' = '{1}'"
                                                 .format(c.encode('utf-8'),
                                                         data2[c]
                                                         .encode('utf-8')))
                                    del data2[c]
                                writer.writerow(data2)
                        count += 1
                        logging.info("{0}: '{1}'"
                                     .format(count, data2['politician_name']))
                    #break
                #break
            #break
    of.close()
    logging.info("Total: {0}".format(count))
