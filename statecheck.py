#-------------------------------------------------------------------------------
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
adv = None
char = None
aspect_lists = {}
auto_states = {'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}}
scene = None
scene_data = None
encounter_data = None
inventory = None
abilities = None
attributes = None
listcollate = None
auto_scene_states = {}
auto_encounter_states = {}
auto_item_states = {}
auto_ability_states = {}
auto_attribute_states = {}
import argsolve
import effects as efunc
from functions import nonemptyprint

#The 'Give' functions are ran only once to give the statecheck script access to Adventure files and the Character file
def GiveAdv(a) :
	global adv
	adv = a
	efunc.GiveAdv(a)
def GiveChar(c) :
	global char
	char = c
	argsolve.GiveChar(char)
	efunc.GiveChar(c)
def GiveListCollate(lcollate) :
	global listcollate
	listcollate = lcollate
	efunc.GiveListCollate(lcollate)

#The 'Prepare' functions are only run when the scene, inventory etc are changed and cache useful, relatively static information for thier respective 'Check' function.
def Prepare(aspect) :
	try :
		aspect_lists[aspect] = char[aspect]['active'] #Which Attributes, Abilities and Scene are/is active is explicitly stated and stored in the Character file in the active list under each aspect heading.
	except KeyError : #However Active lists for Items and Encounters are based on Whitelists and are generated by listcollate. statecheck.Prepare is run before listcollate.
		char[aspect]['active'] = []  #Ideally Adventure creators should still fill in the active lists in the Character template but in case they don't empty ones are generated.
		aspect_lists[aspect] = []
	for thing in aspect_lists[aspect] :
		UpdateAutoList(aspect, thing)

def UpdateAutoList(aspect, thing) :
	if str(thing) not in auto_states[aspect].keys() : #Creates a dictionary that lists the states that have evaluations for each Scene encountered
		auto_states[aspect][str(thing)] = [int(x) for x in StripNonStates(adv.f[aspect][str(thing)].keys()) if HasEvaluations(adv.f[aspect][str(thing)][x])]

def StripNonStates(keys) :
	return [ x for x in keys if x.isdigit() ]

def HasEvaluations(state) :
	try :
		state['evaluations']
		return True
	except KeyError :
		return False

#The 'Check' functions are the meat of the statecheck script. Every iteration of the primary loop each potential state with evaluations is evaluated and a new list of states is generated. Any changes are noted and may trigger effects.
def Check(remit="All") :
	global char
	global scene
	if remit is "All" :
		aspects = aspect_lists.keys()
	else :
		aspects = [remit]
		if remit not in aspect_lists.keys() : #If the aspect has not yet been prepared. This should only happen during setup
			Prepare(remit)
	for aspect in aspects :
		for thing in aspect_lists[aspect] :
			effects = {}
			states_removed = False
			states_added = False
			current_states = char[aspect][str(thing)]
			new_states = [x for x in current_states if x not in auto_states[aspect][str(thing)]] #if x not in Z
			evaluators = [argsolve.Solve(each) for each in adv.f[aspect][str(thing)].get('evaluators', default=[])]
			if not evaluators : continue
			new_states += [x for x in auto_states[aspect][str(thing)] if TestState(adv.f[aspect][str(thing)][str(x)],evaluators)]
			if new_states == current_states : continue
			leaving_states = set(current_states).difference(set(new_states))
			for leavingstate in leaving_states :
				states_removed = True
				try :
					effects.update(adv.f[aspect][str(thing)][str(leavingstate)]['leaveeffects'])
				except KeyError : pass #leave effects are optional
				try :
					nonemptyprint(adv.f[aspect][str(thing)][str(leavingstate)],char,'leavetext')
				except KeyError : pass #leave text is optional
			entering_states = set(new_states).difference(set(current_states))
			for enteringstate in entering_states :
				states_added = True
				try :
					effects.update(adv.f[aspect][str(thing)][str(enteringstate)]['entereffects'])
				except KeyError : pass #enter effects are optional
				try :
					nonemptyprint(adv.f[aspect][str(thing)][str(enteringstate)],char,'entertext')
				except KeyError : pass #enter text is optional
			if states_removed or states_added :
				char[aspect][str(thing)] = new_states
			for effect in effects.keys() :
				arguments = argsolve.Solve(effects[effect])
				eval("efunc."+effect+"(arguments)")
			if states_removed :
				listcollate.RemoveStates(aspect, thing)
			if states_added :
				listcollate.AddStates(aspect, thing)

#Outcomes of actions are determined much the same way as states are so code is shared
def DetermineOutcomes(action) :
	global adv
	global char
	effects = []
	text = False
	if action == 0 : return effects
	action_data = adv.f['Actions'][str(action)]
	all_outcomes = StripNonStates(action_data.keys())
	try :
		effects.append(adv.f['Actions'][str(action)]['effects'])
	except KeyError : pass #effects are optional
	evaluators = [argsolve.Solve(each) for each in action_data.get('evaluators',default=[])]
	if evaluators :
		outcomes = [x for x in all_outcomes if TestState(action_data[str(x)],evaluators)]
	else :
		outcomes = all_outcomes
	if not outcomes :
		print "Nothing Happens\n" #This occurs if no outcomes match
	else :
		for outcome in outcomes :
			try : effects.append(adv.f['Actions'][str(action)][outcome]['effects'])
			except KeyError : pass #effects are optional
			try :
				text = nonemptyprint(adv.f['Actions'][action][outcome],char)
			except KeyError : pass #text is optional
			try :
				char['Beats'] += adv.f['Actions'][action][outcome]['duration']
				efunc.actionstack.extend(efunc.echo.Age(adv.f['Actions'][action][outcome]['duration']))
			except KeyError : pass #duration is optional
	return [effects,text]

def TestState(statedata,evaluators) :
	verdict = False
	for test in statedata.get('evaluations',default={}).keys() :
		verdict = CompareEval(statedata['evaluations'][test],evaluators[test])
		if not verdict : break
	return verdict

def CompareEval(valrange,value) :
	verdict = True
	try :
		if not valrange[0] <= value <= valrange[1] :
			verdict = False
	except TypeError :
		if value is not valrange :
			verdict = False
	return verdict
