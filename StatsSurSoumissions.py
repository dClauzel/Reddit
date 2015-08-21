#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Top des posteurs dont la soumission comporte un mot-clef recherché, avec suivi des horaires des soumissions
#
###############################################################################################################

import praw
import OAuth2Util
import datetime
import collections
from collections import OrderedDict
from collections import Counter


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




###########################################################################################
# On recherche dans les soumissions récentes celles dont le titre contient un des mot-clefs


# mot-clefs recherchés
marqueurs = [
	"Calais",
	"ethni",
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

# liste des auteurs suspects
auteurs = []

# liste par heure des soumissions suspectes
horaires = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# pour chaque soumission
for soumission in sousjlailu.get_new(t="day"): # Toutes les soumissions récentes sur 24 heures, max 100 (limite de Reddit)
	try:
		titre = soumission.title
		auteur = soumission.author.name
		heureCréation = int(datetime.datetime.fromtimestamp(soumission.created_utc).strftime('%k'))
	
		# si le mot-clef est dans le titre
		if any(mot.lower() in titre.lower() for mot in marqueurs):
			auteurs.append(auteur)
			horaires[heureCréation]+=1
	
	except AttributeError as e:
		# les soumissions supprimées font exploser la moulinette
		pass

####################
# calculs des scores

print( "Trouvé {0} soumissions parmi les 100 plus récentes de ces dernières 24 heures".format(len(auteurs)) )
print( "Horaires : {0}".format(horaires) )

# De la liste des auteurs on crée une collection pour en faire un dictionnaire trié par ordre décroissant sur le nombre de soumissions
auteursComptés = OrderedDict( sorted(collections.Counter(auteurs).items(), key=lambda t: t[1], reverse=True) ) 

for auteur in auteursComptés.items():
	print( "{0} : {1}".format(auteur[0], auteur[1]) )

# vim: tabstop=3 shiftwidth=3 noexpandtab
