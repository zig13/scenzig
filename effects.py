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
char = None
listcollate = None
statecheck = None
listg = []
actionstack = []
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c
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

def SetScene(arguments) :
	global char
	char['Scenes']['previous'] = char['Scenes']['active'][0]
	char['Scenes']['active'][0] = arguments[0]
	listcollate.DeactivateThings('Scenes')
	listcollate.ActivateThings('Scenes')
	statecheck.Prepare('Scenes')
	statecheck.Check()
def RevertScene(arguments) :
	global char
	temp = char['Scenes']['active'][0]
	char['Scenes']['active'][0] = char['Scenes']['previous']
	char['Scenes']['previous'] = temp
	listcollate.DeactivateThings('Scenes')
	listcollate.ActivateThings('Scenes')
	statecheck.Prepare('Scenes')
	statecheck.Check()
def AddSceneState(arguments) :
	global char
	if len(arguments) <2 : arguments.append(char['Scenes']['active'][0]) #If no scene is given, the given state is added to the current scene
	try :
		current_states = char['Scenes'][str(arguments[1])]
	except KeyError :
		if str(arguments[1]) not in adv.f['Scenes'] : #If scene does not exist
			print("Scene",str(arguments[1]),"does not exist")
			return
		char['Scenes'][str(arguments[1])] = []
		current_states = char['Scenes'][str(arguments[1])]
		statecheck.auto_states['Scenes'][str(arguments[1])] = [int(x) for x in statecheck.StripNonStates(adv.f['Scenes'][str(arguments[1])]) if statecheck.HasEvaluations(adv.f['Scenes'][str(arguments[1])][x])]
	if arguments[0] not in current_states :
		current_states.append(arguments[0])
		listcollate.AddStates('Scenes', arguments[1])
		statecheck.Check()
def RemoveSceneState(arguments) : #Arguments are state and scene
	global char
	if len(arguments) <2 : arguments.append(char['Scenes']['active'][0]) #If no scene is given, the given state is removed from the current scene
	try :
		current_states = char['Scenes'][str(arguments[1])]
	except KeyError :
		char['Scenes'][str(arguments[1])] = []
		statecheck.UpdateAutoList('Scenes', arguments[1])
		return
	if arguments[0] is 0 : #All manually set states are removed if 0 is given as an argument
		if str(arguments[1]) not in statecheck.auto_states['Scenes'] :
			statecheck.UpdateAutoList('Scenes', arguments[1])
		char['Scenes'][str(arguments[1])] = [x for x in current_states if x in statecheck.auto_states['Scenes'][str(arguments[1])]]
	else :
		char['Scenes'][str(arguments[1])] = [x for x in current_states if x is not arguments[0]]
	listcollate.RemoveStates('Scenes', arguments[1])
	statecheck.Check()

def ListInventory(arguments) :
	if len(arguments) < 1 : arguments.append(1) #If an inventory is not specified, assume inventory 1
	if len(char['Inventories'][str(arguments[0])]) < 1 : return
	inventory = char['Inventories'][str(arguments[0])] #Items are not sorted (new at bottom)
	for itm in inventory :
		states = sorted(char['Items'][str(itm)]) #States are sorted
		printed = False
		for state in states :
			printed = nonemptyprint(adv.f['Items'][str(itm)][str(state)],char)
			if printed is True : break #Once
		if printed is False : #Only if no state has text; print item's base text
			nonemptyprint(adv.f['Items'][str(itm)],char)
def PrintInventory(arguments) :
	if len(arguments) < 1 : arguments.append(1) #If an inventory is not specified, assume inventory 1
	if len(char['Inventories'][str(arguments[0])]) < 1 : return
	inventory = sorted(char['Inventories'][str(arguments[0])]) #Items are sorted
	for itm in inventory :
		nonemptyprint(adv.f['Items'][str(itm)],char) #Print item's base text
		states = sorted(char['Items'][str(itm)]) #States are sorted
		for state in states :
			nonemptyprint(adv.f['Items'][str(itm)][str(state)],char)
