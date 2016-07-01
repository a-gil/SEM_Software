# -*- coding: utf-8 -*-

import numpy as np
#import sem

def func(x_0, y_0, x_max = 102, x_min = -2, y_max = 37, y_min = -65, delta = 1.8):
    """Aight, so you choose your starting position by inputting different x_0 and y_0 values. Default values will be used unless otherwise specified."""        
    #x_max, y_max be the top left corner, x_min, y_min be the lower right corner
    #The maxs and mins span an area.
    #(x_0, y_0) must lie within this grid and is the starting position of the beam.
    #the beam will move right from where it starts from
    #When it reaches the end, of the row (or x_0 = x_min) it will move down in y and back to x_0
    #delta is the spacing between points.
    
    if x_0 > x_max:
        return 'Error: input x is greater than maximum x-value'
    elif x_0 < x_min:
        return 'Error: input x is less than minimum x-value'
    elif y_0 > y_max:
        return 'Error: input y is greater than maximum y-value'
    elif y_0 < y_min:
        return 'Error: input y is less than minimum y-value'
    
    
    
    #This will make a list of 2-element tuples, which will be used as the coordinates of the beams location"
    ##########
    ##########
    
    x_n = x_min + 1                             #dummy variable, may be removed if we make the sub while-->for
    
    coords = []                                 #empty list where we'll store the coordinates
        
    n = 0
    m = 0
    
    while x_n >= x_min:                         #"dummy variable" used to get the while loop started
                    
        x_n = x_0 - n*delta                     #new x posistion
        y_m = y_0 + m*delta                     #new y position
        n = n+1
                                    
        if x_n < x_min:                         #once we reach x_min, set x = x_min
            x_n = x_min               
            n = 0                               #reset n index when we reach the end
            m = m + 1                           #increase m index by 1 to change y_m
                    
        if y_m > y_max:                         #place a bound on the y value
            y_m = y_max           
                
                
        coords = coords + [(round(x_n, 1), round(y_m, 1)),]          #adds the calculated x_n, y_m to the list coord
                
        if y_m == y_max and x_n == x_min:                            #breaks the loop when we reach the bottom corner
            break
    ##########   
    ##########
    
    #Now that we have the list, we can use it to assign the coordinates to the SEM
    ##########
    ##########
    
    i = 0                                       #define a certain magical index
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
    
    
    ##For loop is confusing.
    #for pair in coords:
    #    x,y = pair
    #    z = np.add(x,y)
    #    (x,y,z) = coords[pair]    #Will not accept pair as an argument bc it's defined as a tuple at start
        
    
    return coords

#coordinates = func(102, -65)
#print coordinates