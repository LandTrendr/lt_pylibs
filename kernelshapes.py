'''
kernelshapes.py

Class definitions for various kernel shapes.
Menu:
	- Circle (def: diameter)
	- Triangle (def: width,height,rectangle quadrant)
	- Pie slice (def: diameter, start angle, end angle, negative direction?)
	- Rectangle (def: width & height)
	
Author: Tara Larrue (tlarrue2991@gmail.com
'''

import cairo, math, lthacks, sys
import numpy as np

def defineShapeInstance(shapestring, shapedefs):
	'''defines a kernel based on a string of the shape and a list of kernel definitions'''
	
	shapestring = shapestring.strip().lower()

	if shapestring == "circle":
		shape = Circle(*shapedefs)
		
	elif shapestring == "rectangle":
		shape = Rectangle(*shapedefs)
		
	elif shapestring == "triangle":
		shape = Triangle(*shapedefs)
		
	elif shapestring == "pieslice":
		if len(shapedefs) == 4:
			if isinstance(shapedefs[3],str):
				try:
					shapedefs[3] = int(shapedefs[3])
				except ValueError:
					if shapedefs[3].strip().lower() == "false": shapedefs[3] = False
					elif shapedefs[3].strip().lower() == "true": shapedefs[3] = True
				
		shape = PieSlice(*shapedefs)
	
	else:
		menu = "rectangle, circle, triangle, pieslice"
		sys.exit("Invalid Kernel shape: " + shapestring + "\nMenu: " + menu)
		
	return shape

def geomSurface(width, height):

	# define geometric surface
	data = np.zeros((width, height, 4), dtype=np.uint8)
	surface = cairo.ImageSurface.create_for_data(
		data, cairo.FORMAT_ARGB32, width, height)
	cr = cairo.Context(surface)
	cr.set_antialias(cairo.ANTIALIAS_NONE)

	# fill with 1's
	cr.set_source_rgb(0.005, 0.005, 0.005)
	cr.paint()
	
	return cr, data
	
def extractMaskedKernel(data, width, height, ds, band, x, y, transform):

	# extract full rectangle kernel
	full_rectangle = lthacks.extract_kernel(
		ds, x, y, width, height, band, transform)
	
	if np.any(full_rectangle == -9999) or full_rectangle is None:
		return None, None
		
	else:
		# define a masked array so that stats can be computed
		mask = data[:,:,0]
		mx = np.ma.masked_array(full_rectangle, mask=mask)
	
		return mx, mx.data[~mx.mask]
		
	
		

class Circle:
	#define with a diameter
	
	def __init__(self, diameter):
		self.radius = int(diameter)/2.
		self.height = int(diameter)
		self.width = int(diameter)
		
	def extract_kernel(self, ds, band, x, y, transform):
	
		cr, data = geomSurface(self.width, self.height)
		
		# draw circle
		cr.arc(self.radius, self.radius, self.radius, 0, 2*math.pi)
		cr.set_source_rgb(0.0, 0.0, 0.0) #to get 0's 
		cr.fill()

		masked_array, data_only = extractMaskedKernel(data, self.width, self.height,  
		                                              ds, band, x, y, transform)
		
		return masked_array, data_only
		
		
class Triangle:
	#define with a width & height of rectangle kernel 
	#+ quadrant for triangle to be carved into

	def __init__(self, width, height, quadrant):
		self.width = int(width)
		self.height = int(height)
		self.quadrant = str(quadrant).strip().lower()
		self.midpoint = (math.ceil(int(width)/2.), math.ceil(int(height)/2.))
		
	def extract_kernel(self, ds, band, x, y, transform):
	
		cr, data = geomSurface(self.width, self.height)
		
		# draw triangle
		if self.quadrant == "west":
			cr.move_to(0,0)
			cr.line_to(0,self.height)
			
		elif self.quadrant == "north":
			cr.move_to(0,0)
			cr.line_to(self.width,0)
			
		elif self.quadrant == "east":
			cr.move_to(self.width,0)
			#cr.line_to(self.width-1,self.height-1)
			cr.line_to(self.width,self.height)
			
		elif self.quadrant == "south":
			cr.line_to(0,self.height)
			cr.line_to(self.width,self.height)
			
		else:
			sys.exit("Quadrant not understood: " + quadrant)
		
		cr.line_to(self.midpoint[0], self.midpoint[1])	
		
		#fill with 0's
		cr.set_source_rgb(0.0, 0.0, 0.0) 
		cr.fill()
		
		masked_array, data_only = extractMaskedKernel(data, self.width, self.height,  
		                                              ds, band, x, y, transform)
		
		return masked_array, data_only
		
		
class PieSlice:
	#define with a circle diameter, start & end angle on unit circle of pie arc,
	#and boolean for if you want the arc to be drawn in negative direction of unit circle

	def __init__(self, diameter, startangle, endangle, arcNegBool=False):
		self.radius = math.ceil(int(diameter)/2.)
		self.height = int(diameter)
		self.width = int(diameter)
		self.startangle = math.radians(float(startangle))
		self.endangle = math.radians(float(endangle))
		self.arcNeg = bool(arcNegBool)
		
	def extract_kernel(self, ds, band, x, y, transform):
	
		cr, data = geomSurface(self.width, self.height)
		
		# draw pie slice
		if self.arcNeg:
			cr.arc_negative(self.radius, self.radius, self.radius, self.startangle, 
			                self.endangle)
		else:
			cr.arc(self.radius, self.radius, self.radius, self.startangle, self.endangle)
		
		cr.line_to(self.radius, self.radius)
		circle_x = self.radius * math.cos(self.startangle) + self.radius
		circle_y = self.radius * math.sin(self.startangle) + self.radius
		cr.line_to(circle_x, circle_y)
		
		#fill with 0's
		cr.set_source_rgb(0.0, 0.0, 0.0)
		cr.fill()

		masked_array, data_only = extractMaskedKernel(data, self.width, self.height,  
		                                              ds, band, x, y, transform)
		
		return masked_array, data_only
		
class Rectangle:

	def __init__(self, width, height):
		self.height = int(width)
		self.width = int(height)

	def extract_kernel(self, ds, band, x, y, transform):
		
		#no need to mask the kernel
		full_rectangle = lthacks.extract_kernel(ds, x, y, self.width, self.height, band, 
		                                        transform)
		
		return full_rectangle, full_rectangle
		
	
		
	
#TESTING CODE -- shows shape as PNG		

# data = np.zeros((200, 200, 4), dtype=np.uint8)
# surface = cairo.ImageSurface.create_for_data(
#     data, cairo.FORMAT_ARGB32, 200, 200)
# cr = cairo.Context(surface)
# cr.set_antialias(cairo.ANTIALIAS_NONE)
# 
# # fill with solid white
# cr.set_source_rgb(1.0, 1.0, 1.0)
# cr.paint()
# 
# # draw shape
# #cr.arc(100, 100, 80, 0, 2*math.pi)
# radius = 100
# startangle = math.radians(120)
# endangle = math.radians(240)
# print startangle, endangle
# cr.arc(radius, radius, radius, startangle, endangle)
# #startptx = radius * math.cos(endangle) + radius
# 
# cr.line_to(radius, radius)
# circle_x = radius * math.cos(startangle) + radius
# circle_y = radius * math.sin(startangle) + radius
# print circle_x, circle_y
# cr.line_to(circle_x, circle_y)
# 
# cr.set_line_width(3)
# cr.set_source_rgb(1.0, 0.0, 0.0)
# #cr.stroke()
# cr.fill()
# 
# # write output
# print data[38:48, 38:48, 0]
# surface.write_to_png("./shape.png")
