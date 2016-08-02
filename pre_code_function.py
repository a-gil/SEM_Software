# -*- coding: utf-8 -*-
from __future__ import print_function
print('Start')
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'remote'))
import time
import sem
import struct
from sem_v3_lib import *
import numpy as np
from scipy import misc


#Connect to the SEM SharkSEM interface.
m = sem.Sem()
conn = m.Connect('localhost', 8300)
print("Connection Established.")


#-------------------------------------------------------------------------------------------------------------------------------------------------------------


####important variables to change

#file name properties
SampleName = 'none'

#Image properties
ImageWidth = 512
ImageHeight = 512
bpp = 16

#SEM properties
ScanSpeed = 7
CaptureSE = True
CaptureBSE = False
z_min = 15
z_max = 40

#Initial values

#z_0 is measured manually. We first aim for an initial working distance WD_0 of 25 mm.
#For testing purposes, WD_0 is set for 30 mm
#We then move WD&z to this WD, and this gives us z_0 and WD_0
WD_0 = 30
z_0 = m.StgGetPosition()[2]


#args will hold the arguments for the functions. This is the format of the arguments:
#args = [x_0, y_0, x_max, x_min, y_max, y_min, delta]
#Typically should be used as the starting point of the scan
#but can also be used as a way to change parameters of calc_coords or FindWD
args = [-1, 36]


#-------------------------------------------------------------------------------------------------------------------------------------------------------------


#read SharkSEM message from data connection (callbacks)
def ReadMessage(conn):
    #receive the message header
    msg_name = conn._RecvStrD(16)
    hdr = conn._RecvStrD(16)
    v = struct.unpack("<IIHHI", hdr)
    body_size = v[0]

    #get fn name
    cb_name = DecodeString(msg_name)
                   
    #receive the body
    cb_body = conn._RecvStrD(body_size)

    #finished reading message
    return (cb_name, cb_body)


def WriteImage(m):
    NumChannels = 0

    if CaptureSE == True:
        SEfile = open(RawSEFileName, "ab")
        NumChannels += 1

    if CaptureBSE == True:
        BSEfile = open(RawBSEFileName, "ab")
        NumChannels += 1


    bytes_read = 0
    bytesperpixel = bpp/8
    

    while bytes_read < ImageWidth*ImageHeight*bytesperpixel*NumChannels:
        (cb_name, cb_body) = ReadMessage(m.connection)
        v = struct.unpack("<IiIiI", cb_body[0:20])

        #Channel 0, write SE image.
        if v[1] == 0 and CaptureSE == True:
            SEfile.write(cb_body[20:])
            bytes_read = bytes_read + v[4]

        #Channel 1, write BSE image.
        if v[1] == 1 and CaptureBSE == True:
            BSEfile.write(cb_body[20:])
            bytes_read = bytes_read + v[4]

        #When we are done, close the files.
        if bytes_read >= ImageWidth*ImageHeight*bytesperpixel*NumChannels:        
            if CaptureSE == True:
                 SEfile.close()

            if CaptureBSE == True:
                 BSEfile.close()

