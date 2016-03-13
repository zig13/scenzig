from os import curdir, sep, access, R_OK #sep and curdir produce the correct characters for the operating system in use
from configobj import ConfigObj
class Adventure :
	datafiles = ['abilities', 'actions',  'actiongrps', 'attributes', 'currencies', 'encounters', 'items', 'main', 'scenes', 'vitals']
	def __init__(self, foldername) :
		self.directory = curdir+sep+"Adventures"+sep+foldername+sep
	def validate(self) :
		for datafile in self.datafiles :
			if not access(self.directory+datafile+".scnz", R_OK) : return False
		return True
	def load(self) :
		self.f = dict((datafile, ConfigObj(self.directory+datafile+".scnz", unrepr=True)) for datafile in self.datafiles) #Opens each data file up for reading referenced as an entry in the dictionary 'f'
		for datafile in self.datafiles :
			try:
				self.f[datafile]['0'] #Checks that a section exists in each data file entitled 0
			except:
				return False
		return True