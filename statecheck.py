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
auto_scene_states = {}
auto_encounter_states = {}
auto_item_states = {}
auto_ability_states = {}
auto_attribute_states = {}
import argsolve
from functions import nonemptyprint

#The 'Give' functions are ran only once to give the statecheck script access to Adventure files and the Character file
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c
	argsolve.GiveChar(char)

#The 'Prepare' functions are only run when the scene, inventory etc are changed and cache useful, relatively static information for thier respective 'Check' function.
def Prepare(aspect) :
	aspect_lists[aspect] = char[aspect]['active']
	for thing in aspect_lists[aspect] :
		if str(thing) not in auto_states[aspect].keys() : #Creates a dictionary that lists the states that have evaluations for each Scene encountered
			auto_states[aspect][str(thing)] = [x for x in StripNonStates(adv.f[aspect][str(thing)].keys()) if HasEvaluations(adv.f[aspect][str(thing)][x])]

def StripNonStates(keys) :
	return [ x for x in keys if x.isdigit() ]

def HasEvaluations(state) :
	try :
		state['evaluations']
		return True
	except KeyError :
		return False	

#The 'Check' functions are the meat of the statecheck script. Every iteration of the primary loop each potential state with evaluations is evaluated and a new list of states is generated. Any changes are noted and may trigger effects.
def Check(aspect) :
	global char
	global scene
	changed = False
	effects = {}
	for thing in aspect_lists[aspect] :
		current_states = char[aspect][str(thing)]
		new_states = [x for x in current_states if x not in auto_states[aspect][str(thing)]] #if x not in Z
		evaluators = [argsolve.Solve(each) for each in adv.f[aspect][str(thing)]['evaluators']]
		new_states += [x for x in auto_states[aspect][str(thing)] if TestState(adv.f[aspect][str(thing)][str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			changed = True
			try :
				effects.update(adv.f[aspect][str(thing)][str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			changed = True
			try :
				effects.update(adv.f[aspect][str(thing)][str(enteringstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		if changed :
			char[aspect][str(thing)] = new_states
			break
	return changed, effects

#Outcomes of actions are determined much the same way as states are so code is shared	
def DetermineOutcomes(action) :
	global adv
	global char
	effects = {}
	if action == 0 : return effects
	action_data = adv.f['Actions'][str(action)]
	all_outcomes = StripNonStates(action_data.keys())
	try :
		effects.update(adv.f['Actions'][str(action)]['effects'])
	except KeyError : pass #effects are optional
	if len(all_outcomes) == 1 :
		outcomes = all_outcomes
	else :
		evaluators = [argsolve.Solve(each) for each in action_data['evaluators']]
		outcomes = [x for x in all_outcomes if TestState(action_data[str(x)],evaluators)]
	if not outcomes :
		print "Nothing Happens\n" #This occurs if no outcomes match
	else :
		for outcome in outcomes :
			try : effects.update(adv.f['Actions'][str(action)][outcome]['effects'])
			except KeyError : pass #effects are optional
			try : nonemptyprint(adv.f['Actions'][action][outcome])
			except KeyError : pass #text is optional
			try : char['Beats'] += adv.f['Actions'][action][outcome]['duration']
			except KeyError : pass #duration is optional
	return effects

def TestState(statedata,evaluators) :
	for test in statedata['evaluations'].keys() :
		verdict = CompareEval(statedata['evaluations'][test],evaluators[test])
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