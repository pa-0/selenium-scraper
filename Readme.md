
## Using uScraper.py

- Download [ChromeDriver](https://chromedriver.chromium.org/downloads)
- Update `DRIVER_PATH` value in uscraper.py with the path to the driver
- Run the commands:
```
source env/bin/activate
pip install selenium csv time
python -i uscraper.py
```
- Script opens a browser
- You can scan the page by scan commands
- After each scan data is added to log.csv
```
>>> bot.goTo('<url>')
>>> bot.amazonScan()
>>> bot.goTo('<url>')
>>> bot.comfyScan()
>>> bot.close()
```

## Using hScraper.js (Headless)

Faster but more likely to be blocked by bot detector
- Run these commands:
```
npm i
node scrapers.js
```