import cv2
import numpy as np
from cyvlfeat.sift import sift
from glob import glob

def main():
    imgList = glob('./data/Rainier*.png')

    # %% Feature detection
    Descriptor = {}
    PointInImg = {}

    for path in imgList:
        img = cv2.imread(path)


        # for idx, (key, img) in enumerate(sorted(Images.items())):
        #     I = np.asarray(img.convert('L')).astype('single')
        #     [f, d] = sift(I, compute_descriptor=True, float_descriptors=True)
        #     pointsInImage = swapcolumn(f[:, 0:2])
        #     PointInImg.update({idx: pointsInImage})
        #     Descriptor.update({idx: d})

        cv2.imshow(path, img)
        cv2.waitKey(0)


if __name__ == '__main__':
    main()