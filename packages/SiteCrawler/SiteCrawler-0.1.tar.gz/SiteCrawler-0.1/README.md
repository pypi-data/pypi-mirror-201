# generic-crawler

This project contains a Python script for a web scraper that extracts tables, images, and text from a given website.

## Requirements

- Python 3.7 or later
- Selenium
- Beautiful Soup
- Pandas
- tqdm
- Requests

## Installation
### pip 

pip install WebScraper

### github
1. Clone this repository:

git clone https://gitlab.kaisens.fr/kaisensdata/apps/4inshield/drivers/generic-crawler/-/tree/asaid

2. Install the required Python packages:

pip install -r requirements.txt


## Usage

1. Download the appropriate [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your system and add it to your system's PATH or specify the path when initializing the `WebScraper` class.

2. Use the following example code to run the scraper:

```python
from scraper import WebScraper

chrome_driver_path = "<path_to_your_chromedriver>"
url = "https://example.com"
scraper = WebScraper(chrome_driver_path)
scraper.process_website(url)
