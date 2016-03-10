adv = None
actiongroups = None
char = None
def GiveAdv(a) :
	global adv
	adv = a
	global actiongroups
	actiongroups = a.f['actiongrps']
def GiveChar(c) :
	global char
	char = c
	
def CollateScene() :
	global adv
	global char
	scenedata = adv.f['scenes'][str(char['Scenes']['Current'])]	
	stateid = str(char['Scenes']['States'][str(char['Scenes']['Current'])])
	return Collate(scenedata, stateid)	
	
def CollateEncounter() :
	global adv
	global char
	encounterinfo = char['Scenes']['Encounters'][str(char['Scenes']['Current'])]
	encounterdata = adv.f['encounters'][str(encounterinfo[0])]
	stateid = str(encounterinfo[1])
	return Collate(encounterdata, stateid)
	
def CollateAbilities() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for ability in char['Abilities'].keys() :
		abilitydata = adv.f['abilities'][str(ability)]
		stateid = char['Abilities'][str(ability)]
		lists = Collate(abilitydata, stateid)
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result
	
def CollateItems() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for item in char['Items'].keys() :
		itemdata = adv.f['items'][str(item)]
		stateid = char['Items'][str(item)]
		lists = Collate(itemdata, stateid)
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result
	
def CollateVitals() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for vital in char['Vitals'].keys() :
		itemdata = adv.f['vitals'][str(vital)]
		stateid = char['Vitals'][str(vital)][0]
		lists = Collate(itemdata, str(stateid))
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result

def CollateAttributes() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for attribute in char['Attributes'].keys() :
		itemdata = adv.f['attributes'][str(attribute)]
		stateid = char['Attributes'][str(attribute)][0]
		lists = Collate(itemdata, str(stateid))
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result

def Collate(aspectdata,stateid) :
	global actiongroups
	result = {'white':[],'black':[]}
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
		result['white'] += aspectdata[stateid]['wlist']
	except KeyError : pass
	try :
		for grp in aspectdata[stateid]['wlistagrp'] :
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
	try :
		result['black'] += aspectdata[stateid]['blist']
	except KeyError : pass
	try :
		for grp in aspectdata[stateid]['blistagrp'] :
			try :
				result['black'] += actiongroups[str(agrp)]['list']
			except KeyError : pass
	except KeyError : pass
	return result