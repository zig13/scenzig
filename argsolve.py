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
import listcollate
from sys import modules
char = None

def GiveChar(c) : #Called from the main script to give this module access to the character configobj (i.e. as a dictionary)
	global char
	char = c

def d(sides) :
	global randint
	return randint(1,sides)
def a(id) :
	global char
	attributes = listcollate.attributes
	if char is None:
		print "Character data not available"
		return 0
	if str(id) in attributes.keys() :
		return attributes[str(id)]
	else : #If the character does not have an attribute of the given ID, it is taken to be 0.
		return 0
def c(id) :
	global char
	if char is None:
		print "Character data not available"
		return 0
	if str(id) in char['Currencies'].keys() :
		return char['Currencies'][str(id)]
	else : #If the character does not have a currency of the given ID, it is taken to be 0.
		return 0
def i(id) : #i will return the active inventory the item is present in else 0
	global char
	if char is None:
		print "Character data not available"
		return 0
	inventories = [x for x in char['Inventories'].keys() if x.isdigit()]
	for inventory in inventories :
		if id in char['Inventories'][inventory] :
			return int(inventory)
	return 0
def t(id) : #t will return the (first) state of the item with the given id
	global char
	if char is None:
		print "Character data not available"
		return 0
	try :
		return sorted(char['Items'][str(id)])[0]
	except KeyError :
		return 0
def s(id) : #s has two functions. If passed 0 it will return the current scene else it will return the state of the given scene
	global char
	if char is None:
		print "Character data not available"
		return 0
	if id is 0 :
		return char['Scenes']['active'][0]
	else :
		try :
			return sorted(char['Scenes'][str(id)])[0]
		except KeyError :
			return 0
def n(id) : #Returns length of given Inventory
	if char is None:
		print "Character data not available"
		return 0
	try :
		return len(char['Inventories'][str(id)])
	except KeyError :
		return 0
def o(id) : #Returns 1 if slot is empty otherwise 0
	if char is None:
		print "Character data not available"
		return 0
	if id in char['Slots']['empty'] :
		return 1
	else :
		return 0
def l(id) : #Returns the id of the label assigned to the given class. Retunns 0 if not label is assigned
	if char is None:
		print "Character data not available"
		return 0
	try :
		return char['Labels'][str(id)][0]
	except (KeyError, IndexError) :
		return 0

def SceneHasState(arguments) :
	if char is None:
		print "Character data not available"
		return 0 #False
	if len(arguments) < 2 :
		print "SceneHasState requires two arguments; State and Scene.\nExample:SceneHasState,1,2"
		return 0 #False
	try :
		if int(arguments[0]) in char['Scenes'][arguments[1]] :
			return 1 #True
		else :
			return 0 #False
	except KeyError :
		return 0 #False
def ItemIsActive(arguments) :
	if char is None:
		print "Character data not available"
		return 0
	if int(arguments[0]) in char['Items']['active'] :
		return 1
	else :
		return 0
def ItemInInventory(arguments) : #Does not care if the inventory is active or not
	if char is None:
		print "Character data not available"
		return 0 #False
	if len(arguments) < 2 :
		print "ItemInInventory requires two arguments; Item and Inventory.\nExample:ItemInInventory,1,6"
		return 0 #False
	try :
		if int(arguments[0]) in char['Inventories'][arguments[1]] :
			return 1 #True
	except KeyError : pass
	return 0
def ItemHasState(arguments) :
	if char is None:
		print "Character data not available"
		return 0
	if len(arguments) < 2 :
		print "ItemHasState requires two arguments; State and Item.\nExample:ItemHasState,1,4"
		return 0 #False
	try :
		if int(arguments[0]) in char['Items'][arguments[1]] :
			return 1 #True
	except KeyError : pass
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
			csv = arg.split(",") #Splits the string up based on comma placement
			funct = csv[0]
			try :
				arguments = csv[1:]
			except IndexError :
				print "The function needs to be followed by it's arguments followed by commas e.g SceneHasStatus,3,6"
				return 0
			try :
				return eval(funct+"("+str(arguments)+")")
			except NameError :
				print '"'+funct+'"'+"is not valid"
				return 0
		try :
			return eval(arg[0]+"("+arg[1:]+")") #Calls d, a, v, i or c with the rest of the argument as sides or id
		except TypeError: #This will occur is the input is something like 8/2. The code attempts to call 8 as a function which fails because it is an integer
			print "Sorry. The only operators I recognise at the moment are + (add), - (minus) and x (multiply)"
			return 0
		except NameError: #This will occur is the input is something like bert or b20
			print "The only letters I accept are d (dice roll), v (vital lookup), a (attribute lookup), i (character has item), c (currency lookup) s0 (current scene) and s# (gives state of given scene).\nThe letter should be immediately followed by the number of dice sides for d or ID for v, a and c."
			return 0
		except SyntaxError:
			print "Only integers can follow d (dice roll), v (vital lookup), a (attribute lookup), i (character has item), c (currency lookup) and s (gives state of given scene)."
			return 0
	elif optotal == 1 :
		oprtr = {vr: ky for ky, vr in opcounts.iteritems()}[1] #Inverts the opcounts dictionary so the count is the key and the operator is the value. We can then quickly find the operator with a count of 1
		tup = arg.partition(oprtr) #Creates a tuple that will look something like 'd8', '+', '4'
		operandA = Solve(tup[0])
		operandB = Solve(tup[2])
	elif optotal == 2 :
		if arg[-1] is not ")" :
			tup = arg.partition(")") #Creates a tuple that will look something like '(d8+4', ')', 'x2'
			operandA = Solve(tup[0][1:]) #From the example above cuts out just d8+4
			oprtr = tup[2][0] #From the example above cuts out just x
			operandB = Solve(tup[2][1:]) #From the example above cuts out just 2
		elif arg[0] is not "(" :
			tup = arg.partition("(") #Creates a tuple that will look something like '6+', '(', 'd6x2)'
			operandA = Solve(tup[0][:-1]) #From the example above cuts out just 6
			oprtr = tup[0][-1] #From the example above cuts out just +
			operandB = Solve(tup[2][:-1]) #From the example above cuts out just d6x2
		else : #This should only happen if someone has put in something like (d8+4)x(2)
			print "Please don't use brackets unnecessarily"
			return 0
	else : #This will occur if the input is something like (d8+4)x(2+d4) or ((d8+4)x2)-d10
		print "Sorry I can't deal with nested brackets at the moment :("
		return 0
	if oprtr is '+': return Solve(operandA)+Solve(operandB)
	elif oprtr is '-': return Solve(operandA)-Solve(operandB)
	elif oprtr is 'x': return Solve(operandA)*Solve(operandB)
	elif oprtr is '^': return max(operandA,operandB) #Returns the greater of two operands
	elif oprtr is '_': return min(operandA,operandB)
	elif oprtr is '~': return (operandA+operandB)/2
	elif oprtr is '%': return (operandA*operandB)/100 #Returns operandA % of operandB

if __name__ == "__main__":
	print "I can roll dice for you!"
	while True:
		prompt = str(raw_input(">"))
		if prompt is not "" : print Solve(prompt)
