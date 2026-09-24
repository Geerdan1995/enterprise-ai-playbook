// 判味截图：首页＋阅读器（明/暗/手机）→ web/review/*.png
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const BASE = 'http://localhost:4321/enterprise-ai-playbook/';
mkdirSync('review', { recursive: true });

const browser = await chromium.launch();

async function shot(name, url, { viewport, theme = 'light', fullPage = false, scroll = 0 }) {
  const ctx = await browser.newContext({ viewport, deviceScaleFactor: 2 });
  await ctx.addInitScript((t) => localStorage.setItem('theme', t), theme);
  const page = await ctx.newPage();
  await page.goto(BASE + url, { waitUntil: 'networkidle' });
  if (scroll) await page.evaluate((y) => scrollTo(0, y), scroll);
  await page.waitForTimeout(600);
  await page.screenshot({ path: `review/${name}.png`, fullPage });
  await ctx.close();
  console.log('📸', name);
}

await shot('home-light', '', { viewport: { width: 1440, height: 900 } });
await shot('reader-ch1-light', 'read/ch1/', { viewport: { width: 1440, height: 900 } });
await shot('reader-ch1-light-scrolled', 'read/ch1/', {
  viewport: { width: 1440, height: 900 },
  scroll: 3600,
});
await shot('reader-ch1-dark', 'read/ch1/', { viewport: { width: 1440, height: 900 }, theme: 'dark' });
await shot('reader-editor-note', 'read/editor-note/', {
  viewport: { width: 1440, height: 900 },
  scroll: 1400,
});
await shot('reader-ch1-mobile', 'read/ch1/', { viewport: { width: 390, height: 844 } });

await browser.close();
console.log('完成 → web/review/');
