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
from os import curdir, sep, listdir #sep and curdir produce the correct characters for the operating system in use
try :
	adventures = listdir(curdir+sep+"Adventures"+sep)
except OSError :
	raw_input("Adventures folder missing or incorrectly named.")
	exit(0)
from classes.classAdventure import Adventure
adv = dict((foldername, Adventure(foldername)) for foldername in adventures) #Creates an instance of classAdventure for each folder found in the Adventures folder as a dictionary entry of adv
from functions import valremove, choicelist, Clr, get_valid_filename, dupremove, nonemptyprint
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
import effects as efunc
efunc.GiveAdv(a)
import statecheck
statecheck.GiveAdv(a)
import listcollate
listcollate.GiveAdv(a)
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
		c = ConfigObj(a.directory+"Characters"+sep+choice[1], unrepr=True, raise_errors=True)
		efunc.GiveChar(c)
		statecheck.GiveChar(c)
		statecheck.Prepare('Scenes')
		statecheck.Prepare('Encounters')
		firstrun = False
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
	efunc.GiveChar(c)
	statecheck.GiveChar(c)
	efunc.SetScene(c['Scenes']['active'])
	firstrun = True
statecheck.Prepare('Items')
statecheck.Prepare('Abilities')
statecheck.Prepare('Attributes')
listcollate.GiveChar(c)
listcollate.Setup(statecheck.aspect_lists)
listcollate.SetBaseAttributes()
import argsolve
argsolve.GiveChar(c)
while True : #Primary loop. Below is run after an effect happens
	effecthappened = False
	
	listcollate.reBaseAttributes()
	scenelist = listcollate.CollateScene()
	encounterlist = listcollate.CollateEncounter()
	abilitylist = listcollate.CollateAbilities()
	itemlist = listcollate.CollateItems()
	attributelist = listcollate.CollateAttributes()
	listcollate.CapModifiers() #Ensures Attributes do not exceed thier maximum values
	
	effects = []
	effects.append(statecheck.Check('Scenes')[1])
	effects.append(statecheck.Check('Encounters')[1])
	effects.append(statecheck.Check('Attributes')[1])
	effects.append(statecheck.Check('Items')[1])
	effects.append(statecheck.Check('Abilities')[1])
	for set in effects :
		for effect in set.keys() :
			effecthappened = True
			arguments = argsolve.Solve(set[effect])
			eval("efunc."+effect+"(arguments)")
	if effecthappened or firstrun :
		firstrun = False
		continue #Restarts the primary loop early if an effect happens
	c.write()
	wlist = scenelist['white'] + encounterlist['white'] + abilitylist['white'] + itemlist['white'] + attributelist['white']
	blist = scenelist['black'] + encounterlist['black'] + abilitylist['black'] + itemlist['black'] + attributelist['black']
	glist = [act for act in dupremove(wlist) if act not in blist] #Creates a list which contains Whitelisted Actions (wlist) that are not Blacklisted (present in blist). These are the actions available to the player.
	efunc.GiveList(glist)
	while True : #Secondary loop. Below is run when anything is put into the prompt regardless of validity.
		nonemptyprint(a.f['Scenes'][str(c['Scenes']['active'][0])]) #Scene description will be printed if there is one
		for state in sorted(c['Scenes'][str(c['Scenes']['active'][0])]) :
			nonemptyprint(a.f['Scenes'][str(c['Scenes']['active'][0])][str(state)])
		for encounter in c['Encounters']['active'] :		
			nonemptyprint(a.f['Encounters'][str(encounter)]) #Encounter description will be printed if there is one
			for state in sorted(c['Encounters'][str(encounter)]) :
				nonemptyprint(a.f['Encounters'][str(encounter)][str(state)])
		for vital in c['Attributes']['vital'] :
			for state in sorted(c['Attributes'][str(vital)]) :
				nonemptyprint(a.f['Attributes'][str(vital)][str(state)])
		prompt = raw_input(">").strip() #The main prompt
		action = 0
		try : #Effectively 'if input is a whole number'
			prompt = int(prompt)
			if prompt in glist : 
				action = str(prompt) #If the input matches the UID of a valid action then take note of it's UID
		except ValueError : #Effectively 'if input isn't a whole number'
			prompt = prompt.lower() #Makes all inputted characters lower case where applicable
			actdict = {}
			for actn in glist : #Builds a dictionary that pairs the slug of each valid action with it's UID
				actdict[a.f['Actions'][str(actn)]['slug'].lower()] = actn
			if prompt in actdict.keys() : 
				action = str(actdict[prompt]) #If the input matches the slug of a valid action then take note of it's UID
		Clr()
		effects.append(statecheck.DetermineOutcomes(action))
		for set in effects :
			for effect in set.keys() :
				effecthappened = True
				arguments = argsolve.Solve(set[effect])
				eval("efunc."+effect+"(arguments)")
		if effecthappened :
			break #Leave the secondary loop and re-enter the primary loop