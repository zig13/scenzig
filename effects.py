def SetScene(c,a,arguments) :
	c['Scenes']['Previous'] = c['Scenes']['Current']
	if arguments[0] not in c['Scenes']['States'].keys() : c['Scenes']['States'][arguments[0]] = 1
	c['Scenes']['Current'] = arguments[0]
def RevertScene(c,a,arguments) :
	temp = c['Scenes']['Current']
	c['Scenes']['Current'] = c['Scenes']['Previous']
	c['Scenes']['Previous'] = temp
def SetSceneState(c,a,arguments) :
	try :
		scene = arguments[1]
	except IndexError : #If scene is not given then set scene state of current scene
		scene = c['Scenes']['Current']
	c['Scenes']['States'][scene] = arguments[0]
def PrintItems(c,a,arguments) :
	if len(c['Items']) == 0 : return
	print "You are carrying:"
	position = 0
	for itm in c['Items'] :
		position += 1
		if position != len(c['Items']) :
			print a.f['items'][str(itm)]['description']
		else :
			print a.f['items'][str(itm)]['description']+"\n"	
def RemoveItem(c,a,arguments) :
	from functions import valremove
	c['Items'] = valremove(c['Items'],arguments[0])
def AddItem(c,a,arguments) :
	c['Items'].append(arguments[0])