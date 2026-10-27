# The Printing Yassine Desktop — version client-serveur

Cette version conserve l'interface et le catalogue de l'application fournie, et remplace le stockage isolé par poste par un stockage serveur central. Les connexions utilisent des mots de passe hachés. Les changements sont vérifiés par numéro de révision pour empêcher qu'un poste ancien écrase silencieusement une version plus récente ; les fenêtres connectées vérifient les mises à jour environ toutes les 4 secondes.

## Ce qui est inclus

- `app.py` : serveur Flask, sessions, utilisateurs, API, base centrale SQLAlchemy.
- `templates/login.html` et `templates/index.html` : connexion et interface de gestion.
- `static/` : interface, catalogue, styles et graphiques existants.
- `desktop.py` : fenêtre Windows qui se connecte au serveur distant et demande son adresse au premier lancement si nécessaire.
- `render.yaml` : blueprint de déploiement Render avec base PostgreSQL.
- `create_user.py` : création de comptes supplémentaires.
- `migrate_local_data.py` : import de l'ancien `app_storage` SQLite.
- `build_exe.bat` : création de l'application Windows.

## A. Déployer le serveur central (à faire une seule fois)

Le serveur doit être hébergé sur un compte que vous contrôlez. Je ne peux pas créer le compte d'hébergement, accepter ses conditions ou déployer dans votre compte à votre place depuis ce ZIP.

1. Créez un dépôt Git privé et ajoutez-y le contenu de ce dossier. N'ajoutez jamais de fichier `.env`, de mot de passe, de clé secrète ou d'URL de base de données contenant des identifiants.
2. Dans Render, choisissez **New + → Blueprint** et sélectionnez le dépôt. Le fichier `render.yaml` décrit le service web et la base PostgreSQL.
3. Lorsque Render le demande, renseignez `ADMIN_EMAIL` avec l'e-mail du premier administrateur et `ADMIN_PASSWORD` avec un mot de passe unique d'au moins 12 caractères. Gardez ce mot de passe privé.
4. Attendez la fin du déploiement et copiez le domaine HTTPS attribué au service.
5. Ouvrez `https://VOTRE-DOMAINE/api/health`. Résultat attendu : `{"ok":true,"database":"postgresql"}`. Le service ne doit être utilisé que si cette vérification réussit.
6. Connectez-vous avec l'adresse e-mail et le mot de passe administrateur fournis à Render.

Si l'hébergeur n'accepte pas le plan gratuit déclaré dans `render.yaml`, choisissez un plan/base compatible dans son tableau de bord. Les offres gratuites peuvent avoir des limites, une mise en veille ou une expiration ; vérifiez les conditions actuelles avant d'utiliser le système pour les opérations quotidiennes.

## B. Transférer les anciennes données

Faites cette migration avant de laisser les employés commencer à travailler dans la nouvelle version.

1. Fermez l'ancienne application et faites une copie de sauvegarde du fichier :
   `%LOCALAPPDATA%\The Printing Yassine\printing_yassine_data.db`
2. Sur votre PC Windows, récupérez l'URL PostgreSQL **externe** depuis le tableau de bord de l'hébergeur (l'URL interne Render ne fonctionne pas depuis votre PC). Ouvrez PowerShell dans le dossier du projet, puis définissez la variable dans cette fenêtre uniquement :
   ```powershell
   $env:DATABASE_URL = "postgresql://UTILISATEUR:MOT_DE_PASSE@HOTE:PORT/BASE"
   $env:SECRET_KEY = "votre-cle-secrete-de-developpement"
   ```
   Ne partagez pas cette URL et ne la publiez jamais dans Git.
3. Installez les dépendances serveur (`python -m pip install -r requirements.txt`) et lancez une seule fois :
   `python migrate_local_data.py "$env:LOCALAPPDATA\The Printing Yassine\printing_yassine_data.db"`
4. Contrôlez l'état du stock, les entrées, les sorties et l'historique dans l'interface. Conservez la copie de sauvegarde jusqu'à validation.

Ne faites pas cette importation après que plusieurs utilisateurs ont commencé à modifier le stock, car elle remplace les valeurs des clés importées.

## C. Ajouter des employés

Sur un environnement connecté à la même base centrale, avec `DATABASE_URL` configurée :

`python create_user.py`

Choisissez le rôle `user` pour un employé ou `admin` pour un administrateur. Les mots de passe sont hachés avec Werkzeug. Le compte administrateur initial est créé à partir de `ADMIN_EMAIL` et `ADMIN_PASSWORD` au premier démarrage.

## D. Construire l'application Windows

La compilation du fichier `.exe` doit être effectuée sur Windows. Le ZIP source ne contient pas un exécutable client déjà compilé ni une adresse de serveur inventée.

1. Installez Python 3 depuis `https://www.python.org/downloads/windows/` si nécessaire.
2. Double-cliquez sur `build_exe.bat`.
3. À la fin, l'application se trouve dans `dist\The Printing Yassine\The Printing Yassine.exe`.
4. Copiez **tout le dossier** `dist\The Printing Yassine` sur chaque PC, puis créez un raccourci vers le `.exe`.
5. Au premier lancement, saisissez le domaine HTTPS du serveur central. Cette adresse est mémorisée dans `%APPDATA%\The Printing Yassine\server_url.json`.
6. Connectez chaque utilisateur avec son propre compte. Tous les PC utilisent le même serveur ; Internet est requis.

## Synchronisation et sécurité

- L'interface interroge le serveur toutes les 4 secondes pour détecter les mises à jour d'un autre poste.
- Une révision compare les instantanés : une écriture basée sur une ancienne révision est refusée plutôt que d'écraser silencieusement le travail d'un collègue. Le message de conflit demande de recharger les données et de refaire l'opération.
- Les API de stock nécessitent une session authentifiée. La remise à zéro est réservée aux administrateurs.
- Le serveur doit rester accessible uniquement via HTTPS. Ne publiez jamais `DATABASE_URL`, `SECRET_KEY` ou les mots de passe.
- Configurez des sauvegardes régulières de PostgreSQL et testez leur restauration.
- Cette version protège contre les écrasements concurrents, mais conserve le format de stockage global hérité de l'application initiale. Pour un audit comptable strict, l'étape suivante sera de transformer chaque entrée/sortie en opération immuable indépendante en base, avec validation transactionnelle de quantité et permissions de correction.

## Développement local

Pour tester uniquement sur votre PC, créez un environnement Python, installez `requirements.txt`, puis définissez `COOKIE_SECURE=false` et une `SECRET_KEY` de développement. Pour la production, utilisez PostgreSQL et HTTPS ; n'utilisez pas la base SQLite locale comme base partagée.
