###############################################################
#Thought codes by Armando
###############################################################


#This program will create a matrix of coordinates. The SEM will
#determine the WD at each of these coordinates.

import numpy as np



x_i = 100.                      #starting x position
y_i = 35.
fov = 2.408                    #how many mm we'll move across
x_n = 1                        #dummy variable

coords = []                     #empty list where we'll store the x vals

n = 0
m = 0

while x_n >= 0:                        #dummy variable used to get the while loop started
    
   # if x_n == 1:                      #needed to create a local variable n
     #   n = 0
        
    x_n = x_i - n*fov                  #new x posistion
    y_m = y_i - m*fov
    n = n+1
                        
    if x_n < 0:                        #once we reach neg x values, set x_n = 0.
        x_n = 0.               
        n = 0                          #reset n index when we reach the end
        m = m + 1                      #increase m index by 1 to change y_m
         
    if y_m < - 65:                     #the while loop will run forever unless a bound is placed
        y_m = -65                      #hope this works
    
    
    coords.append([x_n, y_m])          #adds the calculated x_n to the list coord
    
    if y_m == -65 and x_n == 0:
        break
    
lcoords = list(coords)                 #converts the tuple created above into a list
acoords = np.array(lcoords)            #converts the list above into a numpy array. Nothing to do with accordians.

print acoords
