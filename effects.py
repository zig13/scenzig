from functions import nonemptyprint
adv = None
char = None
listcollate = None
statecheck = None
listg = None
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c
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
	statecheck.Check()
def RevertScene(arguments) :
	global char
	temp = char['Scenes']['active'][0]
	char['Scenes']['active'][0] = char['Scenes']['previous']
	char['Scenes']['previous'] = temp
	listcollate.ActivateThings('Scenes')
	statecheck.Check()
def AddSceneState(arguments) :
	global char
	if len(arguments) <2 : arguments.append(char['Scenes']['active'][0]) #If no scene is given, the given state is added to the current scene
	try :
		current_states = char['Scenes'][str(arguments[1])]
	except KeyError :
		char['Scenes'][str(arguments[1])] = []
		current_states = char['Scenes'][str(arguments[1])]
		statecheck.auto_states['Scenes'][str(arguments[1])] = [int(x) for x in statecheck.StripNonStates(adv.f['Scenes'][str(arguments[1])].keys()) if statecheck.HasEvaluations(adv.f['Scenes'][str(arguments[1])][x])]
	if arguments[0] not in current_states :
		current_states.append(arguments[0])
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

def PrintItems(arguments) :
	global char
	global adv
	if len(arguments) < 1 : arguments.append(1) #If an inventory is not specified, assume inventory 1
	if arguments[0] not in char['Inventories']['active'] : return #Non-active inventories won't be printed
	if len(char['Inventories'][str(arguments[0])]) < 1 : return
	for itm in char['Inventories'][str(arguments[0])] :
		states = sorted(char['Items'][str(itm)])
		try :
			print adv.f['Items'][itm][str(states[0])]['description'] #Currently I am ~cheating and printing the description of the lowest number state the item currently has
		except KeyError :
			try :
				print adv.f['Items'][str(itm)]['description']
			except KeyError : pass
def RemoveItem(arguments) : #Arguments are Item and Inventory
	global char
	if len(arguments) < 2 : arguments.append(1)
	if arguments[0] in char['Inventories'][str(arguments[1])] :
		char['Inventories'][str(arguments[1])].remove(arguments[0])
	if arguments[1] in char['Inventories']['active'] :
		listcollate.CollateItems()
		statecheck.Check()
def AddItem(arguments) : #Arguments are Item, Inventory and Item State
	global char
	if len(arguments) < 2 : 
		arguments.append(1)
		if len(arguments) < 3 : arguments.append(1) #If no state is provided use state 1
	try :
		if arguments[0] not in char['Inventories'][str(arguments[1])] :
			char['Inventories'][str(arguments[1])].append(arguments[0])
			if arguments[1] in char['Inventories']['active'] :
				listcollate.ActivateThings('Items')
	except KeyError : #If the given inventory does not exist yet this creates it
		char['Inventories'][str(arguments[1])] = [arguments[0]]
	if arguments[1] in char['Inventories']['active'] :
		listcollate.CollateItems()
		statecheck.Check()
def RemoveAbility(arguments) :
	global char
	if str(arguments[0]) in char['Abilities'].keys() :
		del char['Abilities'][str(arguments[0])]
	statecheck.Prepare('Abilities')
def AddAbility(arguments) : #Is also able to change the state of an existing ability
	global char
	if len(arguments) < 2 : arguments.append(1) #If no state is provided use state 1
	char['Abilities'][str(arguments[0])] = [[arguments[1]],[]]
	statecheck.Prepare('Abilities')
def PrintActions(arguments) :
	global listg
	global adv
	if len(listg) == 0 : return
	for action in listg :
		try :
			print adv.f['Actions'][str(action)]['slug']+" - "+adv.f['Actions'][str(action)]['description']
		except KeyError :
			try :
				print adv.f['Actions'][str(action)]['slug']
			except KeyError : continue
def PrintAttributes(arguments) :
	global char
	global adv
	for attribute in char['Attributes']['active'] :
		if attribute not in char['Attributes']['vital'] :
			firststate = sorted(char['Attributes'][str(attribute)])[0] #Sorts the states and takes the first numerically
			nonemptyprint(adv.f['Attributes'][str(attribute)][str(firststate)])
def DamageAttribute(arguments) :
	global char
	if str(arguments[0]) in char['Attributes'].keys() :
		char['AttributeVals'][str(arguments[0])][0] -= arguments[1]
		if char['AttributeVals'][str(arguments[0])][1] < 0 :
			char['AttributeVals'][str(arguments[0])][1] = 0
		if arguments[0] in char['Attributes']['active'] :
			listcollate.SetBaseAttributes(arguments[0])
			listcollate.reBaseAttributes(arguments[0])
			listcollate.ApplyModifiers(arguments[0])
			statecheck.Check()
def BolsterAttribute(arguments) :
	global char
	if str(arguments[0]) in char['Attributes'].keys() :
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
def TakeAction(arguments) :
	action = arguments[0]
	nonemptyprint(adv.f['Actions'][action]['outcomes'][outcome]) #Action text will be printed if it exists
	for effect in adv.f['Actions'][action]['outcomes'][outcome]['effects'].keys() : #The line below runs the function requested by each effect of the chosen action and passes it any arguments from the Action.
		arguments = argparser.PrsArg(adv.f['Actions'][action]['outcomes'][outcome]['effects'][effect]['variables'])
		eval(adv.f['Actions'][action]['outcomes'][outcome]['effects'][effect]['function']+"(arguments)")