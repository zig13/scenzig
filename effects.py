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
import echo
from functions import nonemptyprint
adv = None
char = {}
currentScene = 1
listcollate = None
statecheck = None
listg = []
actionstack = []
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	global currentScene
	char = c
	currentScene = char['Scenes']['active'][0]
	echo.Initialize(c)
def GiveListCollate(lcollate) :
	global listcollate
	listcollate = lcollate
def GiveStateCheck(scheck) :
	global statecheck
	statecheck = scheck
def GiveList(glist) :
	global listg
	listg = glist

def SetScene(scene) :
	global char
	global currentScene
	char['Scenes']['previous'] = char['Scenes']['active'][0]
	char['Scenes']['active'][0] = scene
	currentScene = scene
	listcollate.DeactivateThings('Scenes')
	listcollate.ActivateThings('Scenes')
	statecheck.Prepare('Scenes')
	statecheck.Check()
def RevertScene() :
	global char
	global currentScene
	temp = char['Scenes']['active'][0]
	char['Scenes']['active'][0] = char['Scenes']['previous']
	currentScene = char['Scenes']['previous']
	char['Scenes']['previous'] = temp
	listcollate.DeactivateThings('Scenes')
	listcollate.ActivateThings('Scenes')
	statecheck.Prepare('Scenes')
	statecheck.Check()
def AddSceneState(state, scene=None) :
	global char
	scene = currentScene if scene is None else scene #If scene isn't supplied, the current scene will be used
	if str(state) not in list(adv.f['Scenes'][str(scene)]) :
		print(f"Error: {state} is not a valid state for scene {scene}")
		return
	try :
		current_states = char['Scenes'][str(scene)]
	except KeyError :
		if str(scene) not in adv.f['Scenes'] : #If scene does not exist
			print("Scene",str(scene),"does not exist")
			return
		char['Scenes'][str(scene)] = []
		current_states = char['Scenes'][str(scene)]
		statecheck.auto_states['Scenes'][str(scene)] = [int(x) for x in statecheck.StripNonStates(adv.f['Scenes'][str(scene)]) if statecheck.HasEvaluations(adv.f['Scenes'][str(scene)][x])]
	if state not in current_states :
		current_states.append(state)
	if scene == currentScene :
		listcollate.AddStates('Scenes', scene)
		statecheck.Check()
def RemoveSceneState(state, scene=None) :
	global char
	scene = currentScene if scene is None else scene #If scene isn't supplied, the current scene will be used
	try :
		current_states = char['Scenes'][str(scene)]
	except KeyError :
		char['Scenes'][str(scene)] = []
		statecheck.UpdateAutoList('Scenes', scene)
		return
	if state : #If state is not 0
		char['Scenes'][str(scene)] = [x for x in current_states if x is not state]
	else : #All manually set states are removed if 0 is given as the 'state'
		if scene not in statecheck.auto_states['Scenes'] :
			statecheck.UpdateAutoList('Scenes', scene)
		char['Scenes'][str(scene)] = [x for x in current_states if x in statecheck.auto_states['Scenes'][scene]]
	if scene == currentScene :
		listcollate.RemoveStates('Scenes', scene)
		statecheck.Check()

def ListInventory(inventoryID=1,allowDupes=1) : #If an inventory is not specified, assume inventory 1. By default duplicates are allowed
	if allowDupes :
		inventory = char['Inventories'][str(inventoryID)]
	else :
		inventory = list(dict.fromkeys(char['Inventories'][str(inventoryID)])) #Turn into dictionary and then back into 
	for itm in inventory :
		states = sorted(char['Items'][str(itm)]) #States are sorted
		printed = False
		for state in states :
			printed = nonemptyprint(adv.f['Items'][str(itm)][str(state)],char)
			if printed is True : break #Once
		if printed is False : #Only if no state has text; print item's base text
			nonemptyprint(adv.f['Items'][str(itm)],char)
def PrintInventory(inventoryID=1) : #If an inventory is not specified, assume inventory 1
	for itm in sorted(char['Inventories'][str(inventoryID)]) :
		nonemptyprint(adv.f['Items'][str(itm)],char) #Print item's base text
		states = sorted(char['Items'][str(itm)]) #States are sorted
		for state in states :
			nonemptyprint(adv.f['Items'][str(itm)][str(state)],char)
