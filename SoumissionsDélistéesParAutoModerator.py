#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Liste les soumissions délistées par AutoModerator
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

r = praw.Reddit(user_agent="posix:SoumissionsDélistéesParAutoModerator:v0 (by /u/dClauzel)", site_name="Reddit")
o = OAuth2Util.OAuth2Util(r, print_log=False)
o.refresh()

print("connecté.")

# fin Connexion
###############

# liaison sur le sousjlailu
sousjlailu = r.get_subreddit("Europe")

# Doc utile
# https://praw.readthedocs.org/en/latest/pages/code_overview.html?highlight=queue#praw.__init__.ModOnlyMixin.get_mod_queue
# https://praw.readthedocs.org/en/latest/pages/code_overview.html?highlight=get_content#praw.__init__.BaseReddit.get_content
# https://www.reddit.com/dev/api#GET_about_modqueue
# https://www.reddit.com/r/redditdev/comments/3jyno4/praw_processing_only_unactioned_submissions_in/

# soumissions non traitées (validées ou délistées)
fileDeModération = sousjlailu.get_unmoderated(limit=None, **{"only":"links"})

for soumission in fileDeModération:

	# on agit sur les soumissions délistées par AutoModerator
	if str(soumission.banned_by) == "AutoModerator":

		try:
	
			print("---------------------------------------------------------------------------------------------------------------------")
	
			print("Titre : ",soumission.title)
			print("Auteur : ",soumission.author.name)
			print("Lien : ",soumission.permalink)
			print("Date : ",datetime.datetime.fromtimestamp(soumission.created_utc))
			print("URL : ",soumission.url)
			print("mod_reports",soumission.mod_reports)
			print("user_reports",soumission.user_reports)
			print("num_reports : ",soumission.num_reports)
			print("report_reasons",soumission.report_reasons)
			print("removal_reason : ",soumission.removal_reason)
			print("soumission.details : ",soumission.details)
	
		except AttributeError as e:
			# compte effacé ou shadowbanni
			print(e)
			pass

# vim: tabstop=3 shiftwidth=3 noexpandtab
