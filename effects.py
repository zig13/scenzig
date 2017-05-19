import statecheck
from functions import nonemptyprint
from listcollate import SetBaseAttributes
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
	char['Scenes']['Previous'] = char['Scenes']['active'][0]
	char['Scenes']['active'][0] = arguments[0]
	if str(arguments[0]) not in char['Scenes'].keys()[2:] : char['Scenes'][str(arguments[0])] = []
	statecheck.Prepare('Scenes') #PrepareScene needs there to be a record for the new scene so the above generates an empty one
	statecheck.Check('Scenes') #If CheckScene dosn't come up with anything then the below line sets the state to 1
	if not char['Scenes'][str(arguments[0])] : char['Scenes'][str(arguments[0])] = [1]
	if str(arguments[0]) not in char['Encounters'].keys() : char['Encounters'][str(arguments[0])] = [0, [[],[]]]
	statecheck.Prepare('Encounters')
	statecheck.Check('Encounters')
	if (not char['Encounters'][str(arguments[0])][1][0]) and (not char['Encounters'][str(arguments[0])][1][1]) : char['Encounters'][str(arguments[0])] = [0, [[1],[]]]
def RevertScene(arguments) :
	global char
	temp = char['Scenes']['active'][0]
	char['Scenes']['active'][0] = char['Scenes']['previous']
	char['Scenes']['previous'] = temp
	statecheck.Prepare('Scenes')
	statecheck.Check('Scenes')
def AddSceneState(arguments) :
	global char
	if len(arguments) <2 : arguments.append(char['Scenes']['active'][0])
	if arguments[0] not in char['Scenes'][arguments[1]] :
		char['Scenes'][str(scene)].append(arguments[0])
def PrintItems(arguments) :
	global char
	global adv
	if len(char['Items']) == 0 : return
	print "You are carrying:"
	for itm in char['Inventories']['c'] :
		states = sorted(char['Items'][str(itm)])
		try :
			print adv.f['Items'][itm][str(states[0])]['description'] #Currently I am ~cheating and printing the description of the lowest number state the item currently has
		except KeyError :
			try :
				print adv.f['Items'][str(itm)]['description']
			except KeyError : pass
	print ""
def RemoveItem(arguments) : #Arguments are Item and Inventory
	global char
	if len(arguments) < 2 : arguments.append('c')
	if arguments[0] in char['Inventories'][str(arguments[1])] :
		char['Inventories'][str(arguments[1])].remove(arguments[0])
		statecheck.Prepare('Items')
def AddItem(arguments) : #Arguments are Item, Inventory and Item State
	global char
	if len(arguments) < 2 : 
		arguments.append('c')
		if len(arguments) < 3 : arguments.append(1) #If no state is provided use state 1
	if arguments[0] not in char['Inventories'][str(arguments[1])] :
		char['Inventories'][str(arguments[1])].append(arguments[0])
		statecheck.Prepare('Items')
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
	print ""
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
		char['Attributes'][str(arguments[0])][1] -= arguments[1]
		if char['Attributes'][str(arguments[0])][1] < 0 : char['Attributes'][str(arguments[0])][1] = 0
		SetBaseAttributes()
def BolsterAttribute(arguments) :
	global char
	if str(arguments[0]) in char['Attributes'].keys() :
		char['AttributeVals'][str(arguments[0])][0] += arguments[1]
		try : #For each attribute, the character stores it's state, value and max value (list indexes 0,1,2). Below the value is set to the max value is it exceeds it.
			if char['AttributeVals'][str(arguments[0])][0] > char['AttributeVals'][str(arguments[0])][1] : char['AttributeVals'][str(arguments[0])][0] = char['AttributeVals'][str(arguments[0])][1]
		except IndexError:
			pass #Max value is optional
		SetBaseAttributes()
def TakeAction(arguments) :
	action = arguments[0]
	nonemptyprint(adv.f['Actions'][action]['outcomes'][outcome]) #Action text will be printed if it exists
	for effect in adv.f['Actions'][action]['outcomes'][outcome]['effects'].keys() : #The line below runs the function requested by each effect of the chosen action and passes it any arguments from the Action.
		arguments = argparser.PrsArg(adv.f['Actions'][action]['outcomes'][outcome]['effects'][effect]['variables'])
		eval(adv.f['Actions'][action]['outcomes'][outcome]['effects'][effect]['function']+"(arguments)")