def RemoveItem(item, inventoryID=1) : #If an inventory is not specified, assume inventory 1
	global char
	if item in char['Inventories'][str(inventoryID)] :
		char['Inventories'][str(inventoryID)].remove(item)
	if inventoryID in char['Inventories']['active'] :
		listcollate.CollateItems()
		statecheck.Prepare('Items')
		statecheck.Check()
def AddItem(item, inventoryID=1) : #Arguments are Item and Inventory
	global char
	try :
		if item not in char['Inventories'][str(inventoryID)] :
			char['Inventories'][str(inventoryID)].append(item)
			if inventoryID in char['Inventories']['active'] :
				listcollate.ActivateThings('Items')
	except KeyError : #If the given inventory does not exist yet this creates it
		char['Inventories'][str(inventoryID)] = [item]
	if inventoryID in char['Inventories']['active'] :
		listcollate.CollateItems()
		statecheck.Prepare('Items')
		statecheck.Check()
def TransferItem(item, inventoryOne, inventoryTwo) : #Arguments are item, inventoryOne and inventoryTwo
	global char
	if item in char['Inventories'].get(str(inventoryOne),default=[]) :
		char['Inventories'][str(inventoryOne)].remove(item)
		try :
			char['Inventories'][str(inventoryTwo)].append(item)
		except KeyError : #If the given inventory does not exist yet this creates it
			char['Inventories'][str(inventoryTwo)] = [item]
	if inventoryOne in char['Inventories']['active'] :
		listcollate.DeactivateThings('Items')
	if inventoryTwo in char['Inventories']['active'] :
		listcollate.ActivateThings('Items')
	if (inventoryOne in char['Inventories']['active']) or (inventoryTwo in char['Inventories']['active']) :
		listcollate.CollateItems()
		statecheck.Prepare('Items')
		statecheck.Check()
def AddItemState(state, item) : #Arguments are state and item
	global char
	try :
		current_states = char['Items'][str(item)]
	except KeyError :
		if str(item) not in adv.f['Items'] : #If item does not exist
			print("Item",str(item),"does not exist")
			return
		char['Items'][str(item)] = []
		current_states = char['Items'][str(item)]
		statecheck.auto_states['Items'][str(item)] = [int(x) for x in statecheck.StripNonStates(adv.f['Items'][str(item)]) if statecheck.HasEvaluations(adv.f['Items'][str(item)][x])]
	if state not in current_states :
		current_states.append(state)
		listcollate.AddStates('Items', item)
		statecheck.Check()
def RemoveItemState(state, item) : #Arguments are state and item
	global char
	try :
		current_states = char['Items'][str(item)]
	except KeyError :
		char['Items'][str(item)] = []
		statecheck.UpdateAutoList('Scenes', item)
		return
	if state : #If state is not 0.
		char['Items'][str(item)] = [x for x in current_states if x is not state]
	else : #All manually set states are removed if 0 is given as the 'state'
		if str(item) not in statecheck.auto_states['Items'] :
			statecheck.UpdateAutoList('Scenes', item)
		char['Items'][str(item)] = [x for x in current_states if x in statecheck.auto_states['Items'][str(item)]]	
	listcollate.RemoveStates('Items', item)
	statecheck.Check()

def RemoveAbility(ability) :
	global char
	if ability in char['Abilities']['active'] :
		char['Abilities']['active'].remove(ability)
	listcollate.DeactivateThings('Abilities')
	statecheck.Prepare('Abilities')
	statecheck.Check()
def AddAbility(ability) :
	global char
	if ability not in char['Abilities']['active'] :
		char['Abilities']['active'].append(ability)
	listcollate.ActivateThings('Abilities')
	statecheck.Prepare('Abilities')
	statecheck.Check()
def PrintActions() :
	global listg
	global adv
	for action in listg :
		try : #By trying to stick a space character on the end of 'commands', I can test if it is a string or a list
			command = adv.f['Actions'][str(action)]['commands']+" " #This will succeed only if 'commands' is a singular string
		except KeyError : #If the action has no commands
			continue #On the off-chance an action is whitelisted but has no commands, it will be ignored
		except TypeError: #If the action has a list of commands (rather than a singular string command)
			command = adv.f['Actions'][str(action)]['commands'][0]+" " #Takes the first command from the list
		try :
			description = "- "+adv.f['Actions'][str(action)]['description']
		except (KeyError, TypeError) : #Having a description is entirely optional so we don't care if we fail to find or it is not a string
			description = ""
		print(command+description) #If the action has a description, this will print e.g. "North - Travel North" else just "North "
