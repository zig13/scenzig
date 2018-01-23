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
