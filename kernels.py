'''
Data structures of various kernel shapes & sizes 
for extracting pixels from rasters.
UNFINISHED - NEVER IMPLEMENTED.
'''
import numpy as np 
import sys

#SQUARE
def Square():

	def __init__(self, size):
		self.size = __validSize(size)
		self.width = self.size
		self.height = self.size
		self.mask = np.ones((self.width, self.height))
		#self.midIndex

	def validSize(self, size):
		if (int(size) % 2 != 0) and int(size) > 0:
			return int(size)
		else:
			errMsg = "Size '"+ str(size) + "'' is not valid for Square. Must be an odd positive number."
			sys.exit(errMsg)


#CIRCLE
def Circle():

	def __init__(self, size):
		self.size = __validSize(size)
		self.width = self.size
		self.height = self.size
		self.mask = __calcMask()
		#self.midIndex

	def validSize(self, size):
		if (int(size) % 2 != 0) and int(size) >= 3:
			return int(size)
		else:
			errMsg = "Size '"+ str(size) + "'' is not valid for Square. Must be an odd number, 3 or greater."
			sys.exit(errMsg)

	def calcMask(self):
		base = np.ones((self.width, self.height))
		#define pixels to turn off
		if self.size == 3:
			delRange = [0]
		elif self.size == 5:
			delRange = [-1,0,1]
		elif self.size == 7:
			delRange = [-3,-2,-1,0,1,2]
		else:
			errMsg = "Size '", str(self.size), "' mask not yet defined."
			sys.exit(errMsg)

		for i in delRange:
			base[0,i] = 0 
			base[-1,i] = 0 
			base[i,-1] = 0
			base[i,0] = 0 

		return base



