adv = None
char = None
collated = {'wActions':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'bActions':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'wEncounters':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'bEncounters':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'wInventories':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'bInventories':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'Bonuses':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'Penalties':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}}}
attributesbase = {}
attributes = {}
from functions import dupremove
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c

def Setup(aspect_lists) :
	for aspect in aspect_lists.keys() :
		ActivateThings(aspect)	

def SetBaseAttributes(attribute="all") :
	global char
	global attributesbase
	if attribute is "all" : 
		attributesbase = dict((str(attribute), char['AttributeVals'][str(attribute)][0]) for attribute in char['Attributes']['active'])
	else :
		attributesbase[str(attribute)] = char['AttributeVals'][str(attribute)][0]
def reBaseAttributes(attribute="all") :
	global attributesbase
	global attributes
	if attribute is "all" :
		attributes = dict(attributesbase)
	else :
		attributes[str(attribute)] = attributesbase[str(attribute)]
	
def ActivateThings(aspect) :
	global collated
	alteredcollections = []
	collatedthings = [int(x) for x in collated['wActions'][aspect].keys()] #Converts the list keys to integers so they can be compared to the active list in the character file	
	for thing in set(char[aspect]['active']).difference(collatedthings) : #Finds things that haven't been collated yet		
		for collection in collated :			
			if collection is not "bonuses" and collection is not "penalties" :
				collated[collection][aspect][str(thing)] = {'0':[]}
			else :
				collated[collection][aspect][str(thing)] = {'0':{}}
			try :
				collated[collection][aspect][str(thing)]['0'] = adv.f[aspect][str(thing)][collection]
				alteredcollections.append(collection)
			except KeyError : pass
		if aspect is "Attributes" :
			SetBaseAttributes(thing)
			reBaseAttributes(thing)
			ApplyModifiers(thing)
		alteredcollections.extend(AddStates(aspect, str(thing)))
	return dupremove(alteredcollections)

def AddStates(aspect, thing) :
	global collated
	alteredcollections = []
	collatedstates = [int(x) for x in collated['wActions'][aspect][thing].keys()] #Converts the list keys to integers so they can be compared to the state list in the character file
	for state in set(char[aspect][thing]).difference(collatedstates) : #Finds states that haven't been collated yet
		for collection in collated :
			if collection is not "bonuses" and collection is not "penalties" :
				collated[collection][aspect][thing][str(state)] = []
			else :
				collated[collection][aspect][thing][str(state)] = {}
			try :
				collated[collection][aspect][thing][str(state)] = adv.f[aspect][thing][str(state)][collection]
				alteredcollections.append(collection)
			except KeyError : pass
	return dupremove(alteredcollections)

def GreyList(white, black) :
	whitelist = []
	blacklist = []
	for aspect in collated[white].keys() :
		for thing in collated[white][aspect].keys() :
			for state in collated[white][aspect][thing].keys() :
				whitelist.extend(collated[white][aspect][thing][state])
				blacklist.extend(collated[black][aspect][thing][state])
	if white is "Bonuses" : return [whitelist, blacklist]
	else : return [x for x in dupremove(whitelist) if x not in blacklist]

def ApplyModifiers(attribute="all") :
	grey = GreyList("Bonuses", "Penalties")
	bonuses = grey[0]
	penalties = grey[1]
	if attribute is "all" : todo = char['Attributes']['active']
	else : todo = [attribute]
	for attribute in todo :
		for bonus in bonuses :
			try : attributes[attribute] += bonus[attribute]
			except KeyError : pass
		for penalty in penalties :
			try : attributes[attribute] += penalty[attribute]
			except KeyError : pass

def CapModifiers() :
	for attribute in attributes.keys() :
		if attributes[attribute] > char['AttributeVals'][attribute][1]:
			attributes[attribute] = char['AttributeVals'][attribute][1]
		elif attributes[attribute] < 0 :
			attributes[attribute] = 0