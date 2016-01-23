def SetScene(c,arguments) :
	c['Scenes']['Previous'] = c['Scenes']['Current']
	if arguments[0] not in c['Scenes']['States'].keys() : c['Scenes']['States'][arguments[0]] = 1
	c['Scenes']['Current'] = arguments[0]
def RevertScene(c,arguments) :
	temp = c['Scenes']['Current']
	c['Scenes']['Current'] = c['Scenes']['Previous']
	c['Scenes']['Previous'] = temp