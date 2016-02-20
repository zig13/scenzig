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
from effects import *
GiveAdv(a)
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
GiveChar(c)
import argparser
argparser.GiveChar(c)
while True : #Primary loop. Is only broken by the quit command. Below is run after any action is taken
	for vital in c['Vitals'].keys() :
		evaluators = [argparser.PrsArg(each) for each in a.f['vitals'][vital]['evaluators']]
		for state in a.f['vitals'][str(vital)].keys()[2:] :
			this = True
			for test in a.f['vitals'][vital][state]['evaluations'].keys() :
				if not a.f['vitals'][vital][state]['evaluations'][test][0] <= evaluators[test] <= a.f['vitals'][vital][state]['evaluations'][test][1] :
					this = False
					break
			if this is True : break
		if this is True :
			for effect in a.f['vitals'][str(vital)][str(c['Vitals'][vital][0])]['leaveeffects'].keys() : #The line below runs the function requested by each effect and passes it any arguments
				eval(effect+"(a.f['vitals'][str(vital)][str(c['Vitals'][vital][0])]['leaveeffects'][effect])")
			c['Vitals'][vital][0] = int(state) #Here the vital state is corrected to that vital value is within state range
			for effect in a.f['vitals'][str(vital)][state]['entereffects'].keys() : #The line below runs the function requested by each effect and passes it any arguments
				arguments = argparser.PrsArg(a.f['vitals'][str(vital)][state]['entereffects'][effect])
				eval(effect+"(arguments)")
			c.write()
	for attribute in c['Attributes'].keys() :
		evaluators = [argparser.PrsArg(each) for each in a.f['attributes'][attribute]['evaluators']]
		for state in a.f['attributes'][str(attribute)].keys()[2:] :
			this = True
			for test in a.f['attributes'][attribute][state]['evaluations'].keys() :
				if not a.f['attributes'][attribute][state]['evaluations'][test][0] <= evaluators[test] <= a.f['attributes'][attribute][state]['evaluations'][test][1] :
					this = False
					break
			if this is True : break
		if this is True :
			for effect in a.f['attributes'][str(attribute)][str(c['Attributes'][attribute][0])]['leaveeffects'].keys() : #The line below runs the function requested by each effect and passes it any arguments
				eval(effect+"(a.f['attributes'][str(attribute)][str(c['Attributes'][attribute][0])]['leaveeffects'][effect])")
			c['Attributes'][attribute][0] = int(state) #Here the attribute state is corrected to that attribute value is within state range
			for effect in a.f['attributes'][str(attribute)][state]['entereffects'].keys() : #The line below runs the function requested by each effect and passes it any arguments
				arguments = argparser.PrsArg(a.f['attributes'][str(attribute)][state]['entereffects'][effect])
				eval(effect+"(arguments)")
			c.write()
	wlist = a.f['scenes'][str(c['Scenes']['Current'])]['Master']['wlist'] + a.f['scenes'][str(c['Scenes']['Current'])][str(c['Scenes']['States'][str(c['Scenes']['Current'])])]['wlist']
	blist = a.f['scenes'][str(c['Scenes']['Current'])]['Master']['blist'] + a.f['scenes'][str(c['Scenes']['Current'])][str(c['Scenes']['States'][str(c['Scenes']['Current'])])]['blist']
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
	GiveList(glist)
	while True : #Secondary loop. Is broken when an action is taken. The code below is repeated when anything is put into the prompt regardless of validity.
		nonemptyprint(a.f['scenes'][str(c['Scenes']['Current'])]['Master']['description']) #Scene description will be printed if there is one
		nonemptyprint(a.f['scenes'][str(c['Scenes']['Current'])][str(c['Scenes']['States'][str(c['Scenes']['Current'])])]['description'])
		nonemptyprint(a.f['encounters'][str(c['Scenes']['Encounters'][str(c['Scenes']['Current'])][0])]['Master']['description'])
		nonemptyprint(a.f['encounters'][str(c['Scenes']['Encounters'][str(c['Scenes']['Current'])][0])][str(c['Scenes']['Encounters'][str(c['Scenes']['Current'])][1])]['description'])
		for vital in c['Vitals'].keys() :
			nonemptyprint(a.f['vitals'][str(vital)][str(c['Vitals'][vital][0])]['description'])
		prompt = raw_input(">").strip() #The main prompt
		try : #Effectively 'if input is a whole number'
			prompt = int(prompt)
			if prompt in glist : action = str(prompt) #If the input matches the UID of a valid action then take note of it's UID
			else :
				Clr()
				continue
		except ValueError : #Effectively 'if input isn't a whole number'
			prompt = prompt.lower() #Makes all inputted characters lower case where applicable
			if (prompt == 'quit') or (prompt == 'exit') or (prompt == 'esc') or (prompt == 'q') : break
			else :
				actdict = {}
				for actn in glist : #Builds a dictionary that pairs the slug of each valid action with it's UID
					actdict[a.f['actions'][str(actn)]['slug'].lower()] = actn
				if prompt in actdict.keys() : action = str(actdict[prompt]) #If the input matches the slug of a valid action then take note of it's UID
				else :
					Clr()
					continue
		Clr()
		evaluators = [argparser.PrsArg(each) for each in a.f['actions'][action]['evaluators']]
		for outcome in a.f['actions'][action]['outcomes'].keys() :
			this = True
			for test in a.f['actions'][action]['outcomes'][outcome]['evaluations'].keys() :
				if not a.f['actions'][action]['outcomes'][outcome]['evaluations'][test][0] <= evaluators[test] <= a.f['actions'][action]['outcomes'][outcome]['evaluations'][test][1] :
					this = False
					break
			if this is True : break
		if this is True :
			nonemptyprint(a.f['actions'][action]['outcomes'][outcome]['text']) #Action text will be printed if it exists
			try :
				for effect in a.f['actions'][action]['outcomes'][outcome]['effects'].keys() : #The line below runs the function requested by each effect of the chosen action and passes it any arguments from the Action.
					arguments = argparser.PrsArg(a.f['actions'][action]['outcomes'][outcome]['effects'][effect]['variables'])
					eval(a.f['actions'][action]['outcomes'][outcome]['effects'][effect]['function']+"(arguments)")
			except KeyError : pass #If an action has no effects, don't sweat it - just carry on
		else : print "Nothing Happens\n" #This occurs if no outcomes match 
		break
	if (prompt == 'quit') or (prompt == 'exit') or (prompt == 'esc') or (prompt == 'q') : break #Temporary. I'll work out a better way of quitting eventually