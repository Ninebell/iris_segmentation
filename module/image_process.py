import cv2
import numpy as np

def local_minima(image):
    height, width = image.shape

    r, c = 1, 1

    board = np.zeros((height, width), np.uint8)
    while r + 1 < height:
        c = 1
        while c + 1 < width:
            value = image[r, c]
            minimum = np.amin(image[r-1:r+1, c-1:c+1])
            if minimum != value:
                board[r, c] = 255
            c = c + 1
        r = r + 1

    result = image | board
    return result


def preprocessing(image):
    height, width = image.shape
    resize_image = cv2.resize(image, (width // 3 * 2, height // 3 * 2), cv2.INTER_CUBIC)

    kernel = np.ones((3,3), np.uint8)
    eroded = cv2.erode(resize_image, kernel)
    return eroded


def find_target_pixel(preprocess_image, max_r):
    crop_image = preprocess_image[max_r:-max_r, max_r:-max_r]

    _, binary_image = cv2.threshold(crop_image, 127.5, 255, cv2.INTER_CUBIC)

    crop_N_binary = crop_image | binary_image

    minima_image = local_minima(crop_N_binary)
    return minima_image


def conv_2d(image, x, y, mask):
    height, width = mask.shape
    masking_image = image[y-height//2: y+height//2, x-width//2: x+width//2] & mask
    count = np.count_nonzero(mask)

    return np.sum(masking_image)/count


def Daughman_Algorithm(image, preprocess, r_max):
    r_min = 15
    height, width = image.shape
    max_value, max_x, max_y, max_r = 0, 0, 0, 0
    daughman_values = np.zeros((height-r_max*2,width-r_max*2, r_max - r_min + 1), np.float)
    for r in range(r_min, r_max+1):
        print("process..... ", r)
        mask = np.zeros((r*2,r*2), np.uint8)
        mask = cv2.circle(mask,(r, r), r, (255), thickness=1)

        for y in range(r_max, height - r_max):
            for x in range(r_max, width - r_max):
                pre_loc_x = x-r_max
                pre_loc_y = y-r_max
                if preprocess[pre_loc_y, pre_loc_x] != 255:
                    daughman_values[pre_loc_y, pre_loc_x, r - r_min] = conv_2d(image, x, y, mask)
    diff_list = []
    for r in range(r_min, r_max-1):
        for y in range(r_max, height - r_max):
            for x in range(r_max, width - r_max):
                pre_loc_x = x-r_max
                pre_loc_y = y-r_max
                diff = daughman_values[pre_loc_y, pre_loc_x, r - r_min] - daughman_values[pre_loc_y, pre_loc_x, r - r_min + 1]
                if abs(diff) > max_value:
                    diff_list.append(abs(diff))
                    max_value = abs(diff)
                    max_x = x
                    max_y = y
                    max_r = r

    circle = cv2.circle(image, (max_x, max_y), max_r, 255, 1)
    max_value = 0
    pupil = (max_x, max_y, max_r)
    for r in range(max_r+10, r_max):
        diff = daughman_values[max_y - r_max, max_x - r_max, r -r_min] - daughman_values[max_y - r_max, max_x - r_max, r -r_min+1]
        if max_value < abs(diff):
            max_value = abs(diff)
            max_r = r

    circle_image = cv2.circle(circle, (max_x, max_y), max_r, 255, 1)
    iris = (max_x, max_y, max_r)
    return pupil, iris, circle_image
