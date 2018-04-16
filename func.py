import numpy as np
from sympy import *



def findHomography(srcPoints, dstPoints):

    print('src points')
    print(srcPoints)
    print('dst points')
    print(dstPoints)

    # calculate homography
    H = np.array([
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ])

    #print(srcPoints[0][0][0])

    x1 = Symbol('x')
    x2 = Symbol('y')
    x3 = Symbol('z')
    x4 = Symbol('a')
    x5 = Symbol('b')
    x6 = Symbol('c')
    x7 = Symbol('d')
    x8 = Symbol('e')


    f1 = None
    f2 = None
    f3 = None
    f4 = None
    f5 = None
    f6 = None
    f7 = None
    f0 = None

    funcs = [f0, f1, f2, f3, f4, f5, f6, f7]
    for j in range(4):
        for i in range(4):
            funcs[i*2] = srcPoints[j][0][0]*x1 + srcPoints[j][0][1] + z - srcPoints[j][0][0]*dstPoints[j][0][0]*d +


    return H


def findHomographyRANSAC(srcPoints, dstPoints):

    ITER_NUM = 500
    for x in range(ITER_NUM):
        random_idxs = [4, 6, 3, 19]
        four_src_points = srcPoints[random_idxs]
        four_dst_points = dstPoints[random_idxs]
        H = findHomography(four_src_points, four_dst_points)

        # calculate error

    return H