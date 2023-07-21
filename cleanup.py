import os
import json

# remove unused slices

def remove_unused_images(image_path = os.getcwd(),
                         json_path = os.getcwd()):
    images = os.listdir(image_path)
    coco = json.load(open(json_path))
    coco_images = coco['images']
    used_images = []

    for image in coco_images:
        used_images.append(image['file_name'])

    # remove unused images
    for image in images:
        if not image.endswith('.JPG'):
            continue

        if image not in used_images:
            os.remove(os.path.join(image_path, image))
        else:
            used_images.pop(used_images.index(image))

remove_unused_images(image_path = './full_res_test_set/',
                     json_path = './full_res_test_set/coco_test_label.json')