from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy import misc

stuff = np.fromfile('test.raw', dtype=uint16)
stuff.shape = (512, 512)
plt.imshow(stuff, cmap='gray')

misc.imsave('test.tiff', stuff)