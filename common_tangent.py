import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys

def find_common_tangent(x1, y1, x2, y2):    
    marr1 = np.array([]) #initialize slope and y intercept arrays
    marr2 = np.array([])
    barr1 = np.array([])
    barr2 = np.array([])
    
    for i in range(len(x1)-1): #calculate slope and y intercept for curve 1
        mval = (y1[i] - y1[i+1])/(x1[i]-x1[i+1])
        bval = y1[i] - mval*x1[i]
        marr1 = np.append(marr1, mval)
        barr1 = np.append(barr1, bval)
    
    for i in range(len(x2)-1): #calculate slope and y intercept for curve 2
        mval = (y2[i] - y2[i+1])/(x2[i]-x2[i+1])
        bval = y2[i] - mval*x2[i]
        marr2 = np.append(marr2, mval)
        barr2 = np.append(barr2, bval)
    
    dm = abs(marr1[0] - marr2[0])
    db = abs(barr1[0] - barr2[0])
    for i in range(len(marr1)): #simultaneously minimize difference
        for j in range(len(marr2)):
            if dm > abs(marr1[i]-marr2[j]) and db > abs(barr1[i]-barr2[j]):
                dm = abs(marr1[i]-marr2[j])
                db = abs(barr1[i]-barr2[j])
                m1 = marr1[i]
                m2 = marr2[j]
                b1 = barr1[i]
                b2 = barr2[j]
                
                u1 = x1[i]
                u2 = x2[j]
                v1 = y1[i]
                v2 = y2[j]
                
    mfinal = (v1-v2)/(u1-u2)
    bfinal = v2 - mfinal*u2
#   print "m1 = ", m1, ", m2 = ", m2, "b1 = ", b1, ", b2 = ", b2 
    print "Coordinates of points of tangency are: (%1.4f, %1.4f) and (%1.4f, %1.4f)" % (u1, v1, u2, v2)
    print "A1 = ", mfinal, ", A0 = ", bfinal
    
    return mfinal, bfinal
	

def equation(args):
	t = float(raw_input("Temperature: "))
	ua0 = 0
	ub0 = 13333.0
	a = 1.2
	b = 2.2
	E = 4.0e7
	de = 0.01

	e_line = np.linspace(-.07, .07, num=300)
	fa = ua0 - (a*(t**4))/12 + 0.5*E*(np.square(e_line))
	fb = ub0 - (b*(t**4))/12 + 0.5*E*(np.square(e_line-de))

	me, be = find_common_tangent(e_line, fa, e_line, fb)

	fig, ax = plt.subplots()
	p1 = plt.plot(e_line, fa, label = r'F$_{\alpha}$')
	p2 = plt.plot(e_line, fb, label = r'F$_{\beta}$')

	x_line = np.array(ax.get_xlim())
	y_line = be + me*x_line
	labelstring = 'y = %1.2fx + %1.2f' % (me, be)
	p3 = plt.plot(x_line, y_line, '--', label=labelstring)

	legend = ax.legend(loc='upper right')
	plt.title("Temperature vs. Strain")
	plt.xlabel(r'$\epsilon$')
	plt.ylabel(r'Temperature')
	plt.show()
	return None

def datadump(args):
	import pandas as pd
	s = ("This script reads columns of data copied from an Excel spreadsheet \n"\
	"and imports them for analysis. You will need to copy the desired range of points \n"\
	"from a spreadsheet for the x and y values for each set of curves. To get this to \n"\
	"work, copy the values to your clipboard (use CTRL + C or CMD + C) and press enter. \n"\
	"Do NOT paste values or press CTRL + V ! \n")
	print s
	r = raw_input("Please press enter to begin.")

	r1 = raw_input("Copy curve 1 x-values to clipboard, then press enter: ")
	x1 = pd.read_clipboard(header=None)
	x1 = x1.values

	print "x1 values read! \n"

	r2 = raw_input("Copy curve 1 y-values to clipboard, then press enter: ")
	y1 = pd.read_clipboard(header=None)
	y1 = y1.values
	
	print "y1 values read! \n"
	r3 = raw_input("Copy curve 2 x-values to clipboard, then press enter: ")
	x2 = pd.read_clipboard(header=None)
	x2 = x2.values
	
	print "x2 values read! \n"

	r4 = raw_input("Copy curve 2 y-values to clipboard, then press enter: ")
	y2 = pd.read_clipboard(header=None)
	y2 = y2.values
	
	print "y2 values read!"
	
	if x1.size != y1.size or x2.size != y2.size:
		print "Error: X and Y arrays must have the same dimensions. Exiting..."
		sys.exit()

	me, be = find_common_tangent(x1, y1, x2, y2)

	fig, ax = plt.subplots()
	
	p1 = plt.plot(x1, y1, label = r'U$_{\alpha}$')
	p2 = plt.plot(x2, y2, label = r'U$_{\beta}$')

	x_line = np.array(ax.get_xlim())
	y_line = be + me*x_line
	labelstring = 'y = %1.2fx + %1.2f' % (me, be)
	p3 = plt.plot(x_line, y_line, '--', label=labelstring)
	legend = ax.legend(loc='best')
	plt.title("Entropy vs. Internal Energy")
	plt.xlabel(r'U')
	plt.ylabel(r'S')
	plt.show()
	
	return None

if __name__ == "__main__":

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""
Description: This script will calculate the coefficients of the equation of a common tangent for two curves.
The program will accept parameters for the equation for free energy, or two sets of data values to generate the curves.
The matplotlib package is used to provide a visualization of the curves and the common tangent.
The pandas package is used to convert Excel column data into useable numpy arrays.
Currently, the script is only able to find the equation of a single common tangent. 
		""")
	subparsers = parser.add_subparsers()
	p_equation = subparsers.add_parser("equation", help="Generate curves by entering parameters for an equation. You will be prompted for a temperature value.")
	p_datadump = subparsers.add_parser("datadump", help="Generate curves by copying x and y values for two curves. You will be prompted to enter values. You need the pandas python package to run this script.")
	
	p_equation.set_defaults(func=equation)
	p_datadump.set_defaults(func=datadump)

	args = parser.parse_args()
	args.func(args)