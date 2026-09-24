// 判味图重截（CommonJS：走 NODE_PATH 找全局 playwright）
const { chromium } = require('playwright');

const BASE = 'http://localhost:4321/enterprise-ai-playbook/';

(async () => {
  const b = await chromium.launch();
  async function shot(name, url, opts) {
    const ctx = await b.newContext({ viewport: opts.viewport, deviceScaleFactor: 2 });
    await ctx.addInitScript((t) => localStorage.setItem('theme', t), opts.theme || 'light');
    const p = await ctx.newPage();
    await p.goto(BASE + url, { waitUntil: 'networkidle' });
    if (opts.scroll) await p.evaluate((y) => scrollTo(0, y), opts.scroll);
    await p.waitForTimeout(500);
    await p.screenshot({ path: 'review/' + name + '.png' });
    await ctx.close();
    console.log('📸', name);
  }
  await shot('home-light', '', { viewport: { width: 1440, height: 900 } });
  await shot('reader-ch1-mobile', 'read/ch1/', { viewport: { width: 390, height: 844 } });
  await shot('reader-ch1-light', 'read/ch1/', { viewport: { width: 1440, height: 900 } });
  await b.close();
})();
