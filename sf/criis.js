// NOTES
// https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md
// https://linuxhint.com/puppeteer_vs_selenium/
// https://pptr.dev/
// https://www.toptal.com/puppeteer/headless-browser-puppeteer-tutorial
// https://stackoverflow.com/questions/52497252/puppeteer-wait-until-page-is-completely-loaded
// https://blog.bitsrc.io/web-scraping-with-puppeteer-e73e5fee7474
const puppeteer = require('puppeteer');

try {
  (async () => {
    const browser = await puppeteer.launch({ headless: true, args: ["--fast-start", "--disable-extensions", "--no-sandbox"], slowMo: 50 });
    console.log('[pup]:',await browser.userAgent())
    const page = await browser.newPage()
    console.log('[pup] Dates:',Date())
    // first page, select dates
    await page.goto('http://www.criis.com/cgi-bin/doc_search.cgi?COUNTY=sanfrancisco&YEARSEGMENT=current&TAB=3')
	await page.select('select[name="DOC_TYPE"]', '007')
    await page.$eval('input[id="dateboxA"]', el => el.value = '06012019')
    await page.$eval('input[id="dateboxB"]', el => el.value = '09202019')
    await page.click('input[type="submit"]')
    console.log('[pup] Dates:',Date())
    // if .waitForSelector() is removed, only a portion of the page is output
    // you have to waitForSelector()

    // wait for next page
    // <a name="Last_Page" id="Last_Page">&nbsp;</a>
    await page.waitForSelector('#Last_Page') 
    console.log("html:", await page.content())
    await browser.close()

  })()
} catch (err) {
  console.error(err)
}

