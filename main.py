import cv2
import numpy as np
import func
from SIFTMatcher import SIFTMatcher
from glob import glob

# Configs
THRESHOLD = 0.7

def main():
    imgList = glob('./data/yosemite*.jpg')
    panoFileName = './result/pano_yosemite.jpg'

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

        # H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        H = func.findHomographyRANSAC(src_pts.reshape(-1,2), dst_pts.reshape(-1,2))
        Transform.update({idx+1: H})

    # Stitch images
    pano = Images[0]
    prev_transfrom = np.identity(3, np.float)
    for idx in range(1, len(imgList)):
        H = prev_transfrom.dot(Transform[idx])

        # Find new corners
        srcImg = Images[idx]
        corners = np.array([
            [0, srcImg.shape[1], srcImg.shape[1], 0],
            [0, 0, srcImg.shape[0], srcImg.shape[0]],
            [1, 1, 1, 1]
        ])
        new_corners = H.dot(corners)
        new_corners = np.concatenate([(new_corners/new_corners[2])[:2,], ((0,pano.shape[1]),(0,pano.shape[0]))], axis=1)

        # Calculate translation matrix
        T = np.identity(3, np.float)
        T[0,2] = -new_corners[0].min()
        T[1,2] = -new_corners[1].min()

        # Calculate new image size
        new_size = (int(new_corners[0].max()-new_corners[0].min()), int(new_corners[1].max()-new_corners[1].min()))

        # Warp images
        warped = cv2.warpPerspective(Images[idx], T.dot(H), new_size)
        pano = cv2.warpPerspective(pano, T, new_size)

        # Blend image
        add_mask = np.sum(warped, axis=2) > np.sum(pano, axis=2)
        for c in range(pano.shape[2]):
            cur_im = pano[:,:,c]
            temp_im = warped[:,:,c]
            cur_im[add_mask] = temp_im[add_mask]
            pano[:,:,c] = cur_im


        prev_transfrom = T.dot(H)

        cv2.imshow('result{}_{}_pano'.format(idx, idx+1), pano)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imwrite(panoFileName, pano)


if __name__ == '__main__':
    main()