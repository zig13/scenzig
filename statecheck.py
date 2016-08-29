adv = None
char = None
scene = None
scene_data = None
encounter_data = None
inventory = None
auto_scene_states = {}
auto_encounter_states = {}
auto_item_states = {}
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
		auto_scene_states[str(scene)] = :[x for x in StripNonStates(scene_data.keys()) if HasEvaluations(scene_data[x])]]		
def PrepareEncounter() :
	global adv
	global char
	global scene
	encounter = char['Encounters'][str(scene)][0]
	global encounter_data
	encounter_data = adv.f['encounters'][str(encounter)]
	global auto_encounter_states
	if str(encounter) not in auto_encounter_states.keys() : #Creates a dictionary that lists the states that have evaluations for each Encounter encountered
		auto_encounter_states[str(encounter)] = :[x for x in StripNonStates(scene_data.keys()) if HasEvaluations(scene_data[x])]]	
def PrepareItems() :
	global adv
	global char
	global inventory
	inventory = char['Items'].keys()
	global auto_item_states
	for item in inventory :	
		if str(item) not in auto_item_states.keys() :  #Creates a dictionary that lists the states that have evaluations for each Item encountered
			auto_item_states[str(item]] = [x for x in StripNonStates(adv.f['items'][str(item)].keys()) if HasEvaluations(StripNonStates(adv.f['items'][str(item)][x])]]
def PrepareAbilities() :
	global adv
	global char
	global inventory
	inventory = char['Abilities'].keys()
	global auto_ability_states
	for ability in inventory :	
		if str(ability) not in auto_ability_states.keys() :  #Creates a dictionary that lists the states that have evaluations for each Item encountered
			auto_ability_states[str(ability]] = [x for x in StripNonStates(adv.f['abilities'][str(ability)].keys()) if HasEvaluations(StripNonStates(adv.f['abilities'][str(ability)][x])]]
def PrepareVitals() :
	global adv
	global char
	global inventory
	inventory = char['Vitals'].keys()
	global auto_vital_states
	for vital in inventory :	
		if str(vital) not in auto_vital_states.keys() :  #Creates a dictionary that lists the states that have evaluations for each Vital encountered
			auto_vital_states[str(vital]] = [x for x in StripNonStates(adv.f['vitals'][str(vital)].keys()) if HasEvaluations(StripNonStates(adv.f['vitals'][str(vital)][x])]]
def PrepareAttributes() :
	global adv
	global char
	global inventory
	inventory = char['Attributes'].keys()
	global auto_attribute_states
	for attribute in inventory :	
		if str(attribute) not in auto_attribute_states.keys() :  #Creates a dictionary that lists the states that have evaluations for each Attribute encountered
			auto_attribute_states[str(attribute]] = [x for x in StripNonStates(adv.f['attributes'][str(attribute)].keys()) if HasEvaluations(StripNonStates(adv.f['attributes'][str(attribute)][x])]]

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
	new_states = [x for x in auto_scene_states if TestState(scene_data[str(x)],evaluators)]
	effects = {}
	leaving_states = set(current_states).difference(set(new_states))
	for leavingstate in leaving_states :
		try :
			effects.append(scene_data[str(leavingstate)]['leaveeffects'])
		except KeyError : pass #leave effects are optional
	entering_states = set(new_states).difference(set(current_states))
	for enteringstate in entering_states :
		try :
			effects.append(scene_data[str(leavingstate)]['entereffects'])
		except KeyError : pass #leave effects are optional
	char['SceneStates'][str(scene)][1] = new_states
	return effects	
def CheckEncounter() :
	global char
	global scene
	global encounter_data
	global auto_encounter_states
	current_states = char['Encounters'][str(scene)][1][1]
	evaluators = [argsolve.Solve(each) for each in encounter_data['evaluators']]
	new_states = [x for x in auto_encounter_states if TestState(encounter_data[str(x)],evaluators)]
	effects = {}
	leaving_states = set(current_states).difference(set(new_states))
	for leavingstate in leaving_states :
		try :
			effects.append(encounter_data[str(leavingstate)]['leaveeffects'])
		except KeyError : pass #leave effects are optional
	entering_states = set(new_states).difference(set(current_states))
	for enteringstate in entering_states :
		try :
			effects.append(encounter_data[str(leavingstate)]['entereffects'])
		except KeyError : pass #leave effects are optional
	char['Encounters'][str(scene)][1][1] = new_states
	return effects	
