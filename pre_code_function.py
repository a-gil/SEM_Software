# -*- coding: utf-8 -*-

#from __future__ import print_function

import numpy as np

print('Start')

#import sys

#import os

#sys.path.append(os.path.join(os.getcwd(), 'remote'))

#import time

#import sem

#import struct

#from sem_v3_lib import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

#args will hold the arguments for the functions. This is the format of the arguments:
#args = [x_0, y_0, x_max, x_min, y_max, y_min, delta]
#Edit the list below to use its arguments.
args = [5, 35]

def calc_coords(x_0, y_0, x_max = 102, x_min = -2, y_max = 37, y_min = -65, delta = 1.8):
    """This function simply creates a rectangular area to scan over. """ \
    """The min and max values are ideally where the stage touches the chamber walls. """\
    """x_0 and y_0 must lie within this area. This function will move the electron """\
    """beam to the given point, then move onto the next one based on the spacing delta."""
    
    if x_0 > x_max:
        
        return 'Error: input x must be smaller'
        
    elif x_0 < x_min:
        
        return 'Error: input x must be larger'
        
    elif y_0 > y_max:
        
        return 'Error: input y must be smaller'
        
    elif y_0 < y_min:
        
        return 'Error: input y must be larger'
    
    
    
#    The following makes a list of 2-element tuples
#    and they will be used as the coordinates of the beam's location

########################
########################
    
   #dummy variable, may be removed if we make the sub while-->for    
    x_n = x_min + 1
    
   #empty list where we'll store the coordinates 
    coords = []
    
   #define indices         
    n = 0
    m = 0
    
   #"dummy variable" used to get the while loop started 
    while x_n >= x_min:                         
                    
        x_n = x_0 - n*delta                 #new x posistion
        y_m = y_0 + m*delta                 #new y position
        n = n+1
                                    
        if x_n < x_min:                     #once we reach x_min, set x = x_min
            x_n = x_min               
            n = 0                           #reset n index when we reach the end
            m = m + 1                       #increase m index by 1 to change y_m
                    
        if y_m > y_max:                     #place a bound on the y value
            y_m = y_max           
                
       #add the calculated x_n, y_m to the list coord         
        coords = coords + [(round(x_n, 1), round(y_m, 1)),]
        
       #break the loop when we reach the bottom corner                 
        if y_m == y_max and x_n == x_min:
            break
    
    return coords
    
########################
########################

def TakeImgs(*args):
    """This function takes the coordinates calculated from calc_coords and feeds """\
    """them to the SEM. At each point, an image is taken. """\
    """CAUTION: please make sure to alter the max and min values if a custom stage is being used."""
    
    coords = calc_coords(*args)

    #Now that we have the list, we can use it to assign the coordinates to the SEM
    ##########
    ##########
    
    
    #define a certain magical index
    i = 0
    
    while i < len(coords):
        
        x, y = coords[i]
        
        #feed x,y to SEM function that moves stage
        #call SEM function that will calculate the WD at this point
        #let's say z = WD, but use a dummy function for testing
        
        z = np.add(x,y)
        
        #sem.StgMoveTo(x, y)
        #sem.AutoWD
        #z = sem.GetWD
        
        coords[i] = (x, y, round(z, 3))
        i = i+1
        
        


##Hello?
#Bruh, ay, ay Duval.
##Yeah, who this?
#Bruh thi--Bruh this Fool, bruh.
##Who?
#Fool, bruh, you with my hoe bruh
##I ain't with yo girl
#Bruh y'all in Atlantic Station, bruh. Somebody just call me, bruh. Why--
##What? What's yo girl name?
#Bruh I love that hoe bruh, why you playin' wit my hoe, bruh?
##What's her name?
#Britney, nigga! What the fuck, you know that my hoe!