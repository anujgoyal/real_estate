// brew install node
// npm i puppeteer-core --save

const puppeteer = require('puppeteer');

(async () => {
	// start browser
	msg = "Browser Startup";
	console.time(msg);
	// https://github.com/GoogleChrome/puppeteer/issues/2757
	const browser = await puppeteer.launch({ headless: false, args: ["--fast-start", "--disable-extensions", "--no-sandbox"],
		executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
	console.timeEnd(msg);

	// load up the CRIIS page
	msg = "Page Load"; console.time(msg);
	const page = await browser.newPage();
	await page.goto('http://www.criis.com/cgi-bin/doc_search.cgi?COUNTY=sanfrancisco&YEARSEGMENT=current&TAB=3');
	console.timeEnd(msg);

	// use page.select, choose "Notice of Default" from Select Dropdown
	// https://stackoverflow.com/questions/45864516/how-to-select-an-option-from-dropdown-select
	msg = "Form Input & Submit"; console.time(msg);
	await page.select('select[name="DOC_TYPE"]', '007'); 
	await page.$eval('input[id="dateboxA"]', el => el.value = '04012019');
	await page.$eval('input[id="dateboxB"]', el => el.value = '04202019');
	// <input type="submit" value="Search"/>
	await page.click('input[type="submit"]');
	console.timeEnd(msg);

	msg = "Result page"; console.time(msg);
	// wait for search results page to load
	const resp = await page.waitForNavigation();
	// https://github.com/GoogleChrome/puppeteer/issues/2696
	// const response = await page.waitForNavigation({waituntil: 'deomcontentloaded'});
	console.log('response', resp);
	//const redirects = response.request().redirectChain();
	console.timeEnd(msg);

    // save contents to file
	await page.screenshot({path: 'criis.png'});
	await browser.close();

})();