def RemoveItem(arguments) : #Arguments are Item and Inventory
	global char
	if len(arguments) < 2 : arguments.append(1)
	if arguments[0] in char['Inventories'][str(arguments[1])] :
		char['Inventories'][str(arguments[1])].remove(arguments[0])
	if arguments[1] in char['Inventories']['active'] :
		listcollate.CollateItems()
		statecheck.Prepare('Items')
		statecheck.Check()
def AddItem(arguments) : #Arguments are Item and Inventory
	global char
	if len(arguments) < 2 :
		arguments.append(1)
	try :
		if arguments[0] not in char['Inventories'][str(arguments[1])] :
			char['Inventories'][str(arguments[1])].append(arguments[0])
			if arguments[1] in char['Inventories']['active'] :
				listcollate.ActivateThings('Items')
	except KeyError : #If the given inventory does not exist yet this creates it
		char['Inventories'][str(arguments[1])] = [arguments[0]]
	if arguments[1] in char['Inventories']['active'] :
		listcollate.CollateItems()
		statecheck.Prepare('Items')
		statecheck.Check()
def TransferItem(arguments) : #Arguments are Item, Inventory1 and Inventory2
	global char
	if len(arguments) < 3 :
		return
	if arguments[0] in char['Inventories'].get(str(arguments[1]),default=[]) :
		char['Inventories'][str(arguments[1])].remove(arguments[0])
		if arguments[0] not in char['Inventories'][str(arguments[1])] :
			try :
				char['Inventories'][str(arguments[2])].append(arguments[0])
			except KeyError : #If the given inventory does not exist yet this creates it
				char['Inventories'][str(arguments[1])] = [arguments[0]]
	if arguments[1] in char['Inventories']['active'] :
		listcollate.DeactivateThings('Items')
	if arguments[2] in char['Inventories']['active'] :
		listcollate.ActivateThings('Items')
	if (arguments[1] in char['Inventories']['active']) or (arguments[2] in char['Inventories']['active']) :
		listcollate.CollateItems()
		statecheck.Prepare('Items')
		statecheck.Check()
def AddItemState(arguments) : #Arguments are state and item
	global char
	try :
		current_states = char['Items'][str(arguments[1])]
	except KeyError :
		if str(arguments[1]) not in adv.f['Items'] : #If item does not exist
			print("Item",str(arguments[1]),"does not exist")
			return
		char['Items'][str(arguments[1])] = []
		current_states = char['Items'][str(arguments[1])]
		statecheck.auto_states['Items'][str(arguments[1])] = [int(x) for x in statecheck.StripNonStates(adv.f['Items'][str(arguments[1])]) if statecheck.HasEvaluations(adv.f['Items'][str(arguments[1])][x])]
	if arguments[0] not in current_states :
		current_states.append(arguments[0])
		listcollate.AddStates('Items', arguments[1])
		statecheck.Check()
def RemoveItemState(arguments) : #Arguments are state and item
	global char
	if len(arguments) <2 : arguments.append(char['Items']['active'][0]) #If no scene is given, the given state is removed from the current scene
	try :
		current_states = char['Items'][str(arguments[1])]
	except KeyError :
		char['Items'][str(arguments[1])] = []
		statecheck.UpdateAutoList('Scenes', arguments[1])
		return
	if arguments[0] is 0 : #All manually set states are removed if 0 is given as an argument
		if str(arguments[1]) not in statecheck.auto_states['Items'] :
			statecheck.UpdateAutoList('Scenes', arguments[1])
		char['Items'][str(arguments[1])] = [x for x in current_states if x in statecheck.auto_states['Items'][str(arguments[1])]]
	else :
		char['Items'][str(arguments[1])] = [x for x in current_states if x is not arguments[0]]
	listcollate.RemoveStates('Items', arguments[1])
	statecheck.Check()

def RemoveAbility(arguments) :
	global char
	if arguments[0] in char['Abilities']['active'] :
		char['Abilities']['active'].remove(arguments[0])
	listcollate.DeactivateThings('Abilities')
	statecheck.Prepare('Abilities')
	statecheck.Check()
def AddAbility(arguments) :
	global char
	if arguments[0] not in char['Abilities']['active'] :
		char['Abilities']['active'].append(arguments[0])
	listcollate.ActivateThings('Abilities')
	statecheck.Prepare('Abilities')
	statecheck.Check()
