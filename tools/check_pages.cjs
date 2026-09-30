// Exercise the generated Pages artifact under a repository subdirectory.
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
const { chromium } = require(process.env.CODEX_NODE_MODULES + '/playwright');
const root = path.resolve('.pages-site');
const prefix = '/Digital-Buro/';
const types = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.woff2':'font/woff2','.webmanifest':'application/manifest+json'};
const server = http.createServer((req, res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  if (!pathname.startsWith(prefix)) { res.writeHead(404).end(); return; }
  let file = path.resolve(root, pathname.slice(prefix.length));
  if (file !== root && !file.startsWith(root + path.sep)) { res.writeHead(404).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) { res.writeHead(404).end(); return; }
  res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
  res.end(fs.readFileSync(file));
});
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({headless:true, executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const errors = [];
  try {
    const page = await browser.newPage({viewport:{width:1440,height:1000}});
    page.on('pageerror', e => errors.push(e.message));
    page.on('response', r => { if (r.url().startsWith(origin) && r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
    const pages = JSON.parse(fs.readFileSync('src/data/pages.json', 'utf8'));
    for (const item of pages) {
      await page.goto(origin + prefix + item.path.replace(/^\//, ''));
      await page.evaluate(() => document.fonts.ready);
      assert.match(await page.locator('h1').evaluate(el => getComputedStyle(el).fontFamily), /Inter/i);
      assert.equal(await page.locator('[data-contact-form]').count(), 0);
      assert.match(await page.locator('meta[name=robots]').getAttribute('content'), /noindex/);
      const urls = await page.evaluate(() => [...document.querySelectorAll('[href],[src],[srcset]')].flatMap(el => [el.getAttribute('href'), el.getAttribute('src'), ...(el.getAttribute('srcset') || '').split(',').map(s => s.trim().split(/\s/)[0])]).filter(s => s && s.startsWith('/') && !s.startsWith('//')));
      for (const url of urls) {
        assert.ok(url.startsWith(prefix), `Unprefixed URL: ${url}`);
        const pathname = new URL(url, origin).pathname;
        const target = path.join(root, decodeURIComponent(pathname.slice(prefix.length)));
        assert.ok(fs.existsSync(target), `Missing target: ${url}`);
      }
    }
    for (const width of [390,1440]) {
      await page.setViewportSize({width,height:1000});
      for (const route of ['', 'contact/', 'reparation-imprimante/', 'nl/', 'en/']) {
        await page.goto(origin + prefix + route);
        await page.evaluate(async () => { document.querySelectorAll('img').forEach(i => i.loading = 'eager'); await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
        assert.equal(await page.locator('img').evaluateAll(imgs => imgs.filter(i => !i.naturalWidth).length), 0);
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      }
      await page.goto(origin + prefix);
      if (width === 390) {
        await page.locator('[data-menu-toggle]').click();
        assert.equal(await page.locator('[data-menu-toggle]').getAttribute('aria-expanded'), 'true');
        await page.keyboard.press('Escape');
      }
      await page.screenshot({path:`artifacts/pages-${width}.png`,animations:'disabled'});
    }
    await page.locator('a[href="/Digital-Buro/contact/"]').first().click();
    assert.equal(new URL(page.url()).pathname, '/Digital-Buro/contact/');
    assert.ok(await page.locator('a[href="mailto:digital-buro@skynet.be"]').count());
    const manifest = JSON.parse(fs.readFileSync(path.join(root, 'site.webmanifest'), 'utf8'));
    assert.equal(manifest.start_url, prefix);
    assert.ok(!fs.existsSync(path.join(root, 'api')));
    assert.deepEqual(errors, []);
    console.log(`PASS: ${pages.length} pages, local assets/links/srcset, fonts, desktop/mobile, navigation, email fallback, no PHP artifact.`);
  } finally {
    await browser.close();
    server.close();
  }
})().catch(e => { console.error(e); server.close(); process.exitCode = 1; });
