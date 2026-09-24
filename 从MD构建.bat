@echo off
cd /d %~dp0
for /f "delims=" %%i in ('npm root -g') do set NODE_PATH=%%i
echo [1/3] 把 manuscript 里的 md 稿编译成书稿片段...
python tools\manuscript.py compile
if errorlevel 1 (
  echo.
  echo 编译失败：看上面第一条报错，会写明哪个文件哪一行什么问题。
  echo 常见原因：::: 没有成对闭合、文件名被改动、** 加粗没合上。
  pause
  exit /b 1
)
echo [2/3] 构建 HTML...
node build.js
if errorlevel 1 (
  echo HTML 构建失败。
  pause
  exit /b 1
)
echo [3/3] 生成 PDF（约一两分钟，请勿关闭本窗口）...
node build-pdf.js
if errorlevel 1 (
  echo PDF 生成失败：多半是 PDF 文件还开着，请关掉再试。
  pause
  exit /b 1
)
echo.
echo 全部完成。成书在 output 目录。
pause
