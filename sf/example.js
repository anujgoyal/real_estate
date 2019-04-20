// brew install node
// npm i puppeteer-core --save

const puppeteer = require('puppeteer');

(async () => {
//  const browser = await puppeteer.launch();

    // https://github.com/GoogleChrome/puppeteer/issues/2757
	const browser = await puppeteer.launch({ 
		headless: true, 
		args: ["--fast-start", "--disable-extensions", "--no-sandbox"],
		executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
	const page = await browser.newPage();
	await page.goto('https://example.com');
	await page.screenshot({path: 'example.png'});
	await browser.close();

})();

