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

r = praw.Reddit(user_agent="posix:DémonstrationDeCollecteSimpleDInformations:v0 (by /u/dClauzel)", site_name="Reddit")
o = OAuth2Util.OAuth2Util(r, print_log=False)
o.refresh()

print("connecté.")

# fin Connexion
###############



# liaison sur le sousjlailu de travail; ici /r/Europe
sousjlailu = r.get_subreddit("Europe")



##########################
# Informations utilisateur

print("Je suis {0} et j’ai un karma de {1} pour mes commentaires.".format(
	r.get_me().name,
	r.get_me().comment_karma) )

# Fin Informations utilisateur
##############################




##################################
# Top des 5 soumissions populaires

print("Top 5")

for soumission in sousjlailu.get_hot(limit=5):
	print("	- {0} — {1} — {2}".format(
		soumission.title,
		soumission.author,
		soumission.url) )

# fin Top des 5 soumissions populaires
######################################



###############
# Bannissements

print("Liste des bannis")

# user_only=False permet de récupérer toutes les informations disponibles sur les bannis, et non pas seulement leur nom:
#	nom : le nom du compte (ce qui est à droite de « /u/ »)
#	id : l’identifiant technique associé au nom du compte
#	date : quand a été placé le bannissement
#	note : la note associée au bannissement

bannis = [i for i in sousjlailu.get_banned(limit=None,user_only=False)]
print( "Il y a {0} bannis.".format(len(bannis)) )

for leBanni in bannis:
	bNom = leBanni['name']
	bId = leBanni['id']
	bDate = datetime.datetime.fromtimestamp(leBanni['date'])
	bNote = leBanni['note']

	print("/u/{0} ({1}) : le {2}; {3}".format(
		bNom,				
		bId,	
		bDate,		
		bNote) )

print("fin Liste des bannis")

# fin Bannissements
###################

# vim: tabstop=3 shiftwidth=3 noexpandtab
