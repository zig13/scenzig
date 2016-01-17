#-------------------------------------------------------------------------------
# Name:        scenzig Main Script
# Purpose:     An engine for text-based adventure games and interactive prose using a scene-based system.
#
# Author:      Thomas Sturges-Allard
#
# Created:     09/01/2016
# Copyright:   (c) Thomas Sturges-Allard 2016
# Licence:      Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#			http://creativecommons.org/licenses/by-nc-sa/3.0/
#-------------------------------------------------------------------------------
from os import curdir, sep, listdir #sep and curdir produce the correct characters for the operating system in use
try :
	adventures = listdir(curdir+sep+"Adventures"+sep)
except OSError :
	raw_input("Adventures folder missing or incorrectly named.")
	exit(0)
from classes.classAdventure import Adventure
adv = dict((foldername, Adventure(foldername)) for foldername in adventures) #Creates an instance of classAdventure for each folder found in the Adventures folder as a dictionary entry of adv
from functions import valremove, choicelist, Clr
for adventure in adventures : #Runs the validate function of each instance of classAdventure. If they return False (fail) then they are removed from the Adventures list
	if adv[adventure].validate() == False : adventures = valremove(adventures, adventure)
if len(adventures) < 1 :
	raw_input("No valid adventures installed.")
	exit(0)
elif len(adventures) == 1 :
	a = adv[adventures[0]] #If only one ~valid Adventure exists, automatically loads it without asking
	if a.load() == False :
		raw_input("No valid adventures installed.")
		exit(0)	
else :
	temptext = "Please enter a number corresponding to the adventure you wish to load:\n"
	while True :
		a = adv[choicelist(adventures, temptext)[1]]
		if a.load() == False :
			temptext = "The selected adventure failed to load. One or more data files lacked key values.\nPlease select a different Adventure:"
			Clr()
		else :
			break
#From here 'a' refers to the classAdventure instance of the active Adventure. All Adventure data will be accessed through it.