



def findHomography(srcPoints, dstPoints):

    print('src points')
    print(srcPoints)
    print('dst points')
    print(dstPoints)

    # calculate homography

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