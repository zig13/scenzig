from random import randint
char = None

def GiveChar(c) : #Called from the main script to give this module access to the character configobj (i.e. as a dictionary)
	global char
	char = c

def d(sides) :
	global randint
	return randint(1,sides)
def a(id) :
	global char
	if str(id) in char['Attributes'].keys() :
		return char['Attributes'][str(id)][1]
	else : #If the character does not a currency of the given ID, it is taken to be 0.
		return 0
def v(id) :
	global char
	if str(id) in char['Vitals'].keys() :
		return char['Vitals'][str(id)][1]
	else : #If the character does not a vital of the given ID, it is taken to be 0.
		return 0
def c(id) :
	global char
	if str(id) in char['Currencies'].keys() :
		return char['Currencies'][str(id)]
	else : #If the character does not a currency of the given ID, it is taken to be 0.
		return 0

def PrsArg(arg) :
	try :
		opcounts = {'+':arg.count('+'), '-':arg.count('-'), 'x':arg.count('x')}
		try :
			return int(arg)
		except ValueError :
			pass #Argument is not an int yet so process it some more
		optotal = sum(opcounts.values())
		if optotal == 0 : #If the argument is not yet a number but has no operators. At this point the argument is expected to be something like d8 or v4.
			try :
				return eval(arg[0]+"("+arg[1:]+")") #Calls d, a, v or c with the rest of the argument as sides or id
			except TypeError: #This will occur is the input is something like 8/2. The code attempts to call 8 as a function which fails because it is an integer
				print "Sorry. The only operators I recognise at the moment are + (add), - (minus) and x (multiply)"
				return 0
			except NameError: #This will occur is the input is something like bert or b20
				print "The only letters I accept are d (dice roll), v (vital lookup), a (attribute lookup) and c (currency lookup). The letter should be immediately followed by the number of dice sides for d or ID for v, a and c."
				return 0
		elif optotal == 1 :
			oprtr = {vr: ky for ky, vr in opcounts.iteritems()}[1] #Inverts the opcounts dictionary so the count is the key and the operator is the value. We can then quickly find the operator with a count of 1
			tup = arg.partition(oprtr) #Creates a tuple that will look something like 'd8', '+', '4'
			operandA = tup[0]
			operandB = tup[2]
		elif optotal == 2 :
			if arg[-1] is not ")" :
				tup = arg.partition(")") #Creates a tuple that will look something like '(d8+4', ')', 'x2'
				operandA = tup[0][1:] #From the example above cuts out just d8+4
				oprtr = tup[2][0] #From the example above cuts out just x
				operandB = tup[2][1:] #From the example above cuts out just 2
			elif arg[0] is not "(" :
				tup = arg.partition("(") #Creates a tuple that will look something like '6+', '(', 'd6x2)'
				operandA = tup[0][:-1] #From the example above cuts out just 6
				oprtr = tup[0][-1] #From the example above cuts out just +
				operandB = tup[2][:-1] #From the example above cuts out just d6x2
			else : #This should only happen if someone has put in something like (d8+4)x(2)
				print "Please don't use brackets unnecessarily"
				return 0
		else : #This will occur if the input is something like (d8+4)x(2+d4) or ((d8+4)x2)-d10
			print "Sorry I can't deal with nested brackets at the moment :("
			return 0
		if oprtr is '+': return PrsArg(operandA)+PrsArg(operandB)
		elif oprtr is '-': return PrsArg(operandA)-PrsArg(operandB)
		elif oprtr is 'x': return PrsArg(operandA)*PrsArg(operandB)
	except AttributeError : #If argument is already an integer
		return arg
		
if __name__ == "__main__":
	print "Stuff"
	while True:
		prompt = str(raw_input(">"))
		print PrsArg(prompt)