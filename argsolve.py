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
	if char is None:
		print "Character data not available"
		return 0
	if str(id) in char['Attributes'].keys() :
		return char['Attributes'][str(id)][1]
	else : #If the character does not have an attribute of the given ID, it is taken to be 0.
		return 0
def v(id) :
	global char
	if char is None:
		print "Character data not available"
		return 0
	if str(id) in char['Vitals'].keys() :
		return char['Vitals'][str(id)][1]
	else : #If the character does not have a vital of the given ID, it is taken to be 0.
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
def i(id) : #i will return 1 if the character has an item of the given id in thier inventory else 0
	global char
	if char is None:
		print "Character data not available"
		return 0
	if str(id) in char['Items'].keys() :
		return 1
	else : return 0
def s(id) : #s has two functions. If passed 0 it will return the current scene else it will return the state of the given scene
	global char
	if char is None:
		print "Character data not available"
		return 0
	if id is 0 :
		return char['Scene']['Current']
	else :
		try :
			return char['SceneStates'][str(id)]
		except KeyError :
			return 0

def Solve(arg) :
	if isinstance(arg, list) :
		return [Solve(each) for each in arg]	
	try :
		opcounts = {'+':arg.count('+'), '-':arg.count('-'), 'x':arg.count('x'), '^':arg.count('^'), '_':arg.count('_'), '~':arg.count('~'), '%':arg.count('%')}
		try :
			return int(arg)
		except ValueError :
			pass #Argument is not an int yet so process it some more
		optotal = sum(opcounts.values())
		if optotal == 0 : #If the argument is not yet a number but has no operators. At this point the argument is expected to be something like d8 or v4.
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
	except AttributeError : #If argument is already an integer
		return arg
		
if __name__ == "__main__":
	print "I can roll dice for you!"
	while True:
		prompt = str(raw_input(">"))
		if prompt is not "" : print Solve(prompt)