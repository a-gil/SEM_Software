# -*- coding: utf-8 -*-
#x_max = 102
#y_max = 65
#x_min = -2
#y_min = -37

def calc_coords(x_0, y_0, x_max = 102, y_max = 65, x_min = -2, y_min = -37, delta = 1.8):
    """Aight, so you choose you're starting position by inputting different x_0 and y_0 values. Default values will be used unless otherwise specified."""        
    #x_0 is our starting x position
    #y_0 is our starting y position
    #mins and maxs be where we don't want the stage to go past
    #delta is the spacing between points.
    
    if x_0 > x_max or x_0 < x_min or y_0 > y_max or y_0 < y_min:
        return 'Error: please ensure that the starting point is within sample range'
    
    x_n = x_min + 1                             #dummy variable, may be removed if we make the sub while-->for

    coords = ()                                 #empty tuple where we'll store the x vals
    
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
        
        
        coords = coords + ((x_n,y_m),)          #adds the calculated x_n to the list coord
        
        if y_m == y_max and x_n == x_min:       #break the loop when we reach the bottom corner
            break
        
    return coords

print calc_coords(102, 65)



#coordinates = calc_coords(100, 35, 2.048)
#print coordinates

#for pair in coordinates:
   # x, y = pair
    #feed x and y to SEM function to move SEM to those x, y coordinates
    #then call function to calculate WD at that coordinate
    #the WD calculated will be appended(?) to the coords tuple
    #each element of the coords tuple will be a 3 element tuple (x, y, z=WD)
    
