import cv2
import numpy as np

def MultibandBlending(A, B):

    # generate Gaussian pyramid for A
    G = A.copy()
    gpA = [G]
    for i in range(6):
        G = cv2.pyrDown(G)
        gpA.append(G)

    # generate Gaussian pyramid for B
    G = B.copy()
    gpB = [G]
    for i in range(6):
        G = cv2.pyrDown(G)
        gpB.append(G)

    # generate Laplacian Pyramid for A
    lpA = [gpA[5]]
    for i in range(5,0,-1):
        GE = cv2.pyrUp(gpA[i])
        res = cv2.resize(GE, (gpA[i-1].shape[1], gpA[i-1].shape[0]))
        L = cv2.subtract(gpA[i-1], res)
        lpA.append(L)

    # generate Laplacian Pyramid for B
    lpB = [gpB[5]]
    for i in range(5,0,-1):
        GE = cv2.pyrUp(gpB[i])
        res = cv2.resize(GE, (gpB[i - 1].shape[1], gpB[i - 1].shape[0]))
        L = cv2.subtract(gpB[i-1], res)
        lpB.append(L)

    # Now add left and right halves of images in each level
    LS = []
    for la,lb in zip(lpA,lpB):
        rows,cols,dpt = la.shape
        ls = np.hstack((la[:,0:int(cols/2)], lb[:,int(cols/2):]))
        LS.append(ls)

    # now reconstruct
    ls_ = LS[0]
    for i in range(1,6):
        ls_ = cv2.pyrUp(ls_)
        res = cv2.resize(ls_, (LS[i].shape[1], LS[i].shape[0]))
        ls_ = cv2.add(res, LS[i])

    return ls_