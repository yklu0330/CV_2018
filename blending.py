import cv2
import numpy as np

def MultibandBlending(A, B, mask):

    # generate Mask pyramid
    pyM = [mask]
    for i in range(5):
        M = cv2.pyrDown(pyM[i])
        pyM.append(M)

    # generate Gaussian pyramid for A
    G = np.array(A.copy(), np.float64)
    gpA = [G]
    for i in range(6):
        G = cv2.pyrDown(G)
        gpA.append(G)

    # generate Gaussian pyramid for B
    G = np.array(B.copy(), np.float64)
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
    for i,(la,lb) in enumerate(zip(lpA,lpB)):
        ls = np.zeros(la.shape)
        for c in range(la.shape[2]):
            ls[:,:,c] = lb[:,:,c] * pyM[5-i] + la[:,:,c] * (1-pyM[5-i])
        LS.append(ls)

    # now reconstruct
    ls_ = LS[0]
    for i in range(1,6):
        ls_ = cv2.pyrUp(ls_)
        res = cv2.resize(ls_, (LS[i].shape[1], LS[i].shape[0]))
        ls_ = cv2.add(res, LS[i])

    return np.asarray(ls_, np.uint8)