def PrintActions(arguments) :
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
def PrintAttributes(arguments) :
	global char
	global adv
	for attribute in char['Attributes']['active'] :
		if attribute not in char['Attributes']['vital'] :
			firststate = sorted(char['Attributes'][str(attribute)])[0] #Sorts the states and takes the first numerically
			nonemptyprint(adv.f['Attributes'][str(attribute)][str(firststate)],char)
def DamageAttribute(arguments) :
	global char
	if str(arguments[0]) in char['Attributes'] :
		char['AttributeVals'][str(arguments[0])][0] -= arguments[1]
		if char['AttributeVals'][str(arguments[0])][0] < 0 :
			char['AttributeVals'][str(arguments[0])][0] = 0
		if arguments[0] in char['Attributes']['active'] :
			listcollate.SetBaseAttributes(arguments[0])
			listcollate.reBaseAttributes(arguments[0])
			listcollate.ApplyModifiers(arguments[0])
			statecheck.Check()
def BolsterAttribute(arguments) :
	global char
	if str(arguments[0]) in char['Attributes'] :
		char['AttributeVals'][str(arguments[0])][0] += arguments[1]
		try : #For each attribute, the character stores it's state, value and max value (list indexes 0,1,2). Below the value is set to the max value is it exceeds it.
			if char['AttributeVals'][str(arguments[0])][0] > char['AttributeVals'][str(arguments[0])][1] : char['AttributeVals'][str(arguments[0])][0] = char['AttributeVals'][str(arguments[0])][1]
		except IndexError:
			pass #Max value is optional
		if arguments[0] in char['Attributes']['active'] :
			listcollate.SetBaseAttributes(arguments[0])
			listcollate.reBaseAttributes(arguments[0])
			listcollate.ApplyModifiers(arguments[0])
			statecheck.Check()

def ActivateSlot(arguments) :
	global char
	if arguments[0] not in char['Slots']['empty'] and arguments[0] not in char['Slots']['full'] :
		char['Slots']['full'].append(arguments[0])
def DeactivateSlot(arguments) :
	global char
	if arguments[0] in char['Slots']['empty'] :
		char['Slots']['empty'] = [x for x in char['Slots']['empty'] if x is not arguments[0]]
	if arguments[0] in char['Slots']['full'] :
		char['Slots']['full'] = [x for x in char['Slots']['empty'] if x is not arguments[0]]
def FillSlot(arguments) :
	global char
	if arguments[0] in char['Slots']['empty'] and arguments[0] not in char['Slots']['full'] :
		char['Slots']['full'].append(arguments[0])
		char['Slots']['empty'] = [x for x in char['Slots']['empty'] if x is not arguments[0]]
def EmptySlot(arguments) :
	global char
	if arguments[0] not in char['Slots']['empty'] and arguments[0] in char['Slots']['full'] :
		char['Slots']['empty'].append(arguments[0])
		char['Slots']['full'] = [x for x in char['Slots']['empty'] if x is not arguments[0]]

def SetLabel(arguments) : #Arguments are the class id and the id of the label to be assigned to it
	global char
	try :
		description = adv.f['Labels'][str(arguments[0])][str(arguments[1])]['description']
	except KeyError :
		print("Label to be assigned to the character does not exist")
		raise
	char['Labels'][str(arguments[0])] = [arguments[1],description]
def RemoveLabel(arguments) :
	global char
	if str(arguments[0]) in char['Labels'] :
		char['Labels'][str(arguments[0])] = []

def TakeAction(arguments) :
	actionstack.append(str(arguments[0]))
def StartEcho(arguments) :
	action = arguments[0]
	interval = arguments[1]
	try :
		categories = arguments[2]
	except IndexError :
		echo.Start(action, interval)
		return
	try :
		repetitions = arguments[3]
	except IndexError :
		echo.Start(action, interval, category)
		return
	echo.Start(action, interval, category, repetitions)
def StopEcho(arguments) :
	echo.Stop(str(arguments[0]))
def ClearStack(arguments) :
	global actionstack
	actionstack = []
