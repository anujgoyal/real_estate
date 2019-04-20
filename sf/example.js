// brew install node
// npm i puppeteer-core --save

const puppeteer = require('puppeteer');

(async () => {
	// https://github.com/GoogleChrome/puppeteer/issues/2757
	const browser = await puppeteer.launch({ headless: true, args: ["--fast-start", "--disable-extensions", "--no-sandbox"],
		executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });

	const page = await browser.newPage();
	//await page.goto('https://example.com');
	await page.goto('http://www.criis.com/cgi-bin/doc_search.cgi?COUNTY=sanfrancisco&YEARSEGMENT=current&TAB=3');

	// use page.select, choose "Notice of Default" from Select Dropdown
	// https://stackoverflow.com/questions/45864516/how-to-select-an-option-from-dropdown-select
	await page.select('select[name="DOC_TYPE"]', '007'); 
	await page.$eval('input[id="dateboxA"]', el => el.value = '04012019');
	await page.$eval('input[id="dateboxB"]', el => el.value = '04202019');

	// <input type="submit" value="Search"/>
	console.log('CLICK before');
	await page.click('input[type="submit"]');
	console.log('CLICK end');

	console.log('waiting...');
	// wait for search results page to load
	await page.waitForNavigation();
	console.log('FOUND!', page.url());

		// take a pic
		await page.screenshot({path: 'criis.png'});
	await browser.close();

})();

