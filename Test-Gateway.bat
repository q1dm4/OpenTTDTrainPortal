@echo off
cd /d "%~dp0"
start "Gateway prototype" /wait openttd.exe -c gateway-prototype.cfg -g demo-start.sav
