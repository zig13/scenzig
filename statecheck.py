adv = None
char = None
scene = None
scene_data = None
encounter_data = None
inventory = None
abilities = None
vitals = None
attributes = None
auto_scene_states = {}
auto_encounter_states = {}
auto_item_states = {}
auto_ability_states = {}
auto_vital_states = {}
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
def PrepareScene() :
	global adv
	global char
	global scene
	scene = char['Scene']['Current']
	global scene_data
	scene_data = adv.f['scenes'][str(scene)]
	global auto_scene_states
	if str(scene) not in auto_scene_states.keys() : #Creates a dictionary that lists the states that have evaluations for each Scene encountered
		auto_scene_states[str(scene)] = [x for x in StripNonStates(scene_data.keys()) if HasEvaluations(scene_data[x])]	
def PrepareEncounter() :
	global adv
	global char
	global scene
	global encounter
	encounter = char['Encounters'][str(scene)][0]
	global encounter_data
	encounter_data = adv.f['encounters'][str(encounter)]
	global auto_encounter_states
	if str(encounter) not in auto_encounter_states.keys() : #Creates a dictionary that lists the states that have evaluations for each Encounter encountered
		auto_encounter_states[str(encounter)] = [x for x in StripNonStates(encounter_data.keys()) if HasEvaluations(encounter_data[x])]
def PrepareItems() :
	global adv
	global char
	global inventory
	inventory = char['Items'].keys()
	global auto_item_states
	for item in inventory :	
		if str(item) not in auto_item_states.keys() :  #Creates a dictionary that lists the states that have evaluations for each Item encountered
			auto_item_states[str(item)] = [x for x in StripNonStates(adv.f['items'][str(item)].keys()) if HasEvaluations(adv.f['items'][str(item)][x])]
def PrepareAbilities() :
	global adv
	global char
	global abilities
	abilities = char['Abilities'].keys()
	global auto_ability_states
	for ability in abilities :	
		if str(ability) not in auto_ability_states.keys() :  #Creates a dictionary that lists the states that have evaluations for each Item encountered
			auto_ability_states[str(ability)] = [x for x in StripNonStates(adv.f['abilities'][str(ability)].keys()) if HasEvaluations(adv.f['abilities'][str(ability)][x])]
def PrepareVitals() :
	global adv
	global char
	global vitals
	vitals = char['Vitals'].keys()
	global auto_vital_states
	for vital in vitals :	
		if str(vital) not in auto_vital_states.keys() :  #Creates a dictionary that lists the states that have evaluations for each Vital encountered
			auto_vital_states[str(vital)] = [x for x in StripNonStates(adv.f['vitals'][str(vital)].keys()) if HasEvaluations(adv.f['vitals'][str(vital)][x])]
def PrepareAttributes() :
	global adv
	global char
	global attributes
	attributes = char['Attributes'].keys()
	global auto_attribute_states
	for attribute in attributes :	
		if str(attribute) not in auto_attribute_states.keys() :  #Creates a dictionary that lists the states that have evaluations for each Attribute encountered
			auto_attribute_states[str(attribute)] = [x for x in StripNonStates(adv.f['attributes'][str(attribute)].keys()) if HasEvaluations(adv.f['attributes'][str(attribute)][x])]

def StripNonStates(keys) :
	return [ x for x in keys if x.isdigit() ]

def HasEvaluations(state) :
	try :
		state['evaluations']
		return True
	except KeyError :
		return False	

#The 'Check' functions are the meat of the statecheck script. Every iteration of the primary loop each potential state with evaluations is evaluated and a new list of states is generated. Any changes are noted and may trigger effects.
def CheckScene() :
	global char
	global scene
	global scene_data
	global auto_scene_states
	current_states = char['SceneStates'][str(scene)][1]
	evaluators = [argsolve.Solve(each) for each in scene_data['evaluators']]
	new_states = [x for x in auto_scene_states[str(scene)] if TestState(scene_data[str(x)],evaluators)]
	effects = {}
	leaving_states = set(current_states).difference(set(new_states))
	for leavingstate in leaving_states :
		try :
			effects.update(scene_data[str(leavingstate)]['leaveeffects'])
		except KeyError : pass #leave effects are optional
	entering_states = set(new_states).difference(set(current_states))
	for enteringstate in entering_states :
		try :
			effects.update(scene_data[str(enteringstate)]['entereffects'])
		except KeyError : pass #leave effects are optional
	char['SceneStates'][str(scene)][1] = new_states
	return effects	
