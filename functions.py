from os import name, system
from re import sub
from unicodedata import normalize
from string import ascii_letters, digits
def Clr() :
	if name == 'posix': #If OS is linux-based
		system('clear') #Executes the shell command 'clear' which clears the terminal in Linux
	elif (name == 'nt') or (name == 'ce') or (name == 'dos') : #If OS is Windows
		system('cls') #Executes the shell command 'cls' which clears the terminal in Windows
	else :
		print "\n" * 10

def yesno() :
	output = None
	while output == None :
		input = raw_input(">")
		Clr()
		if input.isdigit() :
			output = bool(input)
		elif input.isalpha() :
			input = input.lower()
			if (input == 'y') or (input == 'yes') or (input == 'sure') or (input == 'ja') or (input == 'ok') or (input == 'affirmitive') :
				output = True
			elif (input == 'n') or (input == 'no') or (input == 'nah') or (input == 'nein') or (input == 'nope') or (input == 'negative') :
				output = False
			else :
				print "Input not recognised"
		else :
			print "Input not recognised"
	return output

def choicelist(inlist, custom=False) :
	outlist = []
	for element in range(len(inlist)) :
		outlist.append("%s) %s" %(element+1,inlist[element]))
	printout = '\n'.join(outlist)
	while True :	
		if custom == False:
			print "Please enter a number corresponding to an option below:\n", printout
		else : print custom+"\n", printout
		try :		
			input = raw_input(">")
			Clr()
			input = int(input)
			return [input,inlist[input-1]]
			break
		except ValueError :
			print "Input must be a whole number.\n"
		except IndexError :
			print "Input is outside of range of options.\n"
			
def dupremove(seq) :
   seen = {}
   result = []
   for item in seq:
       if item in seen: continue
       seen[item] = 1
       result.append(item)
   return result
   
def valremove(seq,val) :
	if val in seq :
		return [x for x in seq if x != val]
		
def replace_all(text, dic):
    for k, l in dic.iteritems():
        text = text.replace(k, l)
    return text

def get_valid_filename(filename):
	validFilenameChars = "-_.() %s%s" % (ascii_letters, digits)
	cleanedFilename = normalize('NFKD', unicode(filename, errors='ignore')).encode('ASCII', 'ignore')
	return ''.join(c for c in cleanedFilename if c in validFilenameChars).strip().replace(' ', '_')
	
def nonemptyprint(string):
	try :
		print string+"\n"
	except TypeError :
		return