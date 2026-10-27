THE PRINTING YASSINE DESKTOP — VERSION CLIENT-SERVEUR

L'application Windows utilise un serveur central. Le serveur et la base PostgreSQL doivent être déployés avant de distribuer l'application aux employés.

1. Ouvrez README_CENTRAL.md et suivez les sections A et B pour déployer le serveur et importer l'ancien stock.
2. Créez les comptes employés avec create_user.py.
3. Sur Windows, lancez build_exe.bat.
4. Distribuez tout le dossier dist\The Printing Yassine.
5. Au premier lancement, saisissez l'adresse HTTPS du serveur puis connectez-vous.

Ne partagez pas les mots de passe, SECRET_KEY ou DATABASE_URL. La synchronisation nécessite Internet.
