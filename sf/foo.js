// https://www.aymen-loukil.com/en/blog-en/google-puppeteer-tutorial-with-examples/#4Get_the_page_title
const puppeteer = require('puppeteer');
puppeteer.launch().then(async browser => {
  const page = await browser.newPage({ headless: false, args: ["--fast-start", "--disable-extensions", "--no-sandbox"] });
  await page.goto('http://goanuj.freeshell.org');
  const title = await page.title()
  console.log(title)
  const html = await page.content();
  console.log(html)
  await browser.close();
});
