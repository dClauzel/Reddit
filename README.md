Reddit : des scripts pour utiliser l’API de Reddit
==================================================

Les scripts
-----------

* DémonstrationDeCollecteSimpleDInformations.py : démonstration de collecte simple d’informations — karma, top 5 d’un sousjlailu, liste des bannis d’un sousjlailu
* InformationsSurSoumissions.py : recherche de mot-clefs dans le titre de soumissions récentes d’un sousjlailu

Dépendances
-----------

Les scripts ont les dépendances suivantes :

* python3
* [praw](https://github.com/praw-dev/praw) : `pip3 install praw`
* [praw-OAuth2Util](https://github.com/SmBe19/praw-OAuth2Util) : `pip3 install praw-oauth2util`


Utilisation
-----------

1. créer un jeton d’authentification
  1. create an App de type `script` on Reddit (https://www.reddit.com/prefs/apps/
  2. définir `redirect uri` à `http://127.0.0.1:65010/authorize_callback`, le reste est libre
2. renseigner l’authentification des scripts sur Reddit dans le fichier `oauth.txt` (clé et secret)


Références
----------

* https://github.com/reddit/reddit/wiki/API
* https://praw.readthedocs.org/


Licence
-------

En ce glorieux jour du 2015-08-17, moi Damien Clauzel place ce travail sous la licence « [Fais pas chier](https://clauzel.eu/FPC/) ».