def CheckItems() :
	global adv
	global char
	global auto_item_states
	effects = {}
	for item in char['Items'].keys() :
		currentstates = char['Items'][item][1]
		item_data = adv.f['items'][item]
		evaluators = [argsolve.Solve(each) for each in item_data['evaluators']]
		new_states = [x for x in auto_item_states if TestState(item_data[str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			try :
				effects.append(item_data[str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			try :
				effects.append(item_data[str(leavingstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		char['Items'][item][1] = new_states
	return effects	
def CheckAbilities() :
	global adv
	global char
	global auto_ability_states
	effects = {}
	for ability in char['Abilities'].keys() :
		currentstates = char['Abilities'][ability][1]
		ability_data = adv.f['abilities'][ability]
		evaluators = [argsolve.Solve(each) for each in ability_data['evaluators']]
		new_states = [x for x in auto_ability_states if TestState(ability_data[str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			try :
				effects.append(ability_data[str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			try :
				effects.append(ability_data[str(leavingstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		char['Abilities'][ability][1] = new_states
	return effects		
def CheckVitals() :
	global adv
	global char
	global auto_vital_states
	effects = {}
	for vital in char['Vitals'].keys() :
		currentstates = char['Vitals'][vital][1]
		vital_data = adv.f['vitals'][vital]
		evaluators = [argsolve.Solve(each) for each in vital_data['evaluators']]
		new_states = [x for x in auto_vital_states if TestState(vital_data[str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			try :
				effects.append(vital_data[str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			try :
				effects.append(vital_data[str(leavingstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		char['Vitals'][vital][1] = new_states
	return effects		
def CheckAttributes() :
	global adv
	global char
	global auto_attribute_states
	effects = {}
	for attribute in char['Attributes'].keys() :
		currentstates = char['Attributes'][attribute][1]
		attribute_data = adv.f['attributes'][attribute]
		evaluators = [argsolve.Solve(each) for each in attribute_data['evaluators']]
		new_states = [x for x in auto_attribute_states if TestState(attribute_data[str(x)],evaluators)]
		leaving_states = set(current_states).difference(set(new_states))
		for leavingstate in leaving_states :
			try :
				effects.append(attribute_data[str(leavingstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
		entering_states = set(new_states).difference(set(current_states))
		for enteringstate in entering_states :
			try :
				effects.append(attribute_data[str(leavingstate)]['entereffects'])
			except KeyError : pass #leave effects are optional
		char['Attributes'][attribute][1] = new_states
	return effects

#Outcomes of actions are determined much the same way as states are so code is shared	
def DetermineOutcomes(action) :
	global adv
	global char
	action_data = adv.f['actions'][str(action)]
	all_outcomes = StripNonStates(action_data.keys())
	effects = {}
	evaluators = [argsolve.Solve(each) for each in action_data['evaluators']]
	outcomes = [x for x in all_outcomes if TestState(action_data[str(x)],evaluators)]
	if not outcomes :
		print "Nothing Happens\n" #This occurs if no outcomes match
	else :
		for outcome in outcomes :
			try :
				effects.update(adv.f['actions'][str(action)][outcome]['effects'])
			except KeyError : pass #effects are optional
			try :
				nonemptyprint(adv.f['actions'][action][outcome])
			except KeyError : pass #text is optional
	return effects

def TestState(statedata,evaluators) :
	for test in statedata['evaluations'].keys() :
		verdict = CompareEval(thing[state]['evaluations'][test],evaluators[test])
	
def CompareEval(valrange,value) :
	verdict = True
	try :
		if not valrange[0] <= value <= valrange[1] :
			verdict = False
	except TypeError :
		if value is not valrange :
			verdict = False
	return verdict