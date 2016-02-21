adv = None
char = None
import argparser
from effects import *
def GiveAdv(a) :
	global adv
	adv = a
def GiveChar(c) :
	global char
	char = c
	argparser.GiveChar(char)
	
def AutoState(datafile) :
	thing = None
	if datafile is "vitals" :
		lst = char['Vitals'].keys()
		currstate = lambda: char['Vitals'][thing][0]
	elif datafile is 'attributes' :
		lst = char['Attributes'].keys()
		currstate = lambda: char['Attributes'][thing][0]
	elif datafile is 'scenes' :
		lst = [char['scenes']['current']]
		currstate = char['scenes']['states'][char['scenes']['current']]
	elif datafile is "encounters" :
		lst = [char['encounters'][char['scenes']['current']][0]]
		currstate = char['encounters'][char['scenes']['current']][1]
#	elif datafile is "items" :
#		lst = char['items']
#		currstate =	
	
	for thing in lst :
		evaluators = [argparser.PrsArg(each) for each in adv.f[datafile][thing]['evaluators']]
		for state in adv.f[datafile][str(thing)].keys() :
			this = True
			try :
				for test in adv.f[datafile][thing][state]['evaluations'].keys() :
					if not adv.f[datafile][thing][state]['evaluations'][test][0] <= evaluators[test] <= adv.f[datafile][thing][state]['evaluations'][test][1] :
						this = False
						break
			except TypeError : this = False
			if this is True : break
		if this is True :
			if currstate() != int(state) :			
				for effect in adv.f[datafile][str(thing)][str(currstate())]['leaveeffects'].keys() :
					arguments = argparser.PrsArg(adv.f[datafile][str(thing)][str(currstate())]['leaveeffects'][effect])
					eval(effect+"(arguments)")
				if datafile is 'vitals' : char['Vitals'][thing][0] = int(state)
				elif datafile is 'attributes' : char['Attributes'][thing][0] = int(state)
				elif datafile is 'scenes' : char['scenes']['states'][char['scenes']['current']] = int(state)
				elif datafile is "encounters" : char['scenes']['encounters'][char['scenes']['current']][1] = int(state)
#				elif datafile is "items" :
				for effect in adv.f[datafile][str(thing)][state]['entereffects'].keys() :
					arguments = argparser.PrsArg(adv.f[datafile][str(thing)][state]['entereffects'][effect])
					eval(effect+"(arguments)")