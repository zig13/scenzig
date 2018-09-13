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
from os import curdir, sep, access, R_OK #sep and curdir produce the correct characters for the operating system in use
from time import sleep
from configobj import ConfigObj
class Adventure :
	datafiles = ['abilities', 'actions', 'attributes', 'encounters', 'items', 'labels', 'scenes']
	def __init__(self, foldername) :
		self.foldername = foldername
		self.directory = curdir+sep+"Adventures"+sep+foldername+sep
		self.f = {}
	def validate(self) :
		for datafile in self.datafiles :
			if not access(self.directory+datafile+".scnz", R_OK) : return False
		return True
	def load(self) :
		for datafile in self.datafiles :
			try :
				data = {datafile.title(): ConfigObj(self.directory+datafile+".scnz", unrepr=True)}
			except SyntaxError as e :
				print("Problems found with the",datafile,"file of",self.foldername)
				errorlines = []
				for error in e.errors :
					errorlines.append(error.line_number)
				print("Check the following lines:", errorlines)
				input("\nPress enter to return to Adventure selection")
				return False
			self.f.update(data)
			try:
				self.f[datafile.title()]['0'] #Checks that a section exists in each data file entitled 0
			except:
				return False
		try :
			splash = open(self.directory+"splash.txt", "r")
		except IOError :
			print(self.directory+"splash.txt")
			return True
		try :
			duration = int(splash.readline()[30:])
		except ValueError :
			return True
		line = splash.readline()
		while line :
			print(line)
			line = splash.readline()
		sleep(duration)
		return True
