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
from random import randint
from itertools import chain
from inspect import signature
import listcollate
from sys import modules
char = None

def GiveChar(c) : #Called from the main script to give this module access to the character configobj (i.e. as a dictionary)
	global char
	char = c

class letterFunctions :
	#These functions are in a class purely so they can be looked up using getattr()
	def d(strNumber,intNumber) : #Rolls a die with n sides
		if intNumber : #If intNumber is non-zero.
			return randint(1,intNumber)
		return 0

	def a(strNumber,intNumber) : #Returns the numerical value of an attribute
		return listcollate.attributes.get(strNumber,0) #If the attribute of the given ID is not found, 0 is returned

	def c(strNumber,intNumber) :
		return char['Currencies'].get(strNumber,0) #If the currency of the given ID is not found, 0 is returned

	def i(strNumber,intNumber) : #i will return the active inventory the item is present in else 0
		for inventory in char['Inventories'].keys()[1:] : #The first key 'active' is excluded using the [1:] slice
			if intNumber in char['Inventories'][inventory] :
				return int(inventory)
		return 0

	def t(strNumber,intNumber) : #t will return the lowest numbered state of the item with the given id
		itemStates = char['Items'].get(strNumber,[]) #If an item of the given ID isn't found assign an empty list
		return sorted(itemStates)[0] if itemStates else 0 #Get the first state if there are any else 0

	def s(strNumber,intNumber) : #s has two functions. If passed 0 it will return the current scene else it will return the state of the given scene
		if intNumber : #If number is non-zero
			sceneStates = char['Scenes'].get(strNumber,[]) #If a scene of the given ID isn't found assign an empty list
			return sorted(sceneStates)[0] if sceneStates else 0 #Get the first state if there are any else 0
		else : #If number is 0
			return char['Scenes']['active'][0]

	def n(strNumber,intNumber) : #Returns length of given Inventory
		inventory = char['Inventories'].get(strNumber,[])
		return len(inventory)

	def l(strNumber,intNumber) : #Returns the id of the label assigned to the given class. Retunns 0 if no label is assigned
		labelClass = char['Labels'].get(strNumber,[]) #If a class of the given ID isn't found assign and empty list
		return labelClass[0] if labelClass else 0

class wordFunctions :
	#These functions are in a class purely so they can be looked up using getattr()
	def SceneHasState(state, scene) : #SceneHasState requires two arguments; State and Scene. Example:SceneHasState,1,2
		return 1 if state in char['Scenes'].get(str(scene),[]) else 0

	def ItemIsActive(item) :
		return 1 if item in char['Items']['active'] else 0

	def ItemInInventory(item, inventory) : #ItemInInventory requires two arguments; Item and Inventory. Example:ItemInInventory,1,6
		return char['Inventories'].get(str(inventory),[]).count(item)

	def ItemHasState(state, item) : #ItemHasState requires two arguments; State and Item. Example:ItemHasState,1,4
		return 1 if state in char['Items'].get(str(item),[]) else 0

	def SlotIsActive(slot) : #Returns 1 if slot is empty or full otherwise 0
		if char.get('Slots') :
			if char['Slots'].get('full') and char['Slots'].get('empty') :
				return 1 if slot in chain(char['Slots']['full'],char['Slots']['empty']) else 0 #chain efficiently combines the full and empty lists
		print("Character file does not have a valid [Slots] section")
		return 0

	def SlotIsFull(slot) : #Returns 1 if slot is full otherwise 0
		if char.get('Slots') :
			if char['Slots'].get('full') :
				return 1 if slot in char['Slots']['full'] else 0
		print("Character file does not have a valid [Slots] section")
		return 0

	def SlotIsEmpty(slot) : #Returns 1 if slot is empty otherwise 0
		if char.get('Slots') :
			if char['Slots'].get('empty') :
				return 1 if slot in char['Slots']['empty'] else 0
		print("Character file does not have a valid [Slots] section")
		return 0

