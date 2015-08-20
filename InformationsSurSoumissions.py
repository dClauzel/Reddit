#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Démonstration de collecte simple d’informations
#
# Nécessite : être modérateur sur un sousjlailu avec au moins 5 soumissions et un compte banni
#
##############################################################################################

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




##################################
# On recherche dans les soumissions récentes celles dont le titre contient un des mot-clefs


marqueurs = [
	"Calais",
	"integrat",
	"islam",
	"migrant",
	"migration",
	"racism",
	"refugee",
	"xenophob"
]

print("Marqueurs: ", end="")
print(", ".join(marqueurs))
print("_____")

# pour chaque soumission
for soumission in sousjlailu.get_new(limit=1000):
	titre = soumission.title
	auteur = soumission.author
	permalien = soumission.permalink

	# si le mot-clef est dans le titre
	if any(mot.lower() in titre.lower() for mot in marqueurs):
		print("{0}\n/u/{1}\n{2}\n_____".format(
			titre,
			auteur,
			permalien,
			) )

# vim: tabstop=3 shiftwidth=3 noexpandtab
