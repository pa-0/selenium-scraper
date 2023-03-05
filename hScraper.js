const puppeteer = require('puppeteer')
const https = require('https');
const jsoncsv = require('json-2-csv');
const fs = require('fs');

async function amazonScrape(query_item) {
    query_item = query_item.replace(/\s/g, '+');
    let items = [];
    console.log("starting scrape");
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] })
    const page = await browser.newPage()
    for (let i = 0; i < 4; i++) {
        console.log("scraping page " + (i + 1));
        // let url = 'https://www.amazon.de/s?k=waschmaschine&sprefix=was%2Caps%2C92&ref=nb_sb_ss_ts-doa-p_1_3'
        // let url = 'https://www.amazon.de/s?k=toaster&sprefix=toast%2Caps%2C81&ref=nb_sb_ss_ts-doa-p_1_5'
        let url = `https://www.amazon.de/-/en/s?k=${query_item}&page=${i + 1}&crid=T3MMRQJCBWVD&qid=1656715304&sprefix=${query_item}%2Caps%2C78&ref=sr_pg_${i + 1}`
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
        await page.waitForSelector('.a-price-whole');

        let raw_items = await page.$$eval("div.a-section", elements =>
            elements.map(item => {
                let name = item.querySelector("h2 span.a-color-base")?.textContent
                let price = item.querySelector(".a-price-whole")?.textContent
                let link = item.querySelector(".a-link-normal")?.href
                if (name && price) {
                    return {
                        name: name,
                        price: price,
                        link: link
                    }
                }
            }
            ))
        items.push(...raw_items.filter(item => item != null))
    }
    browser.close();
    return items
}

async function walmartScrape(query_item) {
    query_item = query_item.replace(/\s/g, '+');
    let items = [];
    console.log("starting scrape");
    const browser = await puppeteer.launch()
    const page = await browser.newPage()


    for (let i = 0; i < 1; i++) {
        let url = `https://www.walmart.com/search?q=${query_item}`
        console.log("scraping page " + (i + 1) + " from " + url);
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
        // await page.waitForSelector('.absolute');
        await page.waitForTimeout(1200);

        let bodyHTML = await page.evaluate(() => document.body.innerHTML);
        console.log(bodyHTML)

        let raw_items = await page.$$eval("div.pa0-xl ", elements =>
            elements.map(item => {
                // let name = item.querySelector("div.list-view div.flex div.b")?.textContent
                // let price = item.querySelector(".a-price-whole")?.textContent
                // let link = item.querySelector("a.absolute")?.href
                // if (name && price) {
                    console.log("hast inja")
                    return item.innerHTML
                    return {
                        name: name,
                        // price: price,
                        link: link
                    }
                // }
            }
            ))
        items.push(...raw_items.filter(item => item != null))
    }
    browser.close();
    return items
}


async function aldiScrape() {

    let items = [];
    console.log("starting scrape");
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] })
    const page = await browser.newPage()
    let categories = ['gefluegel', 'gemischtes-fleisch', 'lamm', 'rind', 'schwein', 'wurst-aufschnitt']
    for (let i = 0; i < 6; i++) {

        console.log("scraping page category " + categories[i]);
        let url = `https://www.aldi-nord.de/sortiment/kuehlung-tiefkuehlung/fleisch/${categories[i]}.html`
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
        await page.waitForSelector('.mod-article-tile');

        let raw_items = await page.$$eval("div.mod-article-tile", elements =>
            elements.map(item => {
                let name = item.querySelector("h4 span.mod-article-tile__title")?.textContent
                let price = item.querySelector("span.price__wrapper")?.textContent
                let price__unit = item.querySelector("span.price__unit")?.textContent
                let price_base = item.querySelector("span.price__base")?.textContent
                let link = item.querySelector("a.mod-article-tile__action")?.href
                console.log(i)
                if (name && price) {
                    return {
                        name: name.trim(),
                        price: price,
                        price_unit: price__unit,
                        price_base: price_base,
                        link: link
                    }
                }
            }
            ))
        raw_items = raw_items.map(item => ({ ...item, category: categories[i] }))
        items.push(...raw_items.filter(item => item != null))
    }
    browser.close();
    return items
}


