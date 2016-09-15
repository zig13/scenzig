adv = None
actiongroups = None
char = None
vitalsbase = None
vitals = None
attributesbase = None
attributes = None
def GiveAdv(a) :
	global adv
	adv = a
	global actiongroups
	actiongroups = a.f['actiongrps']
def GiveChar(c) :
	global char
	char = c

def SetBaseVitals() :
	global char
	global vitalsbase
	vitalsbase = dict((vital, char['Vitals'][vital][1]) for vital in char['Vitals'].keys())
def reBaseVitals() :
	global vitalsbase
	global vitals
	vitals = vitalsbase
def SetBaseAttributes() :
	global char
	global attributesbase
	attributesbase = dict((attribute, char['Attributes'][attribute][1]) for attribute in char['Attributes'].keys())
def reBaseAttributes() :
	global attributesbase
	global attributes
	attributes = attributesbase
	
def CollateScene() :
	global adv
	global char
	scenedata = adv.f['scenes'][str(char['Scene']['Current'])]	
	states = str(char['SceneStates'][str(char['Scene']['Current'])])
	return Collate(scenedata, states)	
	
def CollateEncounter() :
	global adv
	global char
	encounterinfo = char['Encounters'][str(char['Scene']['Current'])]
	encounterdata = adv.f['encounters'][str(encounterinfo[0])]
	states = str(encounterinfo[1])
	return Collate(encounterdata, states)
	
def CollateAbilities() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for ability in char['Abilities'].keys() :
		abilitydata = adv.f['abilities'][str(ability)]
		states = str(char['Abilities'][str(ability)])
		lists = Collate(abilitydata, states)
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result
	
def CollateItems() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for item in char['Items'].keys() :
		itemdata = adv.f['items'][str(item)]
		states = str(char['Items'][str(item)])
		lists = Collate(itemdata, states)
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result
	
def CollateVitals() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for vital in char['Vitals'].keys() :
		itemdata = adv.f['vitals'][str(vital)]
		states = str(char['Vitals'][str(vital)][0])
		lists = Collate(itemdata, str(states))
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result

def CollateAttributes() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for attribute in char['Attributes'].keys() :
		itemdata = adv.f['attributes'][str(attribute)]
		states = str(char['Attributes'][str(attribute)][0])
		lists = Collate(itemdata, str(states))
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result

def Collate(aspectdata,states) :
	global actiongroups
	result = {'white':[],'black':[]}
	for vital in vitals :
		try :
			vitals[vital] += aspectdata['vitalbonuses'][vital]
		except KeyError : pass
	for attribute in attributes :
		try :
			attributes[attribute] += aspectdata['attributebonuses'][attribute]
		except KeyError : pass
	try : 
		result['white'] += aspectdata['wlist']
	except KeyError : pass
	try :
		for grp in aspectdata['wlistagrp'] :
			try :
				result['white'] += actiongroups[str(agrp)]['list']
			except KeyError : pass
	except KeyError : pass
	try :
		result['black'] += aspectdata['blist']
	except KeyError : pass
	try :
		for grp in aspectdata['blistagrp'] :
			try :
				result['black'] += actiongroups[str(agrp)]['list']
			except KeyError : pass
	except KeyError : pass

	for state in states :
		for vital in vitals :
			try :
				vitals[vital] += aspectdata['vitalbonuses'][vital]
			except KeyError : pass
		for attribute in attributes :
			try :
				attributes[attribute] += aspectdata['attributebonuses'][attribute]
			except KeyError : pass
		try :
			result['white'] += aspectdata[str(state)]['wlist']
		except KeyError : pass
		try :
			for grp in aspectdata[str(state)]['wlistagrp'] :
				try :
					result['white'] += actiongroups[str(agrp)]['list']
				except KeyError : pass
		except KeyError : pass	
		try :
			result['black'] += aspectdata[str(state)]['blist']
		except KeyError : pass
		try :
			for grp in aspectdata[str(state)]['blistagrp'] :
				try :
					result['black'] += actiongroups[str(agrp)]['list']
				except KeyError : pass
		except KeyError : pass
	return result