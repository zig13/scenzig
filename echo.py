#-------------------------------------------------------------------------------
# Thie file is part of scenzig
# Purpose:     An engine for text-based adventure games and interactive prose using a scene-based system.
#
# Author:      Thomas Sturges-Allard
#
# Created:     09/01/2016
# Copyright:   (c) Thomas Sturges-Allard 2016-2017
# Licence:     scenzig is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#              scenzig is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#              You should have received a copy of the GNU General Public License along with scenzig. If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
Echoes = {}
EchoCategories = {'1':[]}
index = 1

def Initialize(c) :
	global char
	global Echoes
	global EchoCategories
	global index
	char = c
	Echoes = char['Echoes'] #Copies echo information from the character file to the echo script
	EchoCategories = char['EchoCategories']
	try :
		index = int(list(char['Echoes'])[-1]) + 1 #On startup sets index to 1 higher than the current highest index
	except IndexError:
		index = 1 #If there are no active echoes at startup then index is left at 1

def Start(action, interval, categories, reps) :
	global index
	Echoes[str(index)] = {'action':action,'interval':interval,'categories':categories,'elapsed':0,'reps':reps}
	for category in categories :
		if category : #If the category is non 0
			try :
				EchoCategories[str(category)].append(str(index))
			except KeyError :
				EchoCategories[str(category)] = [str(index)]
		else : #If the category is 0...
			break #The echo is not listed under any categories
	index += 1
	char['Echoes'] = Echoes #Copies the echo script's echo information back to the character file
	char['EchoCategories'] = EchoCategories
	char.write()

def Stop(categor) : #Argument can be a single category or list of categories
	global Echoes
	try : #If categor is a single category
		int(categor) #Will fail if categories is already a list i.e. there are multiple categories
		if categor is 0 :
			Echoes.clear() #If the argument of 0 is given, all echoes are stopped/destroyed
			EchoCategories.clear()
		else :
			for echo in EchoCategories(str(categor)) :
				for category in Echoes[echo]['categories'] :
					try :
						EchoCategories[category].remove(echo)
					except ValueError :
						pass
				del Echoes[echo]
	except TypeError : #If categor is a list of categories
		echoesToStop = []
		for category in categor :
			echoesToStop.extend(char['EchoCategories'][str(category)])
			del EchoCategories[category]
		echoesToStop = list(dict.fromkeys(echoesToStop)) #Turns into dict and then back into list to remove duplicates
		for echo in echoesToStop :
			for category in Echoes[echo]['categories'] :
				try :
					EchoCategories[category].remove(echo)
				except ValueError :
					pass
			del Echoes[echo]
	char['Echoes'] = Echoes #Copies the echo script's echo information back to the character file
	char['EchoCategories'] = EchoCategories
	char.write()

def Age(beats) :
	actions = []
	for echo in Echoes.copy() :
		Echoes[echo]['elapsed'] += beats
		activations = Echoes[echo]['elapsed']/Echoes[echo]['interval']
		while activations >= 1 :
			actions.append(str(Echoes[echo]['action']))
			Echoes[echo]['elapsed'] -= Echoes[echo]['interval']
			activations = Echoes[echo]['elapsed']/Echoes[echo]['interval']
			try :
				Echoes[echo]['reps'] -= 1
				if Echoes[echo]['reps'] < 1 :
					del Echoes[echo]
					break
			except TypeError : #Will be raised if reps is Infinite
				pass
	char['Echoes'] = Echoes
	char.write()
	return actions