def PrintAttributes() :
	global char
	global adv
	for attribute in char['Attributes']['active'] :
		if attribute not in char['Attributes']['vital'] :
			firststate = sorted(char['Attributes'][str(attribute)])[0] #Sorts the states and takes the first numerically
			nonemptyprint(adv.f['Attributes'][str(attribute)][str(firststate)],char)
def DamageAttribute(attribute, value) :
	global char
	if str(attribute) in char['Attributes'] :
		char['AttributeVals'][str(attribute)][0] -= value
		if char['AttributeVals'][str(attribute)][0] < 0 :
			char['AttributeVals'][str(attribute)][0] = 0
		if attribute in char['Attributes']['active'] :
			listcollate.SetBaseAttributes(attribute)
			listcollate.reBaseAttributes(attribute)
			listcollate.ApplyModifiers(attribute)
			statecheck.Check()
def BolsterAttribute(attribute, value) :
	global char
	if str(attribute) in char['Attributes'] :
		char['AttributeVals'][str(attribute)][0] += value
		try : #For each attribute, the character stores it's state, value and max value (list indexes 0,1,2). Below the value is set to the max value is it exceeds it.
			if char['AttributeVals'][str(attribute)][0] > char['AttributeVals'][str(attribute)][1] : char['AttributeVals'][str(attribute)][0] = char['AttributeVals'][str(attribute)][1]
		except IndexError:
			pass #Max value is optional
		if attribute in char['Attributes']['active'] :
			listcollate.SetBaseAttributes(attribute)
			listcollate.reBaseAttributes(attribute)
			listcollate.ApplyModifiers(attribute)
			statecheck.Check()

def ActivateSlot(slot) :
	global char
	if slot not in char['Slots']['empty'] and slot not in char['Slots']['full'] :
		char['Slots']['full'].append(slot)
def DeactivateSlot(slot) :
	global char
	if slot in char['Slots']['empty'] :
		char['Slots']['empty'] = [x for x in char['Slots']['empty'] if x is not slot]
	if slot in char['Slots']['full'] :
		char['Slots']['full'] = [x for x in char['Slots']['empty'] if x is not slot]
def FillSlot(slot) :
	global char
	if slot in char['Slots']['empty'] and slot not in char['Slots']['full'] :
		char['Slots']['full'].append(slot)
		char['Slots']['empty'] = [x for x in char['Slots']['empty'] if x is not slot]
def EmptySlot(slot) :
	global char
	if slot not in char['Slots']['empty'] and slot in char['Slots']['full'] :
		char['Slots']['empty'].append(slot)
		char['Slots']['full'] = [x for x in char['Slots']['empty'] if x is not slot]

def SetLabel(classID, labelID) : #Arguments are the class id and the id of the label to be assigned to it
	global char
	try :
		description = adv.f['Labels'][str(classID)][str(labelID)]['description']
		char['Labels'][str(classID)] = [labelID,description]
	except KeyError :
		if labelID == 0 :
			char['Labels'][str(classID)] = [0]
		else :
			print("Label to be assigned to the character does not exist")
			raise
	
def RemoveLabel(labelID) :
	global char
	if str(labelID) in char['Labels'] :
		char['Labels'][str(labelID)] = []

def TakeAction(action) : #Argument is Action ID
	actionstack.append(str(action))
def StartEcho(action, interval, categor=0, reps="Infinite") : #If not supplied, category will default to 0 and reps to infinite
	try : #If categor is a single category
		int(categor) #Will fail if categories is already a list i.e. there are multiple categories
		echo.Start(action, interval, [categor], reps) #echo.Start expects a list of categories so even if there is only one we make it a list
	except TypeError :	
		echo.Start(action, interval, categor, reps) #If categor is already a list we can pass it straight through
def StopEcho(categor) : #The argument is either a single category or a list of categories
	echo.Stop(categor)
	
def ClearStack() :
	global actionstack
	actionstack = []
