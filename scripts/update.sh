#!/bin/bash
# Book-PDF 版本更新脚本模板
#
# 用法（仓库任意位置均可）：
#   scripts/update.sh patch "修正某个错误"     # 修订：1.0.0 → 1.0.1
#   scripts/update.sh minor "更新某部分内容"     # 次版本：1.0.0 → 1.1.0
#   scripts/update.sh major "新增某个章节"       # 主版本：1.0.0 → 2.0.0
#   scripts/update.sh build                      # 仅增加build号，不改版本

set -e
cd "$(dirname "$0")/.."

# playwright 依赖全局 npm：不依赖调用者先 export
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"

BUMP_TYPE="${1:-build}"
MESSAGE="${2:-无描述}"
TODAY=$(date +%Y-%m-%d)
VERSION_FILE="scripts/version.json"
CHANGELOG="CHANGELOG.md"

# 读取当前版本
CURRENT_VERSION=$(node -e "console.log(require('./$VERSION_FILE').version)")
CURRENT_BUILD=$(node -e "console.log(require('./$VERSION_FILE').build)")

# 计算新版本
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"
case "$BUMP_TYPE" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
  build) ;; # 只增加build号
  *) echo "❌ 未知类型: $BUMP_TYPE (可选: major/minor/patch/build)"; exit 1 ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
NEW_BUILD=$((CURRENT_BUILD + 1))

echo "📦 版本更新: v$CURRENT_VERSION (#$CURRENT_BUILD) → v$NEW_VERSION (#$NEW_BUILD)"

# 更新 version.json
node -e "
const fs = require('fs');
const v = JSON.parse(fs.readFileSync('$VERSION_FILE', 'utf-8'));
v.version = '$NEW_VERSION';
v.build = $NEW_BUILD;
v.lastUpdate = '$TODAY';
fs.writeFileSync('$VERSION_FILE', JSON.stringify(v, null, 2) + '\n');
"

# 写入 CHANGELOG（仅非build类型）
if [ "$BUMP_TYPE" != "build" ]; then
  node -e "
const fs = require('fs');
let log = fs.readFileSync('$CHANGELOG', 'utf-8');
const entry = '\n## [$NEW_VERSION] $TODAY — $MESSAGE\n\n- $MESSAGE\n';
const firstEntry = log.indexOf('\n## [');
if (firstEntry !== -1) {
  log = log.slice(0, firstEntry) + entry + log.slice(firstEntry);
} else {
  log += entry;
}
fs.writeFileSync('$CHANGELOG', log);
"
  echo "📝 CHANGELOG 已更新"
fi

# 构建 HTML
echo ""
echo "🔨 构建 HTML..."
node scripts/build.js

# 构建 PDF
echo ""
echo "📄 生成 PDF..."
node scripts/build-pdf.js

# 读取标题用于文件名
TITLE=$(node -e "console.log(require('./$VERSION_FILE').title)")

# 备份到 versions/ 目录（仅非build类型）
if [ "$BUMP_TYPE" != "build" ]; then
  mkdir -p versions
  cp "output/$TITLE-v$NEW_VERSION.pdf" "versions/$TITLE-v$NEW_VERSION.pdf"
  echo "💾 备份: versions/$TITLE-v$NEW_VERSION.pdf"
fi

# ===== GitHub Release 自动发布（2026-09-24 作者令：升版本即发布，不要人工喊）=====
# 只在 patch/minor/major 时发布，build 号不触发；只提交 version.json＋CHANGELOG 两个元数据文件，
# 正文改动仍由会话闭环单独提交。任一网络步骤失败只提醒不拦书——本地成书永远是第一产物。
if [ "$BUMP_TYPE" != "build" ]; then
  echo ""
  echo "🌍 发布 GitHub Release..."
  ASSET="enterprise-ai-playbook-v$NEW_VERSION.pdf"
  LABEL="下载整本 PDF：《$TITLE》v$NEW_VERSION"
  cp "output/$TITLE-v$NEW_VERSION.pdf" "output/$ASSET"

  if git add scripts/version.json CHANGELOG.md 2>/dev/null && git commit -m "v$NEW_VERSION $MESSAGE" >/dev/null 2>&1; then
    git push 2>/dev/null || echo "⚠️ git push 失败（离线？），稍后手动 git push 补上"
  fi

  if gh release view "v$NEW_VERSION" >/dev/null 2>&1; then
    gh release upload "v$NEW_VERSION" "output/$ASSET#$LABEL" --clobber \
      || echo "⚠️ Release 资产上传失败，稍后手动补：gh release upload v$NEW_VERSION"
  else
    gh release create "v$NEW_VERSION" "output/$ASSET#$LABEL" \
      --title "《$TITLE》v$NEW_VERSION" \
      --notes "- 📥 下载整本 PDF：《$TITLE》v$NEW_VERSION
- 📖 在线读：https://github.com/Geerdan1995/enterprise-ai-playbook/tree/main/manuscript
- 📝 本次更新：$MESSAGE" \
      || echo "⚠️ Release 创建失败（离线或 gh 未登录），稍后手动补发"
  fi
  rm -f "output/$ASSET"
fi

echo ""
echo "✅ 完成！v$NEW_VERSION (build #$NEW_BUILD)"
echo "   HTML: output/$TITLE-v$NEW_VERSION.html"
echo "   PDF:  output/$TITLE-v$NEW_VERSION.pdf"
