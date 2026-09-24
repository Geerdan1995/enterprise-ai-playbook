/* dynamic-ui → 书籍插图管线：widget HTML 定宽渲染，截成 2x PNG
 * 用法：NODE_PATH="$(npm root -g)" node widget-shot.js <widget.html> <输出.png> [定宽=684]
 */
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [src, out, widthArg] = process.argv.slice(2);
  const width = parseInt(widthArg || '684', 10);
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: width + 48, height: 1200 },
    deviceScaleFactor: 8,
  });
  await page.goto('file:///' + path.resolve(src).replace(/\\/g, '/'));
  await page.waitForTimeout(300);
  const el = await page.$('[data-dynamic-ui-widget]');
  if (!el) { console.error('未找到 [data-dynamic-ui-widget]'); process.exit(1); }
  await el.screenshot({ path: out });
  await browser.close();
  console.log('✅ ' + out);
})();
