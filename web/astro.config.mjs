import { defineConfig } from 'astro/config';

// GitHub Pages 项目站挂在仓库子路径；本地开发用默认值即可
const base = process.env.ASTRO_BASE ?? '/enterprise-ai-playbook/';

export default defineConfig({
  site: 'https://geerdan1995.github.io',
  base,
  output: 'static',
  trailingSlash: 'always',
  devToolbar: { enabled: false },
});
