import numpy as np
from scipy import misc

stuff = np.fromfile('check.raw', dtype=np.uint16)
stuff.shape = (512, 512)
#plt.imshow(stuff, cmap='gray')

misc.imsave('check.tiff', stuff)