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
	if arguments[0] not in char['Scenes']['States'].keys() : char['Scenes']['States'][arguments[0]] = 1
	if arguments[0] not in char['Scenes']['Encounters'].keys() : char['Scenes']['Encounters'][arguments[0]] = [0,1]
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
	char['Scenes']['States'][scene] = arguments[0]
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