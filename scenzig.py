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
from functions import valremove, choicelist, Clr, get_valid_filename, dupremove
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
try :
	characters = listdir(a.directory+"Characters")
except OSError :
	raw_input("Characters folder missing or incorrectly named.")
	exit(0)
for file in characters : #Removes the template character file and any files without the '.scz' extension from the list of character choices
	if file == "template.scz" or file[-4:] != ".scz" : characters = valremove(characters, file)
from configobj import ConfigObj
c = None #'c' refers to the active character file which will be directly edited and reguarly read by the main script
if len(characters) != 0 :
	characters.append("New Character")
	choice = choicelist(characters, "Please enter a number corresponding to the character file you wish to load:\n")
	if choice[0] < len(characters) : #The last option is always 'New Character'. Options less than the total number of options will therefore be pre-existing characters.
		c = ConfigObj(a.directory+"Characters"+sep+choice[1], unrepr=True)
if c == None : from shutil import copy as fileclone
while c == None : #i.e. If there are no pre-existing characters or New Character was selected
	filename = get_valid_filename(raw_input("Please enter a name for your new character file:\n"))+".scz"
	if filename in characters :
		print "There is already a character file with that name"
		continue
	try :
		fileclone(a.directory+"Characters"+sep+"template.scz", a.directory+"Characters"+sep+filename)
	except IOError : #Is raised when the file to be cloned is not present
		raw_input("Character template missing or incorrectly named.")
		exit(0)
	c = ConfigObj(a.directory+"Characters"+sep+filename, unrepr=True)
print "Character succesfully loaded" #Probs temporary
while True : #Primary loop. Below is run after any action is taken
	wlist = a.f['scenes'][str(c['Scenes']['Current'])]['Master']['wlist'] + a.f['scenes'][str(c['Scenes']['Current'])][str(c['Scenes']['States'][c['Scenes']['Current']])]['wlist']
	blist = a.f['scenes'][str(c['Scenes']['Current'])]['Master']['blist'] + a.f['scenes'][str(c['Scenes']['Current'])][str(c['Scenes']['States'][c['Scenes']['Current']])]['blist']
	#Above the Actions Whitelist and Blacklist are initalised by combining the lists from the current scene and it's current state.
	#Below these lists are added to from any Abilities or Items the Character has and Action Groups listed in the current scene or scene state
	for agrp in a.f['scenes'][str(c['Scenes']['Current'])]['Master']['wlistagrp'] : wlist += a.f['actiongrps'][str(agrp)]['list']
	for agrp in a.f['scenes'][str(c['Scenes']['Current'])]['Master']['blistagrp'] : blist += a.f['actiongrps'][str(agrp)]['list']
	for ablty in c['Abilities'] :
		ablty = str(ablty)
		wlist += a.f['abilities'][ablty]['wlist']
		blist += a.f['abilities'][ablty]['blist']
		for agrp in a.f['abilities'][ablty]['wlistagrp'] : wlist += a.f['actiongrps'][agrp]['wlist']
		for agrp in a.f['abilities'][ablty]['blistagrp'] : blist += a.f['actiongrps'][agrp]['blist']
	for itm in c['Items'] :
		itm = str(itm)
		wlist += a.f['items'][itm]['wlist']
		blist += a.f['items'][itm]['blist']
		for agrp in a.f['items'][itm]['wlistagrp'] : wlist += a.f['actiongrps'][agrp]['wlist']
		for agrp in a.f['items'][itm]['blistagrp'] : blist += a.f['actiongrps'][agrp]['blist']
	glist = [act for act in dupremove(wlist) if act not in blist] #Creates a list which contains Whitelisted Actions (wlist) that are not Blacklisted (present in blist). These are the actions available to the player.
	print glist #Temporary
	for action in glist : #Temporary
		print a.f['actions'][str(action)]['description']
	break #Temporary