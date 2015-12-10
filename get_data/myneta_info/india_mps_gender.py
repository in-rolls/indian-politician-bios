#!/usr/bin/env python
# -*- coding: utf-8 -*-

from csv import DictReader, DictWriter

if __name__ == "__main__":
    inputs = ['india-mps-all-nation.csv',
              'india-mps-all-local.csv',
              'india-mps-all-states.csv'
              ]

    women_urls = set()
    with open('output-women.csv', 'rb') as f:
        reader = DictReader(f)
        for r in reader:
            women_urls.add(r['politician_url'])
    print("Total women: {0}".format(len(women_urls)))
    of = None
    count = 0
    for infile in inputs:
        print("Updating...{0}".format(infile))
        f = open(infile, 'rb')
        reader = DictReader(f)
        if of is None:
            of = open('output-all-gender.csv', 'wb')
            writer = DictWriter(of, fieldnames=reader.fieldnames + ['gender'])
            writer.writeheader()
        for r in reader:
            if r['politician_url'] in women_urls:
                r['gender'] = 'female'
                count += 1
            else:
                r['gender'] = 'male'
            writer.writerow(r)
        f.close()
    of.close()

    print("Total updated: {0}".format(count))
