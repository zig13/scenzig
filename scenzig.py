﻿#-------------------------------------------------------------------------------
# Thie file is part of scenzig
# Purpose:     An engine for text-based adventure games and interactive prose using a scene-based system.
#
# Author:      Thomas Sturges-Allard
#
# Created:     09/01/2016
# Copyright:   (c) Thomas Sturges-Allard 2016-2017
# Licence:     scenzig is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#              scenzig is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#              You should have received a copy of the GNU General Public License along with scenzig. If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
from os import chdir, path, curdir, sep, listdir #sep and curdir produce the correct characters for the operating system in use
chdir(path.dirname(path.abspath(__file__)))
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
import statecheck
statecheck.GiveAdv(a)
statecheck.efunc.GiveStateCheck(statecheck)
import listcollate
listcollate.GiveAdv(a)
statecheck.GiveListCollate(listcollate)
Clr() #Clears splash text
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
		listcollate.GiveChar(c)
		statecheck.GiveChar(c)
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
	try :
		c['Labels']['0'] = [0,filename[:-4]]
	except KeyError :
		c['Labels'] = {}
		c['Labels']['0'] = [0,filename[:-4]]
	listcollate.GiveChar(c)
	statecheck.GiveChar(c)
	firstrun = True
listcollate.Setup(statecheck)
statecheck.Check('All')
listcollate.SetBaseAttributes()
import argsolve
argsolve.GiveChar(c)
Clr()
while True : #Primary loop. Below is run after an effect happens
	effecthappened = False
	text = False
	listcollate.CapModifiers() #Ensures Attributes do not exceed thier maximum values
	c.write()
	glist = listcollate.CollateActions() # These are the actions available to the player.
	statecheck.efunc.GiveList(glist)
	while True : #Secondary loop. Below is run when anything is put into the prompt regardless of validity.
		if statecheck.efunc.actionstack :
			action = statecheck.efunc.actionstack.pop()
			prompt = action
		else :
			nonemptyprint(a.f['Scenes'][str(c['Scenes']['active'][0])],c) #Scene description will be printed if there is one
			stateprintInventories = []
			for state in sorted(c['Scenes'][str(c['Scenes']['active'][0])]) :
				nonemptyprint(a.f['Scenes'][str(c['Scenes']['active'][0])][str(state)],c)
				stateprintInventories.extend(a.f['Scenes'][str(c['Scenes']['active'][0])][str(state)].get('printInventories',default=[]))
			for inventory in a.f['Scenes'][str(c['Scenes']['active'][0])].get('printInventories',default=[]) :
				statecheck.efunc.PrintItems([inventory])
			for inventory in stateprintInventories :
				statecheck.efunc.PrintItems([inventory])
			for encounter in c['Encounters']['active'] :
				nonemptyprint(a.f['Encounters'][str(encounter)],c) #Encounter description will be printed if there is one
				for state in sorted(c['Encounters'][str(encounter)]) :
					nonemptyprint(a.f['Encounters'][str(encounter)][str(state)],c)
			for vital in c['Attributes']['vital'] :
				for state in sorted(c['Attributes'][str(vital)]) :
					nonemptyprint(a.f['Attributes'][str(vital)][str(state)],c)
			prompt = raw_input(">").strip() #The main prompt
			action = 0
		missing_actions = []
		try : #Effectively 'if input is a whole number'
			prompt = int(prompt)
			if prompt in glist :
				action = str(prompt) #If the input matches the UID of a valid action then take note of it's UID
			elif action : pass #If action is not 0 (and therefore has been set already)
		except ValueError : #Effectively 'if input isn't a whole number'
			prompt = prompt.lower() #Makes all inputted characters lower case where applicable
			actdict = {}
			for actn in glist : #Builds a dictionary that pairs the command(s) of each valid action with it's UID
				try :
					actdict[a.f['Actions'][str(actn)]['commands'].lower()] = actn #This will succeed only if 'commands' is a singular string
				except AttributeError : #If the action has a list of commands (rather than a singular string command)
					for command in a.f['Actions'][str(actn)]['commands'] :
						actdict[command.lower()] = actn #Makes a record in actdict for each command the action has
				except KeyError : #If a whitelisted action has no commands or does not exist at all
					missing_actions.append(actn) #Echoing actions and others using the actionstack avoid verification as they are reffered to by UID and ∴ don't need commands
			if prompt in actdict.keys() :
				action = str(actdict[prompt]) #If the input matches the command of a valid action then take note of it's UID
			Clr()
		for missing in missing_actions :
			print "Action ID %s is whitelisted but does not exist in actions.scnz"%(str(missing))
		results = statecheck.DetermineOutcomes(action)
		if results :
			effects = results[0]
			text = results[1]
			for outcome in effects :
				for effect in outcome.keys() :
					effecthappened = True
					arguments = argsolve.Solve(outcome[effect])
					eval("statecheck.efunc."+effect+"(arguments)")
		if text :
			print ""
		if effecthappened :
			break #Leave the secondary loop and re-enter the primary loop
