


if __name__ == "__main__":

    r_max = setting_max_r()

    image_ paths = find_all_image_path()

    for image in image_paths:

        # image check
        if r_max * 2 >= image.shape[0] or r_max*2 >= image.shape[1]:
            print("radius is too big for processing radius: {0}, shape: {1}".format(r_max,image.shape))
            continue

        # resizing, mopology(erode)
        preprocess_image = preprocessing(image, r_max)

        # gaussian blur, crop, binary, local minima
        targeting_image = find_target_pixel(preprocess_image)

        # Process Daughman
        result = Daughman_Algorithm(image, targeting_image, r_max)

        image_show()

