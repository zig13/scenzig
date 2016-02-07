from random import randint
from re import findall
operators = ['+', '-', 'x']
char = None

def GiveChar(c) :
	global char
	char = c

def d(sides) :
	global randint
	return randint(1,sides)
def a(id) :
	global char
	if str(id) in char['Attributes'].keys() :
		return char['Attributes'][str(id)][1]
	else :
		return 0
def v(id) :
	global char
	if str(id) in char['Vitals'].keys() :
		return char['Vitals'][str(id)][1]
	else :
		return 0
def c(id) :
	global char
	if str(id) in char['Currencies'].keys() :
		return char['Currencies'][str(id)]
	else :
		return 0

def PrsArg(arg) :
	global operators
	global findall
	try :
		opcounts = {'+':arg.count('+'), '-':arg.count('-'), 'x':arg.count('x')}
		try :
			return int(arg)
		except ValueError :
			pass #Argument is not an int yet so process it some more
		optotal = sum(opcounts.values())
		if optotal == 0 :
			return eval(arg[0]+"("+arg[1:]+")") #Calls d, a, v or c with the rest of the argument as sides or id
		elif optotal == 1 :
			oprtr = {vr: ky for ky, vr in opcounts.iteritems()}[1]
			tup = arg.partition(oprtr)
			operandA = tup[0]
			operandB = tup[2]
		elif optotal == 2 :
			if arg[-1] is not ")" :
				tup = arg.partition(")")
				operandA = tup[0][1:]
				oprtr = tup[2][0]
				operandB = tup[2][1:]
			elif arg[0] is not "(" :
				tup = arg.partition("(")
				operandA = tup[0][:-1]
				oprtr = tup[0][-1]
				operandB = tup[2][:-1]
			else :
				print "Please don't use brackets unnecessarily"
				return 0
		else :
			print "Sorry I can't deal with nested brackets at the moment :("
			return 0
		if oprtr is '+': return int(PrsArg(operandA))+int(PrsArg(operandB))
		elif oprtr is '-': return int(PrsArg(operandA))-int(PrsArg(operandB))
		elif oprtr is 'x': return int(PrsArg(operandA))*int(PrsArg(operandB))
	except AttributeError : #If argument is an integer
		return arg