def CheckEncounter() :
	global char
	global scene
	global encounter
	global encounter_data
	global auto_encounter_states
	current_states = char['Encounters'][str(scene)][1][1]
	evaluators = [argsolve.Solve(each) for each in encounter_data['evaluators']]
	new_states = [x for x in auto_encounter_states[str(encounter)] if TestState(encounter_data[str(x)],evaluators)]
	effects = {}
	leaving_states = set(current_states).difference(set(new_states))
	for leavingstate in leaving_states :
		try :
			effects.update(encounter_data[str(leavingstate)]['leaveeffects'])
		except KeyError : pass #leave effects are optional
	entering_states = set(new_states).difference(set(current_states))
	for enteringstate in entering_states :
		try :
			effects.update(encounter_data[str(enteringstate)]['entereffects'])
		except KeyError : pass #leave effects are optional
	char['Encounters'][str(scene)][1][1] = new_states
	return effects	
def CheckItems() :
	global adv
	global char
	global auto_item_states
	effects = {}
	for item in char['Items'].keys() :
		current_states = char['Items'][item][1]
		item_data = adv.f['items'][item]
		evaluators = [argsolve.Solve(each) for each in item_data['evaluators']]
		new_states = [x for x in auto_item_states[item] if TestState(item_data[str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			try :
				effects.update(item_data[str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			try :
				effects.update(item_data[str(enteringstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		char['Items'][item][1] = new_states
	return effects	
def CheckAbilities() :
	global adv
	global char
	global auto_ability_states
	effects = {}
	for ability in char['Abilities'].keys() :
		current_states = char['Abilities'][ability][1]
		ability_data = adv.f['abilities'][ability]
		evaluators = [argsolve.Solve(each) for each in ability_data['evaluators']]
		new_states = [x for x in auto_ability_states[ability] if TestState(ability_data[str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			try :
				effects.update(ability_data[str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			try :
				effects.update(ability_data[str(enteringstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		char['Abilities'][ability][1] = new_states
	return effects		
def CheckVitals() :
	global adv
	global char
	global auto_vital_states
	effects = {}
	for vital in char['Vitals'].keys() :
		current_states = char['Vitals'][vital][0][1]
		vital_data = adv.f['vitals'][vital]
		evaluators = [argsolve.Solve(each) for each in vital_data['evaluators']]
		new_states = [int(x) for x in auto_vital_states[vital] if TestState(vital_data[str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			try :
				effects.update(vital_data[str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			try :
				effects.update(vital_data[str(enteringstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		char['Vitals'][vital][0][1] = new_states
	return effects		
def CheckAttributes() :
	global adv
	global char
	global auto_attribute_states
	effects = {}
	for attribute in char['Attributes'].keys() :
		current_states = char['Attributes'][attribute][0][1]
		attribute_data = adv.f['attributes'][attribute]
		evaluators = [argsolve.Solve(each) for each in attribute_data['evaluators']]
		new_states = [int(x) for x in auto_attribute_states[attribute] if TestState(attribute_data[str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			try :
				effects.update(attribute_data[str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			try :
				effects.update(attribute_data[str(enteringstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		char['Attributes'][attribute][0][1] = new_states
	return effects

#Outcomes of actions are determined much the same way as states are so code is shared	
def DetermineOutcomes(action) :
	global adv
	global char
	effects = {}
	if action == 0 : return effects
	action_data = adv.f['actions'][str(action)]
	all_outcomes = StripNonStates(action_data.keys())
	try :
		effects.update(adv.f['actions'][str(action)]['effects'])
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
			try : effects.update(adv.f['actions'][str(action)][outcome]['effects'])
			except KeyError : pass #effects are optional
			try : nonemptyprint(adv.f['actions'][action][outcome])
			except KeyError : pass #text is optional
			try : char['Beats'] += adv.f['actions'][action][outcome]['duration']
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