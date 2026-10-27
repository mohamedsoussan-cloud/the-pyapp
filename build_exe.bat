@echo off
setlocal
cd /d "%~dp0"
echo ====================================================
echo The Printing Yassine - Creation de l'application PC
echo ====================================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3 doit etre installe pour construire l'application.
  echo Telechargez Python depuis https://www.python.org/downloads/windows/
  pause
  exit /b 1
)
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv
  if errorlevel 1 goto erreur
)
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto erreur
.venv\Scripts\python.exe -m pip install -r requirements-client.txt
if errorlevel 1 goto erreur
if exist build rmdir /s /q build
if exist "dist\The Printing Yassine" rmdir /s /q "dist\The Printing Yassine"
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --onedir --name "The Printing Yassine" --icon "icon.ico" --collect-all webview desktop.py
if errorlevel 1 goto erreur
if exist server_url.json copy /Y server_url.json "dist\The Printing Yassine\server_url.json" >nul
echo.
echo BUILD TERMINE.
echo Application : dist\The Printing Yassine\The Printing Yassine.exe
echo Distribuez tout le dossier dist\The Printing Yassine, pas seulement le .exe.
echo Au premier lancement, si le serveur n'est pas configure, l'application demandera son adresse HTTPS.
echo.
pause
exit /b 0
:erreur
echo.
echo ECHEC : verifiez Python, Internet et les messages ci-dessus.
pause
exit /b 1
