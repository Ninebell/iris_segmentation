#open library

#custom library
from module.parameter import *
from module.file_io import *
from module.image_process import *

if __name__ == "__main__":
    parameter = make_parser()
    r_max = get_radius(parameter)
    folder_path = get_path(parameter)
    extension = get_extension(parameter)
    image_paths = find_all_image_path(folder_path, extension)

    for image_path in image_paths:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # image check
        if r_max * 2 >= image.shape[0] or r_max*2 >= image.shape[1]:
            print("radius is too big for processing radius: {0}, shape: {1}".format(r_max,image.shape))
            continue

        # resizing, mopology(erode)
        preprocess_image = preprocessing(image)

        # gaussian blur, crop, binary, local minima
        targeting_image = find_target_pixel(preprocess_image, r_max)

        # Process Daughman
        pupil, iris, circle = Daughman_Algorithm(preprocess_image, targeting_image, r_max)
        print("pupil: ", pupil, " iris: ", iris)
        print("if you want stop, press esc")
        cv2.imshow("circle", circle)
        key = cv2.waitKey()
        if key == 27:
            break