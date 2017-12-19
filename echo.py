echoes = {}
categories = {'1':[]}
index = 1

def Start(action, interval, cat=1, reps="Infinite") :
	global index
	echoes[str(index)] = {'action':action,'interval':interval,'elapsed':0,'reps':reps}
	try :
		categories[str(cat)].append(str(index))
	except KeyError :
		categories[str(cat)] = [str(index)]
	index += 1

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
	return actions
