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
		print("\n" * 10)

def yesno() :
	output = None
	while output == None :
		prompt = input(">")
		Clr()
		if prompt.isdigit() :
			output = bool(input)
		elif prompt.isalpha() :
			prompt = prompt.lower()
			if (prompt == 'y') or (prompt == 'yes') or (prompt == 'sure') or (prompt == 'ja') or (prompt == 'ok') or (prompt == 'affirmitive') :
				output = True
			elif (prompt == 'n') or (prompt == 'no') or (prompt == 'nah') or (prompt == 'nein') or (prompt == 'nope') or (prompt == 'negative') :
				output = False
			else :
				print("Input not recognised")
		else :
			print("Input not recognised")
	return output

def choicelist(inlist, custom=False, allowzero=False) :
	outlist = []
	for counter, element in enumerate(inlist, 1) :
		outlist.append(f"{counter}) {element}") #Creates a list that'll look like ['1) First Option', '2) Second Option']
	statement = custom if custom else "Please enter a number corresponding to an option below:"
	while True :
		print(statement, *outlist, sep='\n')
		prompt = input(">")
		Clr()
		try :
			prompt = int(prompt)
		except ValueError :
			print("Input must be a whole number.\n")
			continue
		if prompt > 0 :
			try :
				elementText = inlist[prompt-1]
			except IndexError :
				print("Input is outside of range of options.\n")
				continue
			return elementText
		elif prompt == 0 and allowzero :
			return None
		print("Input must be a positive number.\n")

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
    for k, l in dic.items():
        text = text.replace(k, l)
    return text

def get_valid_filename(filename):
	validFilenameChars = "-_() %s%s" % (ascii_letters, digits)
	cleanedFilename = normalize('NFKD', filename)
	return ''.join(c for c in cleanedFilename if c in validFilenameChars).strip().replace(' ', '_')

def nonemptyprint(thing,char,field='text'):
	try :
		text = thing[field]
	except (TypeError, KeyError):
		return False
	if text[:6] == ".labs." :
		part = text.split('[')
		try :
			part = part[1].split(']')
		except KeyError :
			print("Missing '['")
			print("'.labs.' needs to be followed by a list of what labels are used in the text")
			print("For example: '.labs.[0]Helllo lab0 how are you?'")
			print("You put: "+text)
			return True
		labels = part[0].split(',')
		try :
			text = part[1]
		except KeyError :
			print("Missing ']'")
			print("'.labs.' needs to be followed by a list of what labels are used in the text")
			print("For example: '.labs.[0]Helllo lab0 how are you?'")
			print("You put: "+text)
			return True
		for label in labels :
			try :
				text = text.replace("lab"+str(label),char['Labels'][str(label)][1])
			except KeyError :
				print("Label with the ID of "+str(label)+" not found")
	print(text)
	return True
