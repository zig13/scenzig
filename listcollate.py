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
statecheck = None
collated = {'allowedActions':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'blockedActions':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'allowedInventories':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'blockedInventories':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'bonuses':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}},'penalties':{'Abilities':{}, 'Attributes':{}, 'Encounters':{}, 'Items':{}, 'Scenes':{}}}
actions = None
attributesbase = {}
attributes = {}
from functions import dupremove
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c

def Setup(statecheck_passed) :
	global statecheck
	statecheck = statecheck_passed
	for aspect in collated['allowedActions'] :
		ActivateThings(aspect)
	CollateInventories()

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
	collatedthings = [int(x) for x in collated['allowedActions'][aspect]] #Converts the list keys to integers so they can be compared to the active list in the character file
	statecheck.Prepare(aspect)
	for thing in set(char[aspect]['active']).difference(collatedthings) : #Finds things that haven't been collated yet
		for collection in collated :
			collated[collection][aspect][str(thing)] = {}
		if aspect is "Attributes" :
			SetBaseAttributes(thing)
			reBaseAttributes(thing)
			ApplyModifiers(thing)
		AddStates(aspect, thing)

def DeactivateThings(aspect) :
	global collated
	global actions
	alteredcollections = []
	collatedthings = [int(x) for x in collated['allowedActions'][aspect]] #Converts the list keys to integers so they can be compared to the active list in the character file
	statecheck.Prepare(aspect)
	for thing in set(collatedthings).difference(char[aspect]['active']) : #Finds things that haven't been collated yet
		for collection in collated :
			for state in collated[collection][aspect][str(thing)] :
				if collated[collection][aspect][str(thing)][str(state)] :
					alteredcollections.append(collection)
			del collated[collection][aspect][str(thing)]
	if ("allowedActions" in alteredcollections) or ("blockedActions" in alteredcollections) :
		actions = None
	if "allowdInventories" in alteredcollections or "blockedInventories" in alteredcollections :
		CollateInventories()
	if "bonuses" in alteredcollections or "penalties" in alteredcollections :
		reBaseAttributes()
		ApplyModifiers()

def AddStates(aspect, thing) :
	global collated
	global actions
	alteredcollections = []
	if str(thing) in char[aspect] : #If the character has encountered the thing before
		collatedstates = [int(x) for x in collated['allowedActions'][aspect].get(str(thing),{})] #Converts the list keys to integers so they can be compared to the state list in the character file
		states = list(char[aspect][str(thing)])
		states.append(0)
		states = set(states).difference(collatedstates) #Finds states that haven't been collated yet. Will also collate base values of the thing (as state 0) if they haven't been already
	else : #If the character has not encountered the thing before. Therefore it can be assumed that nothing is collated
		char[aspect][str(thing)] = []
		states = []
		states.append(0)
	for state in states :
		for collection in collated :
			if collection is not "bonuses" and collection is not "penalties" :
				collated[collection][aspect][str(thing)][str(state)] = []
			else :
				collated[collection][aspect][str(thing)][str(state)] = {}
			if state : #If state is non-zero i.e. a state and not base thing values
				try :
					collated[collection][aspect][str(thing)][str(state)] = adv.f[aspect][str(thing)][str(state)][collection]
					alteredcollections.append(collection)
				except KeyError : pass
			else :
				try :
					collated[collection][aspect][str(thing)][str(state)] = adv.f[aspect][str(thing)][collection]
					alteredcollections.append(collection)
				except KeyError : pass
	if ("allowedActions" in alteredcollections) or ("blockedActions" in alteredcollections) :
		actions = None
	if "allowedInventories" in alteredcollections or "blockedInventories" in alteredcollections :
		CollateInventories()
	if "bonuses" in alteredcollections or "penalties" in alteredcollections :
		ApplyModifiers()

def RemoveStates(aspect, thing) :
	global collated
	global actions
	alteredcollections = []
	collatedstates = [int(x) for x in collated['allowedActions'][aspect].get(str(thing),{})] #Converts the list keys to integers so they can be compared to the state list in the character file
	for state in set(collatedstates).difference(char[aspect][str(thing)]) : #Finds states that are no longer valid but have been collated
		if state : #If state is non-zero. Without this things granted from the base (stored as state 0) would also be removed
			for collection in collated :
				if collated[collection][aspect][str(thing)][str(state)] :
					alteredcollections.append(collection)
				del collated[collection][aspect][str(thing)][str(state)]
	if "allowedActions" in alteredcollections or "blockedActions" in alteredcollections :
		actions = None
	if "allowedInventories" in alteredcollections or "blockedInventories" in alteredcollections :
		CollateInventories()
	if "bonuses" in alteredcollections or "penalties" in alteredcollections :
		reBaseAttributes()
		ApplyModifiers()


def CollateInventories() :
	activeInventories = ActiveList('allowedInventories', 'blockedInventories')
	if set(activeInventories) != set(char['Inventories']['active']) :
		unlistedInventories = [x for x in activeInventories if str(x) not in char['Inventories']]
		for inventory in unlistedInventories :
			char['Inventories'][str(inventory)] = []
		char['Inventories']['active'] = activeInventories
		CollateItems()

def CollateItems() :
	activeItems = []
	for inventory in char['Inventories']['active'] :
		activeItems.extend(char['Inventories'][str(inventory)])
	if set(activeItems) != set(char['Items']['active']) :
		char['Items']['active'] = activeItems
		DeactivateThings('Items')
		ActivateThings('Items')

def CollateActions() :
	global actions
	if actions is None:
		actions = ActiveList("allowedActions", "blockedActions")
	return actions

def ActiveList(allow, block) :
	allowList = []
	blockList = []
	for aspect in collated[allow] :
		for thing in collated[allow][aspect] :
			for state in collated[allow][aspect][thing] :
				allowList.extend(collated[allow][aspect][thing][state])
				blockList.extend(collated[block][aspect][thing][state])
	return [x for x in dupremove(allowList) if x not in blockList]

def CollateModifiers() :
	bonuslist = []
	penaltylist = []
	for aspect in collated["bonuses"] :
		for thing in collated["bonuses"][aspect] :
			for state in collated["bonuses"][aspect][thing] :
				bonuslist.append(collated["bonuses"][aspect][thing][state])
				penaltylist.append(collated["penalties"][aspect][thing][state])
	return [bonuslist, penaltylist]

def ApplyModifiers(attribute="all") :
	modifiers = CollateModifiers()
	bonuses = modifiers[0]
	penalties = modifiers[1]
	if attribute is "all" : todo = char['Attributes']['active']
	else : todo = [attribute]
	for attribute in todo :
		for bonus in bonuses :
			try : attributes[str(attribute)] += bonus[attribute]
			except KeyError : pass
		for penalty in penalties :
			try : attributes[str(attribute)] -= penalty[str(attribute)]
			except KeyError :
				pass

def CapModifiers() :
	for attribute in attributes :
		if attributes[attribute] > char['AttributeVals'][attribute][1]:
			attributes[attribute] = char['AttributeVals'][attribute][1]
		elif attributes[attribute] < 0 :
			attributes[attribute] = 0
