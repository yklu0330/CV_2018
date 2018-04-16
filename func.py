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
        [7,8,1]
    ], dtype=np.float)

    #print(srcPoints[0][0][0])

    x = Symbol('0')
    y = Symbol('1')
    z = Symbol('2')
    a = Symbol('3')
    b = Symbol('4')
    c = Symbol('5')
    d = Symbol('6')
    e = Symbol('7')

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
        funcs[j*2] = srcPoints[j][0]*x + srcPoints[j][1]*y + z - srcPoints[j][0]*dstPoints[j][0]*d - dstPoints[j][0]*srcPoints[j][1]*e - dstPoints[j][0]
        funcs[j*2+1] = srcPoints[j][0]*a + srcPoints[j][1]*b + c - srcPoints[j][0]*dstPoints[j][1]*d - dstPoints[j][1]*srcPoints[j][1]*e - dstPoints[j][1]

    sol = solve(funcs, x, y, z, a, b, c, d, e)
    print(sol)

    H[0, 0] = sol[x].evalf()
    H[0, 1] = sol[y].evalf()
    H[0, 2] = sol[z].evalf()
    H[1, 0] = sol[a].evalf()
    H[1, 1] = sol[b].evalf()
    H[1, 2] = sol[c].evalf()
    H[2, 0] = sol[d].evalf()
    H[2, 1] = sol[e].evalf()

    return H


def findHomographyRANSAC(srcPoints, dstPoints):

    ITER_NUM = 10
    bestH = None
    bestErr = np.inf

    for x in range(ITER_NUM):
        maybe_idxs, test_idxs = random_partition(4, len(srcPoints))
        H = findHomography(srcPoints[maybe_idxs], dstPoints[maybe_idxs])
        testErr = np.mean(computeError(H, srcPoints[test_idxs], dstPoints[test_idxs]))
        if testErr < bestErr:
            bestH = H
            bestErr = testErr

    return bestH


def computeError(H, pt1, pt2):
    match_pt2 = pt2.T
    transformed_pt1 = H.dot(np.concatenate([pt1.T, np.ones([1, pt1.shape[0]])], axis=0))
    transformed_pt1 = (transformed_pt1 / transformed_pt1[2])[:2,]
    dists = np.linalg.norm((transformed_pt1 - match_pt2), axis=0).T
    return dists


def random_partition(k, pts_size):
    all_idxs = np.arange(pts_size)
    np.random.shuffle(all_idxs)
    idxs1 = all_idxs[:k]
    idxs2 = all_idxs[k:]
    return idxs1, idxs2


if __name__ == '__main__':
    srcPoints = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ])

    dstPints = np.array([
        [2, 1],
        [4, 1],
        [3, 2],
        [2, 2]
    ])

    print(findHomography(srcPoints, dstPints))
