import cv2
import numpy as np
from cyvlfeat.sift import sift
from glob import glob

def main():
    imgList = glob('./data/Rainier*.png')
    panoFileName = '../results/pano_Rainier.jpg'

    # Read Images
    Images = {}
    for idx, imgPath in enumerate(sorted(imgList)):
        img = cv2.imread(imgPath)
        Images.update({idx: img})
        print(idx, imgPath)
    print('Images loaded. Beginning feature detection...')


if __name__ == '__main__':
    main()