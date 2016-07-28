#!/usr/bin/env python
#
# Autocrops the specified image.
#
# Based on code snippet from the following page:
# http://stackoverflow.com/questions/7528816/trim-scanned-images-with-pil

import os
import sys
import datetime
import tempfile
import numpy as np
from PIL import Image

#these values set how sensitive the bounding box detection is
threshold = 200     #the average of the darkest values must be _below_ this to count (0 is darkest, 255 is lightest) - default 200
obviousness = 150   #how many of the darkest pixels to include (1 would mean a single dark pixel triggers it) - default 50

def find_line(vals):
    #implement edge detection once, use many times 
    for i,tmp in enumerate(vals):
        tmp.sort()
        average = float(sum(tmp[:obviousness]))/len(tmp[:obviousness])
        if average <= threshold:
            return i
    return i    #i is left over from failed threshold finding, it is the bounds

def getbox(img):
    #get the bounding box of the interesting part of a PIL image object
    #this is done by getting the darekest of the R, G or B value of each pixel
    #and finding were the edge gest dark/colored enough
    #returns a tuple of (left,upper,right,lower)

    width, height = img.size    #for making a 2d array
    retval = [0,0,width,height] #values will be disposed of, but this is a black image's box 

    pixels = list(img.getdata())
    vals = []                   #store the value of the darkest color
    for pixel in pixels:
        vals.append(min(pixel)) #the darkest of the R,G or B values

    #make 2d array
    vals = np.array([vals[i * width:(i + 1) * width] for i in xrange(height)])

    #start with upper bounds
    forupper = vals.copy()
    retval[1] = find_line(forupper)

    #next, do lower bounds
    forlower = vals.copy()
    forlower = np.flipud(forlower)
    retval[3] = height - find_line(forlower)

    #left edge, same as before but roatate the data so left edge is top edge
    forleft = vals.copy()
    forleft = np.swapaxes(forleft,0,1)
    retval[0] = find_line(forleft)

    #and right edge is bottom edge of rotated array
    forright = vals.copy()
    forright = np.swapaxes(forright,0,1)
    forright = np.flipud(forright)
    retval[2] = width - find_line(forright)

    if retval[0] >= retval[2] or retval[1] >= retval[3]:
        print "error, bounding box is not legit"
        return None
    return tuple(retval)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s <input-image-file> [output-image-file]' % sys.argv[0]
        sys.exit(1)
    if len(sys.argv) == 3:
        outfilename = sys.argv[2]
    else:
        outfilename = sys.argv[1]
    # Auto crop the image
    image = Image.open(sys.argv[1])
    box = getbox(image)
    print "result is: ",box
    result = image.crop(box)
    # result.show()
    if outfilename == sys.argv[1]:
        os.unlink(outfilename)
    result.save(outfilename)
    print outfilename