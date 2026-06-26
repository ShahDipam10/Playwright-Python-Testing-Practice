@echo off
set PLAYWRIGHT_BROWSERS_PATH=D:\Dipam Shah\Playwright_Browsers
"D:\Dipam Shah\Playwright Learning\.venv\Scripts\python.exe" -m pytest %* --headed -v -s
