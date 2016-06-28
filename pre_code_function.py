def calc_coords(x_0, y_0, fov):
    #x_0 = 100.                      #starting x position
    #y_0 = 35.
    #fov = 2.408                    #how many mm we'll move across
    x_n = 1                        #dummy variable

    coords = ()                     #empty tuple where we'll store the x vals
    
    n = 0
    m = 0
    
    while x_n >= 0:                 #dummy variable used to get the while loop started
            
        x_n = x_0 - n*fov          #new x posistion
        y_m = y_0 - m*fov
        n = n+1
                            
        if x_n < 0:                #once we reach neg x values, set x_n = 0.
            x_n = 0.               
            n = 0                  #reset n index when we reach the end
            m = m + 1              #increase m index by 1 to change y_m
            
        if y_m < - 65:             #place a bound on the y value
            y_m = -65           
        
        
        coords = coords + ((x_n,y_m),)        #adds the calculated x_n to the list coord
        
        if y_m == -65 and x_n == 0:           #break the loop when we reach the bottom corner
            break
        
    return coords

coordinates = calc_coords(100, 35, 2.048)
print coordinates


