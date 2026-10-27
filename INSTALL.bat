@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv
  if errorlevel 1 python -m venv .venv
  if errorlevel 1 goto erreur
)
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto erreur
.venv\Scripts\python.exe -m pip install -r requirements-client.txt
if errorlevel 1 goto erreur
echo Installation terminee. Lancez run.bat pour ouvrir l'application.
pause
exit /b 0
:erreur
echo Installation impossible. Verifiez Python et votre connexion Internet.
pause
exit /b 1
