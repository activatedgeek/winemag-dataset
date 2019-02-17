# Winemag Dataset

This is the web spider for [Winemag](https://www.winemag.com/) Reviews Dataset
built with [Scrapy](https://scrapy.org/).

## Data

At this stage, the following attributes are being collected.

| **Field**  | **Type**  | **Description**  | **Example**  |
|---|---|---|---|
| _url_  | `str`  | Full URL to the review  |  [https://www.winemag.com/buying-guide/laurent-...-morgon/](https://www.winemag.com/buying-guide/laurent-gauthier-2016-vieilles-vignes-cote-du-py-morgon/) |
| _title_ | `str` | Title/Name of the wine. **WARNING**: May include scraping errors.  | Laurent Gauthier 2016 Vieilles Vignes Côte du Py (Morgon)  |
| _rating_  | `int` | Wine rating on the 100-point scale  | 91 |
| _description_  | `str` | Review of the wine  | Wood aging has given spice to this rich, structured wine. Tannins and generous black fruits show through the still-young structure. This powerful wine, from one of the top vineyards in Morgon, will age well. Drink from 2020. |
| _price_  | `float`, `NULL` | Price in $ |  25  |
| _designation_  | `str`, `NULL` | Quality level of wine  | Vieilles Vignes Côte du Py |
| _varietal_ | `str`  | Grape Varietal/Blend name  | Gamay |
| _country_  | `str`  | Name of Country  | France |
| _region_  | `str`, `NULL`  | Region within a Country  | Beaujolais  |
| _subregion_  | `str`, `NULL`  | Sub-region within a region  | Morgon  |
| _subsubregion_  | `str`, `NULL`  | Detailed region  |  |
| _winery_ | `str`  |  Name of producer/winery | Laurent Gauthier |
| _vintage_  | `int`, `NULL`  | Vintage (Year) of production  | 2016  |
| _alcohol_  | `float`, `NULL`  | Alcohol By Volume (ABV) in %  | 13.5  |
| _category_ | `str`  |  Category of wine | Red |

## Dependencies

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (4.5+)

* Install the environment using
  ```bash
  conda env create -f environment.yaml
  ```
  
**NOTE**: Feel free to use any package manager as long as the dependencies are
satisfied.

## Usage

Start the crawler using,

```bash
scrapy crawl winemag -a start_page=1 -a end_page=10 \
                     -o winemag-1-10.csv
```

See [Scrapy Command Line](https://docs.scrapy.org/en/latest/topics/commands.html)
for more details.

This command will scrape pages 1 to 10 of the reviews.

**WARNING**: Careful with the scraping limits. You are advised to scrape only a 
few pages per spider per session.

With the current [settings.py](./winemag/settings.py), it takes about ~320 hours
(~20 hours each for 16 spiders) to collect ~250k reviews.

## Access Data

Download the raw data [here](http://bit.ly/winemag-raw-250k). 

### Notes

* Some vintages have been wrongly parsed in situations where the title included
  more than one four-digit numbers.

## License

MIT