def Solve(arg) :
	try :
		return int(arg)
	except (ValueError, TypeError) :
		pass #Argument is not an int yet so process it some more
	if isinstance(arg, list) :
		return [Solve(each) for each in arg]
	opcounts = {'+':arg.count('+'), '-':arg.count('-'), 'x':arg.count('x'), '^':arg.count('^'), '_':arg.count('_'), '~':arg.count('~'), '%':arg.count('%')}
	optotal = sum(opcounts.values())
	if optotal == 0 : #If the argument is not yet a number but has no operators. At this point the argument is expected to be something like d8 or SceneHasState,1,1.
		if arg[:1].isupper() : #If the first character is an uppercase letter
			seperatedValues = arg.split(",") #Splits the string up based on comma placement
			words = seperatedValues[0]
			wordFunction = getattr(wordFunctions,words,None) #Returns a function matching the words given or returns None if it fails
			if wordFunction : #If a function was successfully found
				if char : #All the multi-word functions require access to a character so pointless to progress further if one is not available
					strArguments = seperatedValues[1:]
					if strArguments :
						try :
							intArguments = [int(x) for x in strArguments]
						except ValueError :
							print(f"{words} should be followed by it's numerical arguments seperated by commas e.g {words},3,6\nWhat it got was {strArguments}")
							return 0
						try :
							return wordFunction(*intArguments) #Only if all the conditions are passed will the function finnally be exexuted
						except TypeError :
							argumentsRequired = signature(wordFunction).parameters
							print(f"{words} requires exactly {len(argumentsRequired)} arguments but {len(intArguments)} was given\nThe format should be:")
							print(words, *argumentsRequired, sep=',')
					else :
						argumentsRequired = signature(wordFunction).parameters
						print(f"{words} is a valid function but needs to be followed by it's arguments in the format:")
						print(words, *argumentsRequired, sep=',')
				else :
					print("Character data not available")
			else :
				print(f"{words} is not a valid function")
				print("The multi-word functions are:",*dir(wordFunctions)[:7])
			return 0 #If any of the preceeding ifs are failed, bespoke error text is printed and then this line will be reached
		elif arg[:1].islower() : #If the first character is a lowercase letter
			letter = arg[0]
			strNumber = arg[1:]
			letterFunction = getattr(letterFunctions,letter,None) #Returns a function matching the letter given or returns None if it fails
			if letterFunction :
				if char or letter == "d": #d is the only function that does not require access to the a character
					if strNumber :
						try :
							intNumber = int(strNumber)
						except ValueError :
							print(f"Only a number should follow a single letter function\n{letter} was successfully called but {strNumber} is not a valid input for it.")
							return 0
						return letterFunction(strNumber,intNumber) #Only if all the conditions are passed will the function finnally be exexuted
					else :
						print(f"{letter} is a valid function but it needs an argument in the form of a number directly after it e.g {letter}6")
				else :
					print("Character data not available")
			else :
				print(f"{letter} is not a valid function")
				print("The single letter functions are: d (dice roll), a (attribute lookup), c (currency lookup), i (inventory item is in), t (item state lookup), s0 (current scene), s# (gives state of given scene), n (length of inventory) and l (id of label of given class).\nThe letter should be immediately followed by the number of dice sides for d or ID for the rest.")
		else : #This should only occur if the input is something like 8/2
			print("Sorry. The only operators I recognise at the moment are + (add), - (minus) and x (multiply)")
		return 0 #If any of the preceeding ifs are failed, bespoke error text is printed and then this line will be reached
	elif optotal == 1 :
		oprtr = {vr: ky for ky, vr in opcounts.items()}[1] #Inverts the opcounts dictionary so the count is the key and the operator is the value. We can then quickly find the operator with a count of 1
		tup = arg.partition(oprtr) #Creates a tuple that will look something like 'd8', '+', '4'
		operandA = Solve(tup[0])
		operandB = Solve(tup[2])
	elif optotal == 2 :
		if arg[-1] != ")" :
			tup = arg.partition(")") #Creates a tuple that will look something like '(d8+4', ')', 'x2'
			operandA = Solve(tup[0][1:]) #From the example above cuts out just d8+4
			oprtr = tup[2][0] #From the example above cuts out just x
			operandB = Solve(tup[2][1:]) #From the example above cuts out just 2
		elif arg[0] != "(" :
			tup = arg.partition("(") #Creates a tuple that will look something like '6+', '(', 'd6x2)'
			operandA = Solve(tup[0][:-1]) #From the example above cuts out just 6
			oprtr = tup[0][-1] #From the example above cuts out just +
			operandB = Solve(tup[2][:-1]) #From the example above cuts out just d6x2
		else : #This should only happen if someone has put in something like (d8+4)x(2)
			print("Please don't use brackets unnecessarily")
			return 0
	else : #This will occur if the input is something like (d8+4)x(2+d4) or ((d8+4)x2)-d10
		print("Sorry I can't deal with nested brackets at the moment :(")
		return 0
	if oprtr == '+': return Solve(operandA)+Solve(operandB)
	elif oprtr == '-': return Solve(operandA)-Solve(operandB)
	elif oprtr == 'x': return Solve(operandA)*Solve(operandB)
	elif oprtr == '^': return max(operandA,operandB) #Returns the greater of two operands
	elif oprtr == '_': return min(operandA,operandB)
	elif oprtr == '~': return (operandA+operandB)/2
	elif oprtr == '%': return (operandA*operandB)/100 #Returns operandA % of operandB

if __name__ == "__main__":
	adventure = None
	character = None
	if adventure and character : #adventure and character can be assigned so argsolve can access a character for testing purposes
		from os import curdir, sep
		from configobj import ConfigObj
		adventureFolder = f"{curdir}{sep}Adventures{sep}"
		characterFolder = f"{sep}Characters{sep}"
		char = ConfigObj(f"{adventureFolder}{adventure}{characterFolder}{character}.scz", unrepr=True, raise_errors=True)
	print("I can roll dice for you!")
	while True:
		prompt = str(input(">"))
		if prompt != "" : print(Solve(prompt))
