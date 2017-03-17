import numpy as np
from PIL import ImageOps, Image
from separateTVAndL1 import *
import sys
import scipy.misc as misc
import os.path as path

def main(filepath, outpath):
    print(filepath)
    try:
        im_raw = Image.open(filepath)
    except:
        print("Cannot Open File")
        return
    
    if im_raw == None:
        print("Cannot Open File")
        return

    gray_img = ImageOps.grayscale(im_raw)
    gray_img = np.array(gray_img)
    gray_img = gray_img / 255.0
    
    shadeless = removeShade(gray_img, 100)

    shadeless[shadeless>1.0] = 1.0
    shadeless[shadeless<0] = 0

    misc.imsave(outpath, shadeless);

if __name__ == "__main__":
    argvs = sys.argv
    print(argvs[1])
    argc = len(argvs)

    if argc <= 1:
        print("Usage: python3 shaderemover.py inputfilename outputfilename")
    elif argc == 2:
        main(argvs[1], path.splitext(argvs[1])[0]+"_sl"+path.splitext(argvs[1])[1])
    else:
        main(argvs[1], argv[2])
