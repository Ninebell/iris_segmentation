import os


def find_all_image_path(folder_path, extension):
    find_list = []
    list_dir = os.listdir(folder_path)
    for item in list_dir:
        if item.find('.') == -1:
            inner_list = find_all_image_path(os.path.join(folder_path, item), extension)
            find_list += inner_list
        elif item.find(extension) != -1:
            find_list.append(os.path.join(folder_path. item))

    return find_list
