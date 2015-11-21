## Biographical Data of Indian Politicians

Biographical data of national, state and some local elections candidates from [archive.india.gov.in](https://www.archive.india.gov.in/) and [myneta.info](http://www.myneta.info/) along with scripts for retrieving the data. 

### Data on Indian MPs from the 'National Portal of India'

Data on Indian MPs serving the [Lok Sabha](http://www.archive.india.gov.in/govt/loksabha.php?alpha=all) and the [Rajya Sabha](http://www.archive.india.gov.in/govt/rajyasabha.php?alpha=all). The data were scraped in June, 2014 and November, 2015.    
* [15th Lok Sabha](data/loksabha_2014.csv) Scraped June, 2014  
* [16th Lok Sabha](data/loksabha_2015.csv) Scraped November, 2015  
* [Rajya Sabha 2014](data/rajyasabha_2014.csv)  Scraped June, 2014  
* [Rajya Sabha 2015](data/rajyasabha_2015.csv)  Scraped November, 2015  

**Note:** In 2015, the list of Rajya Sabha members on the site appears to differ slightly from the list posted on [http://rajyasabha.nic.in/](http://rajyasabha.nic.in/).  

To get the data, download the scripts in the [get_data/archive_india_gov](get_data/archive_india_gov) folder to your computer. The scripts require `Python 3.x` and `BeautifulSoup 4` to run. The package dependency is listed in [get_data/archive_india_gov/requirements.txt](get_data/archive_india_gov/requirements.txt). Once you have installed the dependencies, you can run the scripts.

1.  To download web pages containing the information, run [scrape_indian_gov.py](scripts/scrape_indian_gov.py): 
	```
	python scrape_indian_gov.py
	```
	The HTML files will be saved in `./rajyasabha` and `./loksabha`  

2. To parse and extract information from the HTML files, run [extract_indian_gov.py](scripts/extract_indian_gov.py)

	```
	python extract_indian_gov.py <dir>
	```
	The script outputs a CSV file, saving it as `dir-out.csv`  

### Data on All Candidates from myNeta

Select biographical data of national, state and some local elections candidates from [myneta.info](http://myneta.info). The data were scraped in November, 2015.   
* [All the candidates](data/myneta_data.csv)

### Applications

1. The data from the 15th Lok Sabha and members in Rajya Sabha as of June, 2014 was used to produce this small note: [(No) Missing daughters of Indian Politicians](http://gbytes.gsood.com/2014/06/29/missing-daughters-of-indian-politicians/)

### License
Scripts, figures, and writing are released under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/). 