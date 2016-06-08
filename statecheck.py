adv = None
char = None
import argsolve
from functions import nonemptyprint
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c
	argsolve.GiveChar(char)
	
def CheckScene() :
	global adv
	global char
	scene = char['Scene']['Current']
	currentstate = char['SceneStates'][str(scene)]
	effects = []
	evaluators = [argsolve.Solve(each) for each in adv.f['scenes'][str(scene)]['evaluators']]
	if FindState(dict([(str(currentstate), adv.f['scenes'][str(scene)][str(currentstate)])]),evaluators) is None : #Passes the current state only to FindState to test it
		try :
			resultstate = int(FindState(adv.f['scenes'][str(scene)],evaluators))
		except TypeError:
			return effects #If FindState returns None or another non-string then leave the Scene state alone
		if resultstate != currentstate :
			try :
				effects.append(adv.f['scenes'][str(scene)][str(currentstate)]['leaveeffects'])
			except KeyError : pass #leave effects are optional
			try :
				effects.append(adv.f['scenes'][str(scene)][str(resultstate)]['entereffects'])
			except KeyError : pass #enter effects are optional
			char['SceneStates'][str(scene)] = resultstate
	return effects
		
def CheckVitals() :
	global adv
	global char
	effects = []
	for vital in char['Vitals'].keys() :
		currentstate = char['Vitals'][vital][0]
		evaluators = [argsolve.Solve(each) for each in adv.f['vitals'][vital]['evaluators']]
		if FindState(dict([(str(currentstate), adv.f['vitals'][vital][str(currentstate)])]),evaluators) is None : #Passes the current state only to FindState to test it
			try :
				resultstate = int(FindState(adv.f['vitals'][vital],evaluators))
			except TypeError :
				continue #If FindState returns None or another non-string then leave the Vital state alone
			if resultstate != currentstate :
				try :
					effects.append(adv.f['vitals'][vital][str(currentstate)]['leaveeffects'])
				except KeyError : pass #leave effects are optional
				try :
					effects.append(adv.f['vitals'][vital][str(resultstate)]['entereffects'])
				except KeyError : pass #enter effects are optional
				char['Vitals'][vital][0] = resultstate
	return effects	
		
def CheckAttributes() :
	global adv
	global char
	effects = []
	for attribute in char['Attributes'].keys() :
		currentstate = char['Attributes'][attribute][0]
		evaluators = [argsolve.Solve(each) for each in adv.f['attributes'][attribute]['evaluators']]
		if FindState(dict([(str(currentstate), adv.f['attributes'][attribute][str(currentstate)])]),evaluators) is None : #Passes the current state only to FindState to test it
			try :
				resultstate = int(FindState(adv.f['attributes'][attribute],evaluators))
			except TypeError :
				continue #If FindState returns None or another non-string then leave the Vital state alone
			if resultstate != currentstate :
				try :
					effects.append(adv.f['attributes'][attribute][str(currentstate)]['leaveeffects'])
				except KeyError : pass #leave effects are optional
				try :
					effects.append(adv.f['attributes'][attribute][str(resultstate)]['entereffects'])
				except KeyError : pass #enter effects are optional
				char['Attributes'][attribute][0] = resultstate
	return effects
	
def CheckItems() :
	global adv
	global char
	effects = []
	for item in char['Items'].keys() :
		currentstate = char['Items'][item]
		evaluators = [argsolve.Solve(each) for each in adv.f['items'][item]['evaluators']]
		if FindState(dict([(str(currentstate), adv.f['items'][item][str(currentstate)])]),evaluators) is None : #Passes the current state only to FindState to test it
			try :
				resultstate = int(FindState(adv.f['items'][item],evaluators))
			except TypeError :
				continue #If FindState returns None or another non-string then leave the Vital state alone
			if resultstate != currentstate :
				try :
					effects.append(adv.f['items'][item][str(currentstate)]['leaveeffects'])
				except KeyError : pass #leave effects are optional
				try :
					effects.append(adv.f['items'][item][str(resultstate)]['entereffects'])
				except KeyError : pass #enter effects are optional
				char['Items'][item] = resultstate
	return effects
	
def CheckAbilities() :
	global adv
	global char
	effects = []
	for ability in char['Abilities'].keys() :
		currentstate = char['Abilities'][ability]
		evaluators = [argsolve.Solve(each) for each in adv.f['abilities'][ability]['evaluators']]
		if FindState(dict([(str(currentstate), adv.f['abilities'][ability][str(currentstate)])]),evaluators) is None : #Passes the current state only to FindState to test it
			try :
				resultstate = int(FindState(adv.f['abilities'][ability],evaluators))
			except TypeError :
				continue #If FindState returns None or another non-string then leave the Vital state alone
			if resultstate != currentstate :
				try :
					effects.append(adv.f['abilities'][ability][str(currentstate)]['leaveeffects'])
				except KeyError : pass #leave effects are optional
				try :
					effects.append(adv.f['abilities'][ability][str(resultstate)]['entereffects'])
				except KeyError : pass #enter effects are optional
				char['Abilities'][ability] = resultstate
	return effects
			
def CheckEncounter() :
	global adv
	global char
	scene = char['Scene']['Current']
	encounter = char['Encounters'][str(scene)][0]
	currentstate = char['Encounters'][str(scene)][1]
	effects = []
	evaluators = [argsolve.Solve(each) for each in adv.f['encounters'][str(encounter)]['evaluators']]
	try :
		resultstate = int(FindState(adv.f['encounters'][str(encounter)],evaluators))
	except TypeError:
		return effects #If FindState returns None or another non-string then leave the Scene state alone
	if resultstate != currentstate :
		try :
			effects.append(adv.f['encounters'][str(encounter)][str(currentstate)]['leaveeffects'])
		except KeyError : pass #leave effects are optional
		try :
			effects.append(adv.f['encounters'][str(encounter)][str(resultstate)]['entereffects'])
		except KeyError : pass #enter effects are optional
		char['Encounters'][str(scene)][1] = resultstate
	return effects
			
def DetermineOutcome(action) :
	global adv
	global char
	effects = {}
	evaluators = [argsolve.Solve(each) for each in adv.f['actions'][str(action)]['evaluators']]
	outcome = FindState(adv.f['actions'][action],evaluators)
	if outcome is None : 
		print "Nothing Happens\n" #This occurs if no outcomes match
	else :
		try :
			effects = adv.f['actions'][action][outcome]['effects']
		except KeyError : pass #effects are optional
		nonemptyprint(adv.f['actions'][action][outcome])
	return effects
	
def FindState(thing,evaluators) :
	for state in StripNonStates(thing.keys()) :
		verdict = True
		try :
			for test in thing[state]['evaluations'].keys() :
				verdict = CompareEval(thing[state]['evaluations'][test],evaluators[test])
		except KeyError : pass #If there are no evaluations then it passes by default
		if verdict is True :
			return state
			
def StripNonStates(keys) :
	return [ x for x in keys if x.isdigit() ]
	
def CompareEval(valrange,value) :
	verdict = True
	try :
		if not valrange[0] <= value <= valrange[1] :
			verdict = False
	except TypeError :
		if value is not valrange :
			verdict = False
	return verdict