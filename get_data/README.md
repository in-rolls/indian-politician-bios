India Members of Parliament
============================

Requires
-------------
- Python 3.x
- BeautifulSoup 4

Usage
------
1. Scrape data to files

```
python scrape_indian_gov.py
```

HTML files will be saved to `./rajyasabha` and `./loksabha`

2. Parse and extract information from file

```
python extract_indian_gov.py <dir>
```

Outputs CSV file. Saved as `dir-out.csv`

