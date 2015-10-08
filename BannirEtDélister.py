#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Banni un compte puis déliste ses publications, ou le débannit et valide ses publications
#
# Nécessite : être modérateur sur un sousjlailu 
#
############################################################################################

import praw
import OAuth2Util
import sys
import argparse


#####################################
# Collecte des informations pour agir

# On a besoin de 3 informations :
# - le compte à bannir et délister, ou à débannir et valider
# - si bannissement, la durée de bannissement; par défaut 30 jours
# - si bannissement, le texte de note interne aux modérateurs et de notification au compte; par défaut « Ban evasion with multiple accounts »

# définition des arguments de l’outil
parseurArguments = argparse.ArgumentParser(description="Banni un compte puis déliste ses publications, ou le débannit et valide ses publications")
parseurArguments.add_argument("compte", type=str, help="compte à bannir et délister")
parseurArguments.add_argument("durée", type=int, nargs="?", default=30, help="durée du bannissement")
parseurArguments.add_argument("message", type=str, nargs="?", default="Ban evasion with multiple accounts", help="texte de note interne aux modérateurs et de notification au compte")
parseurArguments.add_argument("--grace", action="store_true", help="Débanni et valide toutes les publications d’un compte")
arguments = parseurArguments.parse_args()

compte = arguments.compte
durée = arguments.durée
message = arguments.message
retourEnGrace = arguments.grace

# fin Collecte des informations pour agir
#########################################


# sousjlailu dans lequel on agit
sousjlailuDeTravail = "Europe"

if retourEnGrace:
	print( "Débannir et valider les publications u/{0} dans r/{1}".format(compte,sousjlailuDeTravail) )
else:
	print( "Bannir et délister les publications de u/{0} dans r/{1} pour {2} jours avec la note et le message « {3} »".format(compte,sousjlailuDeTravail,durée,message) ) 


###########
# Connexion

print("Connexion…", end=" ")

# Il est nécessaire de personnaliser l’user-agent pour suivre les règles de Reddit
# doc : https://github.com/reddit/reddit/wiki/API

r = praw.Reddit(user_agent="posix:BannirEtDélister:v1 (by /u/dClauzel)", site_name="Reddit")
o = OAuth2Util.OAuth2Util(r, print_log=False)
o.refresh()

print("connecté.")

# fin Connexion
###############



# liaison sur le sousjlailu
sousjlailu = r.get_subreddit(sousjlailuDeTravail)


# débannissement ou bannissement avec note privée et message de notification
# si on ne trouve pas l’utilisateur, on s’arrête là
try:

	utilisateur = r.get_redditor(compte)
	if retourEnGrace:
		sousjlailu.remove_ban(utilisateur)
#		TODO ajouter une usernote Toolbox via PUNI
	else:
		sousjlailu.add_ban(utilisateur, **{"duration": durée, "note": message, "ban_message": message})
#		TODO ajouter une usernote Toolbox via PUNI

except praw.errors.InvalidUser:

	print( "Impossible de trouver le compte {0} sur r/{1}".format(compte,sousjlailuDeTravail) )
	exit(2)


# on récupère la liste des soumissions et commentaires
soumissions = utilisateur.get_submitted(limit=None)
commentaires = utilisateur.get_comments(limit=None)


# pour chaque soumission de l’utilisateur
for soumission in soumissions:
	
	try:

		# c’est une soumission dans le sousjlailu ? On agit
		if soumission.subreddit.display_name.lower() == sousjlailuDeTravail.lower():
			if retourEnGrace:
					soumission.approve()
			else:
					soumission.remove()
					soumission.add_comment("This submission has been delisted, and the submitter banned.").distinguish()

	except:
		pass

# pour chaque commentaire de l’utilisateur
for commentaire in commentaires:

	try:

		# c’est un commentaire dans le sousjlailu ? On agit
		if commentaire.subreddit.display_name.lower() == sousjlailuDeTravail.lower():
			if retourEnGrace:
				commentaire.approve()
			else:
				commentaire.remove()

	except:
		pass

# vim: tabstop=3 shiftwidth=3 noexpandtab
