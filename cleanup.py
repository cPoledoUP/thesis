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
        if not (image.endswith('.JPG') or image.endswith('.jpg')):
            continue

        if image not in used_images:
            os.remove(os.path.join(image_path, image))
        else:
            used_images.pop(used_images.index(image))
    
    for annotation in coco['annotations']:
        if 'segmentation' in annotation:
            annotation.pop('segmentation')
    
    # Serializing json
    json_object = json.dumps(coco, indent=4)
    
    # Writing to sample.json
    with open(json_path, "w") as outfile:
        outfile.write(json_object)

remove_unused_images(image_path = './datasets/320_12/coco_train_label_images_320_012',
                     json_path = './datasets/320_12/coco_train_label_320_012.json')