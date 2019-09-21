// NOTES
// https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md
// https://stackoverflow.com/questions/52497252/puppeteer-wait-until-page-is-completely-loaded
// https://linuxhint.com/puppeteer_vs_selenium/
// https://www.toptal.com/puppeteer/headless-browser-puppeteer-tutorial
// https://blog.bitsrc.io/web-scraping-with-puppeteer-e73e5fee7474
// https://puppeteersandbox.com/
// https://pptr.dev/
const puppeteer = require('puppeteer');
const fs = require('fs');

// Get Notice of Default links in HTML from www.criis.com
// I usually search for a quarter's worth of defaults
// There is the initial page where dates must be set and then click submit
// Then another page will load up in 2-3 seconds with many HTML links
try {
  (async () => {
    const browser = await puppeteer.launch({ headless: true, args: ["--fast-start", "--disable-extensions", "--no-sandbox"], slowMo: 50 });
    console.log('[1:agent]',await browser.userAgent())
    const page = await browser.newPage()
    console.log('[2:start]',Date())
    // first page, select dates
    await page.goto('http://www.criis.com/cgi-bin/doc_search.cgi?COUNTY=sanfrancisco&YEARSEGMENT=current&TAB=3')
	await page.select('select[name="DOC_TYPE"]', '007')
    await page.$eval('input[id="dateboxA"]', el => el.value = '06012019')
    await page.$eval('input[id="dateboxB"]', el => el.value = '09202019')
    await page.click('input[type="submit"]')

    // wait for next page to load
    // NB: if waitForSelector() is not called, only a portion of page is output! Have to waitForSelector() to complete
    // The trick is to wait for a DOM element at page bottom: <a name="Last_Page" id="Last_Page">&nbsp;</a>
    await page.waitForSelector('#Last_Page') 
    console.log('[3:await]',Date())

    // once page is loaded write a file
    const html = await page.content()
    const filename = "nod.html"
    fs.writeFile(filename, html, function(err) {
      if(err) { return console.log(err); }
    }); 
    console.log('[4:write]', filename, html.length,"bytes")

    // finally close browser
    await browser.close()

  })()
} catch (err) {
  console.error(err)
}

