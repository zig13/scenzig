echoes = {}
categories = {'1':[]}
index = 1

def Initialize(c) :
	global char
	global echoes
	global categories
	char = c
	echoes = char['Echoes']
	categories = char['EchoCats']	

def Start(action, interval, cat=1, reps="Infinite") :
	global index
	echoes[str(index)] = {'action':action,'interval':interval,'elapsed':0,'reps':reps}
	try :
		categories[str(cat)].append(str(index))
	except KeyError :
		categories[str(cat)] = [str(index)]
	index += 1
	char['Echoes'] = echoes
	char['EchoCats'] = categories
	char.write()

def Stop(category) :
	try :
		stopechoes = categories[category]
	except KeyError :
		if category == '0' :
			global echoes
			echoes = {} #If the argument of 0 is given, all echoes are stopped/destroyed
		return
	for echo in stopechoes :
		del echoes[echo]
	del categories[category]

def Age(beats) :
	actions = []
	for echo in echoes.keys() :
		echoes[echo]['elapsed'] += beats
		activations = echoes[echo]['elapsed']/echoes[echo]['interval']
		while activations >= 1 :
			actions.append(str(echoes[echo]['action']))
			echoes[echo]['elapsed'] -= echoes[echo]['interval']
			activations = echoes[echo]['elapsed']/echoes[echo]['interval']
			try :
				echoes[echo]['reps'] -= 1
				if echoes[echo]['reps'] < 1 :
					del echoes[echo]
					break
			except TypeError : #Will be raised if reps is Infinite
				pass
	char['Echoes'] = echoes
	char.write()
	return actions
