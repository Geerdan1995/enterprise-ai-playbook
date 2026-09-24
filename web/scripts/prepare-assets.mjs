// 把书内插图拷进 Astro 静态目录：fragments 里的 <img> 按
// `${base}assets/illustrations/shots/…` 引用，公开目录需有同名文件。
import { cpSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(root, '..', 'assets', 'illustrations', 'shots');
const dest = join(root, 'public', 'assets', 'illustrations', 'shots');

if (!existsSync(src)) {
  console.error(`[prepare-assets] 找不到插图目录：${src}（要在仓库根的 web/ 里跑）`);
  process.exit(1);
}
mkdirSync(dest, { recursive: true });
cpSync(src, dest, { recursive: true });
console.log('[prepare-assets] 插图已同步到 public/assets/illustrations/shots');
