## Biographical Details of Indian MPs

Data for MPs serving in the **Lok Sabha** (Lower House) and the **Rajya Sabha** (Upper House). The data were scraped from [archive.india.gov](http://www.archive.india.gov.in/govt/). 

### Application
The data from the 15th Lok Sabha and members in Rajya Sabha as of June, 2014 was used to produce this small note: [(No) Missing daughters of Indian Politicians](http://gbytes.gsood.com/2014/06/29/missing-daughters-of-indian-politicians/)

### Get the Data

To use the scripts, download them to your computer. The scripts require `Python 3.x` and `BeautifulSoup 4`. The package dependencies are listed in [get_data/requirements.txt](get_data/requirements.txt). Once you have installed the dependencies, you can run the scripts.

1. To download web pages containing the information, run [scrape_indian_gov.py](scripts/scrape_indian_gov.py): 

```
python scrape_indian_gov.py
```

The HTML files will be saved in `./rajyasabha` and `./loksabha`

2. To parse and extract information from the HTML files, run [extract_indian_gov.py](scripts/extract_indian_gov.py)

```
python extract_indian_gov.py <dir>
```

The script outputs a CSV file, saving it as `dir-out.csv`

###  Data

* [15th Lok Sabha](data/loksabha_2014.csv) [Scraped June, 2014]
* [16th Lok Sabha](data/loksabha_2015.csv) [Scraped November, 2015]
* [Rajya Sabha 2014](data/rajyasabha_2014.csv)  [Scraped June, 2014]
* [Rajya Sabha 2015](data/rajyasabha_2015.csv)  [Scraped November, 2015]

### License

Scripts, figures, and writing are released under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/). 