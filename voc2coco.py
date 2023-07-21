import os
import json
import xml.etree.ElementTree as ET

def category_name_to_id(categories, name):
    for category in categories:
        if category['name'] == name:
            return category['id']
    return -1

def voc2coco(ann_dir = os.getcwd(), img_dir = os.getcwd(), img_file_prefix = '', img_file_extension = '', output_filename = 'coco.json', categories = []):
    # List the xml label files
    annotations = []
    images = []

    bad_xml = 0
    no_image = 0
    no_error = 0

    ann_dir_files = os.listdir(ann_dir)
    for file in ann_dir_files:
        if file.endswith('.xml'):
            annotations.append(file)
    
    img_dir_files = os.listdir(img_dir)
    for file in img_dir_files:
        if file.endswith(img_file_extension):
            images.append(file)

    # Create the coco annotation
    c_images = []
    c_annotations = []
    curr_img_id = 0
    curr_ann_id = 0

    for ann in annotations:
        tree = ET.parse(os.path.join(ann_dir, ann))
        root = tree.getroot()

        # skip if annotation file is invalid
        if len(root) < 1:
            print(f'Annotation file "{ann}" invalid.')
            bad_xml += 1
            continue

        file_name = img_file_prefix + root.find('filename').text + img_file_extension

        # skip if image does not exist in the directory
        if not file_name in images:
            print(f'Skipping image "{file_name}" as it does not exist in img directory.')
            no_image += 1
            continue

        curr_img_id += 1

        # for images array
        temp_images = {
            'file_name': file_name,
            'height': int(root.find('size').find('height').text),
            'width': int(root.find('size').find('width').text),
            'id': int(curr_img_id)
        }

        c_images.append(temp_images)
        
        # for annotations array
        for object in tree.findall('object'):
            curr_ann_id += 1
            obj_name = object.find('name').text
            min_x = int(object.find('bndbox').find('xmin').text)
            min_y = int(object.find('bndbox').find('ymin').text)
            max_x = int(object.find('bndbox').find('xmax').text)
            max_y = int(object.find('bndbox').find('ymax').text)

            height = max_y - min_y
            width = max_x - min_x

            area = height * width
            bbox = [min_x, min_y, width, height]

            category_id = category_name_to_id(categories, obj_name)
            if category_id == -1:
                print(f'Skipping an annotation, not valid category "{obj_name}".')
                continue

            temp_annotation = {
                'area': area,
                'iscrowd': 0,
                'bbox': bbox,
                'category_id': category_id,
                'ignore': 0,
                'image_id': curr_img_id,
                'id': curr_ann_id
            }
            c_annotations.append(temp_annotation)
        
        no_error += 1
    
    # create the coco json
    coco = {
        'images': c_images,
        'annotations': c_annotations,
        'categories': categories
    }

    # Serializing json
    json_object = json.dumps(coco, indent=4)
    
    # Writing to sample.json
    with open(output_filename, "w") as outfile:
        outfile.write(json_object)
    
    print(f'Process completed with {bad_xml} bad xml files, {no_image} missing images, and {no_error} no errors. {bad_xml + no_image + no_error} files processed total.')

voc2coco(ann_dir = './trainImages/labels',
         img_dir = './trainImages',
         img_file_prefix = 'train_',
         img_file_extension = '.JPG',
         output_filename = './trainImages/coco_train_label.json',
         categories = [{"supercategory": "none", "id": 0, "name": "human"}])

voc2coco(ann_dir = './testImages/labels',
         img_dir = './testImages',
         img_file_prefix = 'test_',
         img_file_extension = '.JPG',
         output_filename = './testImages/coco_test_label.json',
         categories = [{"supercategory": "none", "id": 0, "name": "human"}])