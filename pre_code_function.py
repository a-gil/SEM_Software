# -*- coding: utf-8 -*-

from __future__ import print_function

import numpy as np

print('Start')

import sys

import os

sys.path.append(os.path.join(os.getcwd(), 'remote'))

#import time

import sem

import struct

from sem_v3_lib import *

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

print("So far so good.")

SampleName = 'Stardust Track 191 Andromeda, 34 nm spot'

ImageWidth = 2000

ImageHeight = 2000

ImageOffsetx = 0#-0.2 # in microns

ImageOffsety = 0#0.1  # in microns

DriftCorrx = 0 # microns/frame

DriftCorry = 0 # microns/frame

DriftCorrz = 0 # microns/frame

NumImages = 200

bpp = 16

ScanSpeed = 5

CaptureSE = True

CaptureBSE = True

SEFileName = '%s, %dx%dx%d, %d bpp, little endian, SE.raw' % (SampleName, ImageWidth, ImageHeight, NumImages, bpp)

BSEFileName = '%s, %dx%dx%d, %d bpp, little endian, BSE.raw' % (SampleName, ImageWidth, ImageHeight, NumImages, bpp)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def ReadMessage(conn):

    # receive the message header

    msg_name = conn._RecvStrD(16)

    hdr = conn._RecvStrD(16)

    v = struct.unpack("<IIHHI", hdr)

    body_size = v[0]


    # get fn name

    cb_name = DecodeString(msg_name)
                  

    # receive the body

    cb_body = conn._RecvStrD(body_size)

        

    # finished reading message

    return (cb_name, cb_body)


def WriteImage(m):

    NumChannels = 0

    if CaptureSE == True:

        SEfile = open(SEFileName, "ab")

        NumChannels += 1

    if CaptureBSE == True:

        BSEfile = open(BSEFileName, "ab")

        NumChannels += 1

    #bio = BytesIO()



    #pdb.set_trace()

    bytes_read = 0

    bytesperpixel = bpp/8

    while bytes_read < ImageWidth*ImageHeight*bytesperpixel*NumChannels:
        (cb_name, cb_body) = ReadMessage(m.connection)
        
        v = struct.unpack("<IiIiI", cb_body[0:20])
        
        # Channel 0, write SE image.
        
        if v[1] == 0 and CaptureSE == True:

            SEfile.write(cb_body[20:])

            bytes_read = bytes_read + v[4]
            
            #bio.write(cb_body[20:])
            
        # Channel 1, write BSE image.

        if v[1] == 1 and CaptureBSE == True:

            BSEfile.write(cb_body[20:])

            bytes_read = bytes_read + v[4]

            #bio.write(cb_body[20:])
            
        # When we are done, close the files.

        if bytes_read >= ImageWidth*ImageHeight*bytesperpixel*NumChannels:        

            if CaptureSE == True:

                 SEfile.close()

            if CaptureBSE == True:

                 BSEfile.close()

        

        #time.sleep(1)



#        im = Image.frombuffer("L", bytes_read, bio, "raw", "L", 0, 1)

#        im.save(file_name + ".tif")



def func(x_0, y_0, x_max = 102, x_min = -2, y_max = 37, y_min = -65, delta = 1.8):
    """Aight, so you choose your starting position by inputting different x_0 and y_0 values. Default values will be used unless otherwise specified."""        
    #x_max, y_max be the top left corner, x_min, y_min be the lower right corner
    #The maxs and mins span a rectangular area--edges are ideally limitations of vacuum chamber
    #(x_0, y_0) must lie within this area and is the starting position of the beam.
    #the beam will move right from where it starts from
    #When it reaches the end, of the row (or x_0 = x_min) it will move down in y and back to x_0
    #delta is the spacing between points.
    
    if x_0 > x_max:
        
        return 'Error: input x must be smaller'
        
    elif x_0 < x_min:
        
        return 'Error: input x must be larger'
        
    elif y_0 > y_max:
        
        return 'Error: input y must be smaller'
        
    elif y_0 < y_min:
        
        return 'Error: input y must be larger'
    
    
    
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