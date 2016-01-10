﻿#-------------------------------------------------------------------------------
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
from os import curdir, sep, listdir
try :
	adventures = listdir(curdir+sep+"Adventures"+sep)
except OSError :
	raw_input("Adventures folder missing or incorrectly named.")
	exit(0)
from classes.classAdventure import Adventure
adv = dict((foldername, Adventure(foldername)) for foldername in adventures)
from functions import valremove, choicelist
for adventure in adventures :
	if adv[adventure].validate() == False : adventures = valremove(adventures, adventure)
if len(adventures) == 1 :
	a = adv[adventures[0]]
elif len(adventures) < 1 :
	raw_input("No valid adventures installed.")
	exit(0)
else :
	a = adv[choicelist(adventures, "Please enter a number corresponding to the adventure you wish to load:\n")[1]]
	print a.directory #Temporary
	a.load()