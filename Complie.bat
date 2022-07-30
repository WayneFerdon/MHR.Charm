pyinstaller -F `Charms.py
xcopy .\dist\ .\Release\ /y
xcopy .\CharmsData.* .\Release /y
xcopy .\Config.json .\Release\ /y
xcopy .\Skills.json .\Release\ /y
xcopy .\*.md .\Release\ /y
xcopy .\Language .\Release\Language\ /e /y /h /r /q
pause