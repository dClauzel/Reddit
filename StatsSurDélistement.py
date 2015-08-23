#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Top des posteurs non bannis dont les soumissions et commentaires ont été délistés récemment
#
#############################################################################################################

import praw
import OAuth2Util
import collections
from collections import OrderedDict
from collections import Counter
from itertools import chain


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



#######################################################################################################
# On recherche les comptes non bannis qui ont le plus de soumissions et commentaires délistés récemment

# liste des bannis
bannis = [banni.name for banni in sousjlailu.get_banned(limit=None,user_only=True)]

# liste des actions de modération
# cf https://www.reddit.com/dev/api#GET_about_log
actionRemovecomment = sousjlailu.get_mod_log(action="removecomment", limit=100)
actionRemovelink = sousjlailu.get_mod_log(action="removelink", limit=100)
actionsDeModération = chain(actionRemovecomment, actionRemovelink)

# auteurs délistés
auteursDélistés = []

# Pour chaque action de modération
for action in actionsDeModération:
	
	try:
		auteur = action.target_author
	
		# si l’auteur n’est pas banni
		if auteur not in bannis:
			auteursDélistés.append(auteur)

	except AttributeError as e:
		# les soumissions supprimées font exploser la moulinette
		pass

####################
# calculs des scores

print( "Trouvé {0} auteurs non bannis délistés récemment".format(len(auteursDélistés)) )

# De la liste des auteurs on crée une collection pour en faire un dictionnaire trié par ordre décroissant sur le nombre de soumissions
auteursDélistésTriés = OrderedDict( sorted(collections.Counter(auteursDélistés).items(), key=lambda t: t[1], reverse=True) ) 

for auteur in auteursDélistésTriés.items():
	print( "{0} : {1}".format(auteur[0], auteur[1]) )

# vim: tabstop=3 shiftwidth=3 noexpandtab
