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
	char['Scenes']['Previous'] = char['Scenes']['Current']
	if str(arguments[0]) not in char['Scenes']['States'].keys() : char['Scenes']['States'][str(arguments[0])] = 1
	if str(arguments[0]) not in char['Scenes']['Encounters'].keys() : char['Scenes']['Encounters'][str(arguments[0])] = [0,1]
	char['Scenes']['Current'] = arguments[0]
def RevertScene(arguments) :
	global char
	temp = char['Scenes']['Current']
	char['Scenes']['Current'] = char['Scenes']['Previous']
	char['Scenes']['Previous'] = temp
def SetSceneState(arguments) :
	global char
	try :
		scene = arguments[1]
	except IndexError : #If scene is not given then set scene state of current scene
		scene = char['Scenes']['Current']
	char['Scenes']['States'][str(scene)] = arguments[0]
def PrintItems(arguments) :
	global char
	global adv
	if len(char['Items']) == 0 : return
	print "You are carrying:"
	for itm in char['Items'] :
			print adv.f['items'][str(itm)]['description']
	print ""
def RemoveItem(arguments) :
	global char
	if arguments[0] in char['Items'] :
		char['Items'] = [x for x in char['Items'] if x != arguments[0]]
def AddItem(arguments) :
	global char
	char['Items'].append(arguments[0])
def RemoveAbility(arguments) :
	global char
	if arguments[0] in char['Abilities'] :
		char['Abilities'] = [x for x in char['Abilities'] if x != arguments[0]]
def AddAbility(arguments) :
	global char
	char['Abilities'].append(arguments[0])
def PrintActions(arguments) :
	global listg
	global adv
	if len(listg) == 0 : return
	for action in listg :
		if adv.f['actions'][str(action)]['description'] is None : 
			print adv.f['actions'][str(action)]['slug']
		else :
			print adv.f['actions'][str(action)]['slug']+" - "+adv.f['actions'][str(action)]['description']
	print ""
def PrintAttributes(arguments) :
	global char
	global adv
	for attribute in char['Attributes'].keys() :
			try :
				print adv.f['attributes'][str(attribute)][str(char['Attributes'][attribute][0])]['description']+"\n"
			except TypeError :
				pass
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
		char['Attributes'][str(str(arguments[0]))][1] += arguments[1]
		try : #For each attribute, the character stores it's state, value and max value (list indexes 0,1,2). Below the value is set to the max value is it exceeds it.
			if char['Attributes'][str(str(arguments[0]))][1] > char['Attributes'][str(str(arguments[0]))][2] : char['Attributes'][str(str(arguments[0]))][1] = char['Attributes'][str(str(arguments[0]))][2]
		except IndexError:
			pass #Max value is optional
def TakeAction(arguments) :
	action = arguments[0]
	nonemptyprint(adv.f['actions'][action]['outcomes'][outcome]['text']) #Action text will be printed if it exists
	for effect in adv.f['actions'][action]['outcomes'][outcome]['effects'].keys() : #The line below runs the function requested by each effect of the chosen action and passes it any arguments from the Action.
		arguments = argparser.PrsArg(adv.f['actions'][action]['outcomes'][outcome]['effects'][effect]['variables'])
		eval(adv.f['actions'][action]['outcomes'][outcome]['effects'][effect]['function']+"(arguments)")