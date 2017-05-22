adv = None
char = None
attributesbase = None
attributes = None
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c

def SetBaseAttributes() :
	global char
	global attributesbase
	attributesbase = dict((str(attribute), char['AttributeVals'][str(attribute)][0]) for attribute in char['Attributes']['active'])
def reBaseAttributes(id="all") :
	global attributesbase
	global attributes
	if id is "all" :
		attributes = dict(attributesbase)
	else :
		attributes[str(id)] = attributesbase[str(id)]
	
def CollateScene() :
	global adv
	global char
	scenedata = adv.f['Scenes'][str(char['Scenes']['active'][0])]	
	states = str(char['Scenes'][str(char['Scenes']['active'][0])])
	return Collate(scenedata, states)	
	
def CollateEncounter() :
	global adv
	global char
	encounterinfo = char['Encounters'][str(char['Scenes']['active'][0])]
	encounterdata = adv.f['Encounters'][str(encounterinfo[0])]
	states = str(encounterinfo[1])
	return Collate(encounterdata, states)
	
def CollateAbilities() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for ability in char['Abilities']['active'] :
		abilitydata = adv.f['Abilities'][str(ability)]
		states = str(char['Abilities'][str(ability)])
		lists = Collate(abilitydata, states)
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result
	
def CollateItems() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for item in char['Items']['active'] :
		itemdata = adv.f['Items'][str(item)]
		states = str(char['Items'][str(item)])
		lists = Collate(itemdata, states)
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result

def CollateAttributes() :
	global adv
	global char
	result = {'white':[],'black':[]}
	for attribute in char['Attributes']['active'] :
		itemdata = adv.f['Attributes'][str(attribute)]
		states = str(char['Attributes'][str(attribute)][0])
		lists = Collate(itemdata, str(states))
		result['white'] += lists['white']
		result['black'] += lists['black']
	return result

	{scenes}
	
	
def Collate(aspectdata,states) :
	global actiongroups
	result = {'white':[],'black':[]}
	CollateModifiers(aspectdata)
	try : 
		result['white'] += aspectdata['wlist']
	except KeyError : pass
	try :
		result['black'] += aspectdata['blist']
	except KeyError : pass

	for state in states :
		CollateModifiers(aspectdata,state)
		try :
			result['white'] += aspectdata[str(state)]['wlist']
		except KeyError : pass
		try :
			result['black'] += aspectdata[str(state)]['blist']
		except KeyError : pass
	return result

def CollateModifiers(aspectdata,state=False) :
	if state :
		for attribute in attributes.keys() :
			try : attributes[attribute] += aspectdata[str(state)]['attributebonuses'][attribute]
			except KeyError : pass
			try : attributes[attribute] -= aspectdata[str(state)]['attributepenalties'][attribute]
			except KeyError : pass
	else :
		for attribute in attributes.keys() :
			try : attributes[attribute] += aspectdata['attributebonuses'][attribute]
			except KeyError : pass
			try : attributes[attribute] -= aspectdata['attributepenalties'][attribute]
			except KeyError : pass
def CapModifiers() :
	for attribute in attributes.keys() :
		if attributes[attribute] > char['AttributeVals'][attribute][1]:
			attributes[attribute] = char['AttributeVals'][attribute][1]
		elif attributes[attribute] < 0 :
			attributes[attribute] = 0