#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Liste les soumissions délistées récemment
#
# Nécessite : être modérateur sur un sousjlailu 
#
############################################################################################

import praw
import OAuth2Util
import sys
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

# liaison sur le sousjlailu
sousjlailu = r.get_subreddit("Europe")

# soumissions délistées
journalDeModération = sousjlailu.get_mod_log(limit=50, action="removelink")

for soumission in journalDeModération:

	try:

		print("---------------------------------------------------------------------------------------------------------------------")

		print("Lien : https://reddit.com{0}".format(soumission.target_permalink))
		print("Auteur : ",soumission.target_author)
		print("Date : ",datetime.datetime.fromtimestamp(soumission.created_utc))
		print("Modérateur : ",soumission.mod)
	
		# Via sa configuration, AutoModerator est capable de fournir une explication
		if str(soumission.mod) == "AutoModerator":
			print(soumission.details)
	
	except AttributeError as e:
		print(e)
		pass

# vim: tabstop=3 shiftwidth=3 noexpandtab
