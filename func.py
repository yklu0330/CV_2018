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



    f1 = None
    f2 = None
    f3 = None
    f4 = None
    f5 = None
    f6 = None
    f7 = None
    f0 = None

    belem = [0, 0, 0, 0, 0, 0, 0, 0]

    funcs = [f0, f1, f2, f3, f4, f5, f6, f7]
    for j in range(4):
        funcs[j * 2] = [srcPoints[j][0], srcPoints[j][1], 1, 0, 0, 0, -srcPoints[j][0] * dstPoints[j][0],
                       -dstPoints[j][0] * srcPoints[j][1]]
        belem[j * 2] = dstPoints[j][0]
        funcs[j * 2 + 1] = [ 0, 0, 0, srcPoints[j][0], srcPoints[j][1], 1, -srcPoints[j][0] * dstPoints[j][1]
                           , -dstPoints[j][1] * srcPoints[j][1]]
        belem[j * 2 + 1] = dstPoints[j][1]

    A = np.array([funcs[0], funcs[1], funcs[2], funcs[3], funcs[4], funcs[5], funcs[6], funcs[7]])  # 构造系数矩阵 A
    b = np.mat(belem).T  # 构造转置矩阵 b （这里必须为列向量）
    try:
        sol = np.linalg.solve(A, b)  # 调用 solve 函数求解
    except np.linalg.LinAlgError:
        return None
    print(sol)

    H[0, 0] = sol[0]
    H[0, 1] = sol[1]
    H[0, 2] = sol[2]
    H[1, 0] = sol[3]
    H[1, 1] = sol[4]
    H[1, 2] = sol[5]
    H[2, 0] = sol[6]
    H[2, 1] = sol[7]

    return H


def findHomographyRANSAC(srcPoints, dstPoints):

    ITER_NUM = 500
    bestH = None
    bestErr = np.inf

    for x in range(ITER_NUM):
        maybe_idxs, test_idxs = random_partition(4, len(srcPoints))
        H = findHomography(srcPoints[maybe_idxs], dstPoints[maybe_idxs])
        if H is None:
            continue
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
