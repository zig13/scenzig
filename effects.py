import statecheck
from functions import nonemptyprint
adv = None
char = None
listg = None
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c
def GiveList(glist) :
	global listg
	listg = glist

def SetScene(arguments) :
	global char
	char['Scene']['Previous'] = char['Scene']['Current']
	char['Scene']['Current'] = arguments[0]
	if str(arguments[0]) not in char['SceneStates'].keys() : char['SceneStates'][str(arguments[0])] = [[],[]]
	statecheck.PrepareScene() #PrepareScene needs there to be a record for the new scene so the above generates an empty one
	statecheck.CheckScene() #If CheckScene dosn't come up with anything then the below line sets the state to 1
	if (not char['SceneStates'][str(arguments[0])][0]) and (not char['SceneStates'][str(arguments[0])][1]) : char['SceneStates'][str(arguments[0])] = [[1],[]]
	if str(arguments[0]) not in char['Encounters'].keys() : char['Encounters'][str(arguments[0])] = [0, [[],[]]]
	statecheck.PrepareEncounter()
	statecheck.CheckEncounter()
	if (not char['Encounters'][str(arguments[0])][1][0]) and (not char['Encounters'][str(arguments[0])][1][1]) : char['Encounters'][str(arguments[0])] = [0, [[1],[]]]
def RevertScene(arguments) :
	global char
	temp = char['Scene']['Current']
	char['Scene']['Current'] = char['Scene']['Previous']
	char['Scene']['Previous'] = temp
	statecheck.PrepareScene()
	statecheck.CheckScene()
def SetSceneState(arguments) :
	global char
	try :
		scene = arguments[1]
	except IndexError : #If scene is not given then set scene state of current scene
		scene = char['Scene']['Current']
	try :
		char['SceneStates'][str(scene)][0] = [arguments[0]]
	except KeyError :
		char['SceneStates'][str(scene)] = [[arguments[0]],[]]
def PrintItems(arguments) :
	global char
	global adv
	if len(char['Items']) == 0 : return
	print "You are carrying:"
	for itm in char['Items'].keys() :
		states = sorted(char['Items'][itm][0] + char['Items'][itm][1])
		try :
			print adv.f['items'][itm][str(states[0])]['description'] #Currently I am ~cheating and printing the description of the lowest number state the item currently has
		except KeyError :
			try :
				print adv.f['items'][str(itm)]['description']
			except KeyError : pass
	print ""
def RemoveItem(arguments) :
	global char
	if str(arguments[0]) in char['Items'].keys() :
		del char['Items'][str(arguments[0])]
	statecheck.PrepareItems()
def AddItem(arguments) : #Is also able to change the state of an existing item
	global char
	if len(arguments) < 2 : arguments.append(1) #If no state is provided use state 1
	char['Items'][str(arguments[0])] = [[arguments[1]],[]]
	statecheck.PrepareItems()
def RemoveAbility(arguments) :
	global char
	if str(arguments[0]) in char['Abilities'].keys() :
		del char['Abilities'][str(arguments[0])]
	statecheck.PrepareAbilities()
def AddAbility(arguments) : #Is also able to change the state of an existing ability
	global char
	if len(arguments) < 2 : arguments.append(1) #If no state is provided use state 1
	char['Abilities'][str(arguments[0])] = [[arguments[1]],[]]
	statecheck.PrepareAbilities()
def PrintActions(arguments) :
	global listg
	global adv
	if len(listg) == 0 : return
	for action in listg :
		try :
			print adv.f['actions'][str(action)]['slug']+" - "+adv.f['actions'][str(action)]['description']
		except KeyError :
			try :
				print adv.f['actions'][str(action)]['slug']
			except KeyError : continue
	print ""
def PrintAttributes(arguments) :
	global char
	global adv
	for attribute in char['Attributes'].keys() :
		firststate = (sorted(char['Attributes'][attribute][0][0] + char['Attributes'][attribute][0][1]))[0] #Merges the two state lists into 1, sorts them and takes the first numerically
		nonemptyprint(adv.f['attributes'][str(attribute)][str(firststate)])
def DamageVital(arguments) :
	global char
	if str(arguments[0]) in char['Vitals'].keys() :
		char['Vitals'][str(arguments[0])][1] -= arguments[1]
		if char['Vitals'][str(arguments[0])][1] < 0 : char['Vitals'][str(arguments[0])][1] = 0
def BolsterVital(arguments) :
	global char
	if str(arguments[0]) in char['Vitals'].keys() :
		char['Vitals'][str(arguments[0])][1] += arguments[1]
		try : #For each vital, the character stores it's state, value and max value (list indexes 0,1,2). Below the value is set to the max value is it exceeds it.
			if char['Vitals'][str(arguments[0])][1] > char['Vitals'][str(arguments[0])][2] : char['Vitals'][str(arguments[0])][1] = char['Vitals'][str(arguments[0])][2]
		except IndexError:
			pass #Max value is optional
def DamageAttribute(arguments) :
	global char
	if str(arguments[0]) in char['Attributes'].keys() :
		char['Attributes'][str(arguments[0])][1] -= arguments[1]
		if char['Attributes'][str(arguments[0])][1] < 0 : char['Attributes'][str(arguments[0])][1] = 0
def BolsterAttribute(arguments) :
	global char
	if str(arguments[0]) in char['Attributes'].keys() :
		char['Attributes'][str(arguments[0])][1] += arguments[1]
		try : #For each attribute, the character stores it's state, value and max value (list indexes 0,1,2). Below the value is set to the max value is it exceeds it.
			if char['Attributes'][str(str(arguments[0]))][1] > char['Attributes'][str(str(arguments[0]))][2] : char['Attributes'][str(str(arguments[0]))][1] = char['Attributes'][str(str(arguments[0]))][2]
		except IndexError:
			pass #Max value is optional
def TakeAction(arguments) :
	action = arguments[0]
	nonemptyprint(adv.f['actions'][action]['outcomes'][outcome]) #Action text will be printed if it exists
	for effect in adv.f['actions'][action]['outcomes'][outcome]['effects'].keys() : #The line below runs the function requested by each effect of the chosen action and passes it any arguments from the Action.
		arguments = argparser.PrsArg(adv.f['actions'][action]['outcomes'][outcome]['effects'][effect]['variables'])
		eval(adv.f['actions'][action]['outcomes'][outcome]['effects'][effect]['function']+"(arguments)")