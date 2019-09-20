const puppeteer = require('puppeteer');

(async () => {
	const browser = await puppeteer.launch({ headless: false, args: ["--fast-start", "--disable-extensions", "--no-sandbox"] });
	const page = await browser.newPage();
	await page.goto('http://www.criis.com/cgi-bin/doc_search.cgi?COUNTY=sanfrancisco&YEARSEGMENT=current&TAB=3');

	await page.select('select[name="DOC_TYPE"]', '002'); 
	await page.$eval('input[id="dateboxA"]', el => el.value = '04012019');
	await page.$eval('input[id="dateboxB"]', el => el.value = '04202019');
	await page.click('input[type="submit"]');

	const resp = await page.waitForNavigation(); // wait for search results page to load
	console.log(resp._headers);
	await browser.close();

})();

