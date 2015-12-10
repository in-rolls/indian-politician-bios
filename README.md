## Biographical Data of Indian Politicians

Biographical data of national, state and some local elections candidates from [archive.india.gov.in](https://www.archive.india.gov.in/) and [myneta.info](http://www.myneta.info/) along with scripts for retrieving the data. The data from the 15th Lok Sabha and members in Rajya Sabha as of June, 2014 was used to produce this small note: [(No) Missing daughters of Indian Politicians](http://gbytes.gsood.com/2014/06/29/missing-daughters-of-indian-politicians/). While data on all political candidates in national, state and some local elections from myNeta was used to analyze spousal income, movable and immovable assets by politician gender. [Link to analysis](analysis/myneta.md).

----
### Table of Contents

* [Data on Indian MPs from the 'National Portal of India'](#data-on-indian-mps-from-the-national-portal-of-india)  
  * [Get the Data](#get-the-data)
  * [Data](#data)
  * [Analysis and Write-up](#analysis)

* [Data on All Candidates from myNeta](#data-on-all-candidates-from-myneta)
  * [Get the Data](#get-the-data-1)
  * [Data](#data-1)
  * [Analysis and Write-up](#analysis-1) 

----

### Data on Indian MPs from the 'National Portal of India'

Data on Indian MPs serving the [Lok Sabha](http://www.archive.india.gov.in/govt/loksabha.php?alpha=all) and the [Rajya Sabha](http://www.archive.india.gov.in/govt/rajyasabha.php?alpha=all). 

#### Get the Data

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

#### Data

The data were scraped in June, 2014 and November, 2015.    
* [15th Lok Sabha](data/loksabha_2014.csv) (Scraped June, 2014)  
* [16th Lok Sabha](data/loksabha_2015.csv) (Scraped November, 2015)  
* [Rajya Sabha 2014](data/rajyasabha_2014.csv)  (Scraped June, 2014)  
* [Rajya Sabha 2015](data/rajyasabha_2015.csv)  (Scraped November, 2015)

**Note:** In 2015, the list of Rajya Sabha members on the site appears to differ slightly from the [list](data/rajyasabha_rajyasabha_in_nov_2015.csv) posted on [http://rajyasabha.nic.in/](http://rajyasabha.nic.in/).  

#### Analysis 
* [Script](analysis/indiamps.R)

----

### Data on All Candidates from myNeta

Select biographical and electoral data of national, state and some local elections candidates from [myneta.info](http://myneta.info). The data were scraped in November, 2015. 

#### Get the Data
There are three scripts. Why three? Information about gender is not provided on candidate pages and is integrated later. The three scripts are:  
* [india_mps.py](india_mps.py) to download basic profile data.
* [india_mps_women.py](india_mps_women.py) to get information on gender.
* [india_mps_gender.py](india_mps_gender.py) to merge gender information into all three CSVs.

To begin using the scripts, install the [requirements](requirements.txt). Then download the scripts into a folder, and run scripts from the command line. 

```
usage: india_mps.py [-h] [-o OUTPUT] [-n MAX_CONN] [-s FROM_STATE]
                    [-y FROM_YEAR] [-c FROM_CONSTITUENCY] [-t TYPE]
                    [--no-header]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output CSV file name
  -n MAX_CONN, --max-conn MAX_CONN
                        Max concurrent connections
  -s FROM_STATE, --from-state FROM_STATE
                        Start from a specific state
  -y FROM_YEAR, --from-year FROM_YEAR
                        Start from a specific election year
  -c FROM_CONSTITUENCY, --from-constituency FROM_CONSTITUENCY
                        Start from a specific constituency
  -t TYPE, --type TYPE  Type (all|state|nation|local)
  --no-header           Output without header at the first row
```

#### Example

```
python india_mps.py -o india-mps-all.csv
```

#### Get all women candidates

```
python india_mps_women.py
```

URL of all women candidates saved as: `output-women.csv`

To merge all candidates with gender, run:

```
python india_mps_gender.py
```

#### Data  

* [Local](data/india-mps-all-local.csv)
* [State](data/india-mps-all-state.csv)
* [National](data/india-mps-all-nation.csv)
* [Combined](data/myneta_data.csv)

**Meta Data**
* Each row = politician per constituency per election year. 
* Columns  
    * Politician Name, Constituency, State, Party, Election Year, Whether They Won or Not, Type: State/National/Local  
    * Education, Age, Address, Self Profession, Spouse Profession 
    * Income Tax Return: Self Total Income, Spouse Total Income  
    * Self Movable Assests, Spouse Movable Assets: 
      * cash--- for self and spouse  
      * jewellery --- for self and spouse  
      * totals --- for self and spouse    
    * Immovable Assets --- Self Totals, Spouse Totals  
    * Liabilities      --- Self Totals, Spouse Totals 

**Notes**

There are missing data for election years before 2011: 

* Income Tax Return so no Self/Spouse Total Income
* No column for Spouse in the Liabilities
* In a few elections, multiple candidates with the same name are fighting to get elected from the same constituency. For instance, check [here](http://www.myneta.info/pmc2007/index.php?action=show_candidates&constituency_id=19), [here](http://www.myneta.info/bmc2012/index.php?action=show_candidates&constituency_id=110), [here](http://www.myneta.info/mcd2012/index.php?action=show_candidates&constituency_id=213), [here](http://www.myneta.info/mcd2012/index.php?action=show_candidates&constituency_id=141), [here](http://www.myneta.info/mcd2012/index.php?action=show_candidates&constituency_id=171), and [here](http://www.myneta.info/pmc2007/index.php?action=show_candidates&constituency_id=19).

#### Analysis 
* [Script](analysis/myneta.R)

----

### License
Scripts, figures, and writing are released under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/). 