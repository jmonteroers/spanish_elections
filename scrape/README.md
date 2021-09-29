# Scraping Election Results from ElPais

El Pais general election results are available in XML files.
This package retrieves these XMLs and stores them in
`spanish_elections/data`. To run the scraper, you only need Python 3 installed
and run:
```
python3 scrape.py
```
Beware! This command will lead to running many requests to
the web server of El Pais. So, be mindful before using it.

The names of Autonomous Communities and Provinces are derived from the file
`aacc_province_codes.csv`, which was manually copied from [this link](
  https://www.ine.es/en/daco/daco42/codmun/cod_ccaa_provincia_en.htm
  ). The scrape module applies some corrections to the Autonomous Community
  codes.
