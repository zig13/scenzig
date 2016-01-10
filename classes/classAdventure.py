class Adventure :
	datafiles = ['abilities', 'actions',  'actiongrps', 'attributes', 'classifications', 'currencies', 'encounters', 'items', 'main', 'scenes', 'vitals']
	def __init__(self, foldername) :
		from os import curdir, sep
		self.directory = curdir+sep+"Adventures"+sep+foldername+sep
	def validate(self) :
		from os import access, R_OK
		for datafile in self.datafiles :
			if not access(self.directory+datafile+".scnz", R_OK) : return False
		print "Pass" #Temporary
		return True