const isElementVisible = async (page, cssSelector) => {
    let visible = true;
    await page
        .waitForSelector(cssSelector, { visible: true, timeout: 2000 })
        .catch(() => {
            visible = false;
        });
    return visible;
};
async function autoScroll(page) {
    console.log("in scrolling")
    await page.evaluate(async () => {
        await new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 200;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                console.log("scrolling")
                totalHeight += distance;

                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    });
}
async function edekaScrape() {

    let items = [];
    console.log("starting scrape");
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] })
    const page = await browser.newPage()
    for (let i = 0; i < 1; i++) {
        console.log("scraping page " + (i + 1));
        let url = `https://www.edeka24.de/Lebensmittel/Beilagen/Nudeln/`
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
        await page.waitForSelector('.product-details');
        await page.waitForTimeout(1000);

   

        let loadMoreVisible = await isElementVisible(page, '#loader-btn');
        // while (loadMoreVisible) {
        //     await page
        //         .click('.loader-container button.FXgradOrange')
        //         .catch(() => {});
        //     loadMoreVisible = await isElementVisible(page, '.loader-container button.FXgradOrange');
        // }
        // await page.click('div.loader-container button.FXgradOrange')
        let j = 0
        while (j < 4) {
            await page.focus('#loader-btn');
            await page.$eval('#loader-btn', elem => elem.click());
            await page.waitForTimeout(1000);
            console.log("loaded more")
            j++
        }

        let raw_items = await page.$$eval("div.product-details", elements =>
            elements.map(item => {
                let name = item.querySelector("a h2")?.textContent
                let price = item.querySelector("div.price")?.textContent
                let price_note = item.querySelector("p.price-note")?.textContent
                let link = item.querySelector("a")?.href
                if (name && price) {
                    return {
                        name: name,
                        price: price?.trim(),
                        price_base: price_note?.trim(),
                        link: link
                    }
                }
            }
            ))
        items.push(...raw_items.filter(item => item != null))
    }
    browser.close();
    return items
}

async function mediamarktScrape() {

    let items = [];
    console.log("starting scrape");
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] })
    const page = await browser.newPage()
    for (let i = 0; i < 1; i++) {
        
        // let url = `https://www.mediamarkt.de/de/search.html?query=toaster&t=1656766140849`
        // let url = `https://www.mediamarkt.de/de/category/toaster-64.html`
        // let url = `https://www.mediamarkt.de/de/category/waschmaschinen-3.html`
        let url = `https://www.mediamarkt.de/de/brand/samsung/smartphones`
        
        console.log("scraping page " + (i + 1) + "from " + url);
        // let url = `https://www.mediamarkt.de/de/brand/apple/iphone`
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
        await page.setViewport({
            width: 1200,
            height: 800
        });
        await page.waitForTimeout(500)
        await autoScroll(page);
        await page.waitForSelector('[class^="StyledCardWrapper"]');

        await page.waitForTimeout(700)
        await page.waitForSelector('div[class^="Paging"]');
        await page.focus('div[class^="Paging"] > button');
        await page.$eval('div[class^="Paging"] > button', elem => elem.click());
        await page.waitForTimeout(1000);
        console.log("loaded more")
        await autoScroll(page);


        let raw_items = await page.$$eval('div[class^="StyledListItem"]', elements =>
            elements.map(item => {
                let name = item.querySelector('p[class^="BaseTypo"]')?.textContent
                let price = item.querySelector('div[class^="StyledUnbrandedPriceDisplayWrapper"] span[aria-hidden="true"]')?.innerText
                let link = item.querySelector("a[class^=StyledLinkRouter]")?.href
                console.log(price)
                if (name && price) {
                    return {
                        name: name,
                        price: price,
                        link: link
                    }
                }
            }
            ))
        items.push(...raw_items.filter(item => item != null))
    }
    browser.close();
    return items
}

async function kauflandScrape(query_item) {
    query_item = query_item.replace(/\s/g, '+');
    let items = [];
    console.log("starting scrape");
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] })
    const page = await browser.newPage()
    for (let i = 0; i < 4; i++) {
        console.log("scraping page " + (i + 1));
        let url = `https://www.kaufland.de/category/5951/`
        if (i != 0) {
            let url = `https://www.kaufland.de/category/5951/p${i + 1}/`
        }
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
        await page.waitForSelector('article.product');

        let raw_items = await page.$$eval("article.product", elements =>
            elements.map(item => {
                let name = item.querySelector("div.product__title")?.textContent
                let price = item.querySelector("div.price__container")?.textContent
                let price_base = item.querySelector("div.product__base-price")?.textContent
                let link = item.querySelector("a.product__wrapper")?.href
                if (name && price) {
                    return {
                        name: name,
                        price: price,
                        price_base: price_base.trim(),
                        link: link
                    }
                }
            }
            ))
        items.push(...raw_items.filter(item => item != null))
    }
    browser.close();
    return items
}


async function scrape() {
    // let items = await amazonScrape('iphone')
    // let items = await aldiScrape()
    // let items = await edekaScrape()
    // let items = await mediamarktScrape()
    // let items = await kauflandScrape('instant-kaffee')
    let items = await walmartScrape('coffee')
    jsoncsv.json2csv(items, (err, csv) => {
        if (err)
            throw err;
        // console.log(csv);
        fs.writeFileSync('items.csv', csv);
    });
}

scrape()

