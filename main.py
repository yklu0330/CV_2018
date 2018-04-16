import cv2
import numpy as np
import func
from SIFTMatcher import SIFTMatcher
from glob import glob

# Configs
THRESHOLD = 0.7

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

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # Extract SIFT features
    Descriptor = {}
    PointInImg = {}
    for idx, (key, img) in enumerate(sorted(Images.items())):
        I = np.asarray(img)
        f, d = sift.detectAndCompute(I, None)
        PointInImg.update({idx: f})
        Descriptor.update({idx: d})

    # Compute Transformation
    Transform = {}
    for idx in range(len(imgList) - 1):
        print('fitting transformation from ' + str(idx) + ' to ' + str(idx + 1) + '\t')
        M = SIFTMatcher(Descriptor[idx], Descriptor[idx + 1], THRESHOLD)
        print('matching points:', len(M, ), '\n')

        dst_pts = np.float32([PointInImg[idx][m[0]].pt for m in M]).reshape(-1, 1, 2)
        src_pts = np.float32([PointInImg[idx+1][m[1]].pt for m in M]).reshape(-1, 1, 2)

        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        # H = func.findHomographyRANSAC(src_pts, dst_pts)
        wrap = cv2.warpPerspective(Images[idx+1], H, (Images[idx+1].shape[1]+Images[idx+1].shape[1] , Images[idx+1].shape[0]+Images[idx+1].shape[0]))
        # result = cv2.addWeighted(img1, 0.5, wrap, 0.5, 0)
        wrap[0:Images[idx+1].shape[0], 0:Images[idx+1].shape[1]] = Images[idx]

        # rows, cols = np.where(wrap[:,:,0] !=0)
        # min_row, max_row = min(rows), max(rows) +1
        # min_col, max_col = min(cols), max(cols) +1
        # result = wrap[min_row:max_row,min_col:max_col,:] # Remove extra blank space
        result = wrap
        cv2.imshow('result{}_{}'.format(idx, idx+1),result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



if __name__ == '__main__':
    main()