def TakeImgs(*args):
    global raw
    global tiff
    global RawSEFileName
    global RawBSEFileName
    
    if conn<0:
        print("Error: Unable to connect to SEM")
        return

    coords = FindWD(*args)
    
    print(coords)

    ViewField = m.GetViewField()*1000 # View field in microns.
    Voltage = m.HVGetVoltage()/1000 # Voltage in keV.
    
    k = 0
    while k < len(coords):
        (x, y, z) = coords[k]
        
        raw = '.raw'
        tiff = '.tiff'
        SEFileName = '(' + str(x) + ', ' + str(y) + ', ' + str(z) + ') ' + '%s, %d keV, %dx%dx, %g um wide, %d bpp, little endian, BSE' % (SampleName, Voltage, ImageWidth, ImageHeight, ViewField, bpp)
        BSEFileName = '(' + str(x) + ', ' + str(y) + ', ' + str(z) + ') ' + '%s, %d keV, %dx%dx, %g um wide, %d bpp, little endian, BSE' % (SampleName, Voltage, ImageWidth, ImageHeight, ViewField, bpp)
        RawSEFileName = SEFileName + raw
        RawBSEFileName = BSEFileName + raw
    
    
        # make sure scanning is inactive
        m.ScStopScan()
        m.ScSetSpeed(ScanSpeed)
    
        #Set Scan Mode to Depth
        m.SMSetMode(1)
        
        #move beam to that location
        m.StgMoveTo(x, y, z)
        time.sleep(5)
    
    
        #Take an image.
        print('Scanning image at' + '(' + str(x) + ', ' + str(y) + ', ' + str(z) + ') ' )
        res = m.ScScanXY(1, ImageWidth, ImageHeight, 0, 0, ImageWidth-1, ImageHeight-1, 1)
        time.sleep(1)
    
        #Let the image come in as it is acquired and then write it.
        WriteImage(m)
        
        #Convert the image into a .tiff file
        if CaptureSE == True:
            SEImage = np.fromfile(RawSEFileName, dtype=np.uint16)
            SEImage.shape = (ImageWidth, ImageHeight)
            misc.imsave(SEFileName + tiff, SEImage)
        
        if CaptureBSE == True:
            BSEImage = np.fromfile(RawBSEFileName, dtype=np.uint16)
            BSEImage.shape = (ImageWidth, ImageHeight)
            misc.imsave(BSEFileName + tiff, BSEImage)
        
        k = k + 1
        
    print("\n\n")
    time.sleep(1)
    print('Done')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

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
    
    
#The following makes a list of 2-element tuples
#and they will be used as the coordinates of the beam's location
    
    #dummy variable, might be removed if we make the sub while-->for    
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
        
        #break the loop when we reach the top left corner                 
        if y_m == y_max and x_n == x_min:
            break
    
    return coords



def FindWD(*args):
    """This function takes the coordinates calculated from calc_coords and feeds """\
    """them to the SEM. At each point, the working distance is calculated and used to find """\
    """the sample height"""
    """CAUTION: please make sure to alter the max and min values if a custom stage is being used."""


    #Assign SE to channel 0 and BSE to channel 1.
    m.DtSelect(0, 0)
    m.DtSelect(1, 1)

    #Enable each, 8 or 16 bits/pixel.
    if CaptureSE == True:
        m.DtEnable(0, 1, bpp)
    else:
        m.DtEnable(0, 0)
    if CaptureBSE == True:
        m.DtEnable(1, 1, bpp)
    else:
        m.DtEnable(1, 0)
        
    #switch scan mode to Resolution
    m.SMSetMode(0)

    #global coords
    coords = calc_coords(*args)
        
    #Now that we have the list, we can use it to assign the coordinates to the SEM    
    #define a certain magical index
    j = 0
    while j < len(coords):
        x, y = coords[j]
        
        #move SEM to that location
        m.StgMoveTo(x, y)
        time.sleep(3)
        
        #stop scanning to find WD
        m.ScStopScan()
        
        #Autofocus on that point        
        m.AutoWD(0)
        time.sleep(25)
        
        #save value of the autoWD into a variable to get sample height
        WD_n = m.GetWD()
        
        #Find sample height by using a bit of math.
        z_n = z_0 + (WD_0 - WD_n)
        print(z_n)
        
        #set limiting values for possible stage z-position to avoid collisions
        if z_n < z_min:
            print('z_n value dropped below safe zone and has been changed to border it at z_n = ')
            z_n = z_min
            print(z_n)
        if z_n > z_max:
            print('z_n value has gone too far from the WD and has been changed to border it at z_n = ')
            z_n = z_max
            print(z_n)
        
        
        #add z value to the list of coordinates calculated
        coords.remove(coords[j])
        coords.insert(j, (x, y, round(z_n, 1)))
        
        j = j+1
        
    return coords