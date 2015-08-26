#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Liste les comptes bannis d’un sousjlailu
#
# Nécessite : être modérateur sur un sousjlailu avec au moins un compte banni
#
#############################################################################

import praw
import OAuth2Util
import datetime

###########
# Connexion

print("Connexion…", end=" ")

# Il est nécessaire de personnaliser l’user-agent pour suivre les règles de Reddit
# doc : https://github.com/reddit/reddit/wiki/API

r = praw.Reddit(user_agent="posix:MonScript:v0 (by /u/MonIdentifiantReddit)", site_name="Reddit")
o = OAuth2Util.OAuth2Util(r, print_log=False)
o.refresh()

print("connecté.")

# fin Connexion
###############



# liaison sur le sousjlailu de travail; ici /r/Europe
sousjlailu = r.get_subreddit("Europe")



##################
# Liste des bannis

# on prends toutes les informations disponibles
bannis = [banni for banni in sousjlailu.get_banned(limit=None,user_only=False)]

print( "Il y a {0} bannis.".format(len(bannis)) )

for banni in bannis:
	nom = banni['name']
	id = banni['id']
	date = datetime.datetime.fromtimestamp(banni['date'])
	note = banni['note']

	print( "{0} ({1}) — {2} : {3}".format(nom, id, date, note) )

# vim: tabstop=3 shiftwidth=3 noexpandtab
