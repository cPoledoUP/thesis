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

voc2coco(ann_dir = '../heridal/trainImages/labels',
         img_dir = '../heridal/trainImages',
         img_file_prefix = 'train_',
         img_file_extension = '.JPG',
         output_filename = '../heridal/trainImages/coco_train_label.json',
         categories = [{"supercategory": "none", "id": 0, "name": "human"}])

voc2coco(ann_dir = '../heridal/testImages/labels',
         img_dir = '../heridal/testImages',
         img_file_prefix = 'test_',
         img_file_extension = '.JPG',
         output_filename = '../heridal/testImages/coco_test_label.json',
         categories = [{"supercategory": "none", "id": 0, "name": "human"}])

""" Result from converting heridal xml annotations to coco
Annotation file "train_BRA_1003.xml" invalid.
Annotation file "train_BRA_1004.xml" invalid.
Annotation file "train_BRA_1005.xml" invalid.
Annotation file "train_BRA_1006.xml" invalid.
Annotation file "train_BRA_1007.xml" invalid.
Annotation file "train_BRA_1008.xml" invalid.
Annotation file "train_BRA_1009.xml" invalid.
Annotation file "train_BRA_1010.xml" invalid.
Annotation file "train_BRA_1022.xml" invalid.
Annotation file "train_BRA_1030.xml" invalid.
Annotation file "train_BRA_1034.xml" invalid.
Annotation file "train_BRA_1035.xml" invalid.
Annotation file "train_BRA_1036.xml" invalid.
Annotation file "train_BRA_1041.xml" invalid.
Annotation file "train_BRA_1042.xml" invalid.
Annotation file "train_BRA_1043.xml" invalid.
Annotation file "train_BRA_1044.xml" invalid.
Annotation file "train_BRA_1045.xml" invalid.
Annotation file "train_BRA_1046.xml" invalid.
Annotation file "train_BRA_1047.xml" invalid.
Annotation file "train_BRA_1048.xml" invalid.
Annotation file "train_BRA_1049.xml" invalid.
Annotation file "train_BRA_1050.xml" invalid.
Annotation file "train_BRA_1051.xml" invalid.
Annotation file "train_BRA_1057.xml" invalid.
Annotation file "train_BRA_1058.xml" invalid.
Annotation file "train_BRA_1059.xml" invalid.
Annotation file "train_BRA_1062.xml" invalid.
Annotation file "train_BRA_1072.xml" invalid.
Annotation file "train_BRK_2021.xml" invalid.
Annotation file "train_BRK_2022.xml" invalid.
Annotation file "train_BRK_2023.xml" invalid.
Annotation file "train_BRK_2024.xml" invalid.
Annotation file "train_BRK_2025.xml" invalid.
Annotation file "train_BRK_2026.xml" invalid.
Annotation file "train_BRK_2027.xml" invalid.
Annotation file "train_BRK_2029.xml" invalid.
Annotation file "train_BRK_2030.xml" invalid.
Annotation file "train_BRK_2031.xml" invalid.
Annotation file "train_BRK_2032.xml" invalid.
Annotation file "train_BRK_2033.xml" invalid.
Annotation file "train_BRK_2034.xml" invalid.
Annotation file "train_BRK_2078.xml" invalid.
Annotation file "train_BRK_2079.xml" invalid.
Annotation file "train_BRK_2080.xml" invalid.
Annotation file "train_BRK_2081.xml" invalid.
Annotation file "train_BRK_2082.xml" invalid.
Annotation file "train_BRK_2083.xml" invalid.
Annotation file "train_BRK_2084.xml" invalid.
Annotation file "train_BRK_2090.xml" invalid.
Annotation file "train_BRK_2102.xml" invalid.
Annotation file "train_BRK_2126.xml" invalid.
Annotation file "train_BRK_2127.xml" invalid.
Annotation file "train_BRK_2128.xml" invalid.
Annotation file "train_BRK_2129.xml" invalid.
Annotation file "train_BRK_2130.xml" invalid.
Annotation file "train_BRK_2131.xml" invalid.
Annotation file "train_BRK_2132.xml" invalid.
Annotation file "train_BRK_2133.xml" invalid.
Annotation file "train_BRK_2134.xml" invalid.
Annotation file "train_BRK_2135.xml" invalid.
Annotation file "train_BRK_2136.xml" invalid.
Annotation file "train_BRK_2137.xml" invalid.
Annotation file "train_BRK_2138.xml" invalid.
Annotation file "train_BRK_2139.xml" invalid.
Annotation file "train_BRK_2140.xml" invalid.
Annotation file "train_BRS_0002.xml" invalid.
Annotation file "train_BRS_0012.xml" invalid.
Annotation file "train_BRS_0014.xml" invalid.
Annotation file "train_BRS_0020.xml" invalid.
Annotation file "train_BRS_0021.xml" invalid.
Annotation file "train_BRS_0022.xml" invalid.
Annotation file "train_BRS_0026.xml" invalid.
Annotation file "train_BRS_0027.xml" invalid.
Annotation file "train_BRS_0028.xml" invalid.
Annotation file "train_BRS_0029.xml" invalid.
Annotation file "train_BRS_0030.xml" invalid.
Annotation file "train_BRS_0031.xml" invalid.
Annotation file "train_BRS_0042.xml" invalid.
Annotation file "train_BRS_0043.xml" invalid.
Annotation file "train_BRS_0044.xml" invalid.
Annotation file "train_BRS_0045.xml" invalid.
Annotation file "train_BRS_0046.xml" invalid.
Annotation file "train_BRS_0047.xml" invalid.
Annotation file "train_CAP_0007.xml" invalid.
Annotation file "train_CAP_0008.xml" invalid.
Annotation file "train_CAP_0009.xml" invalid.
Annotation file "train_CAP_0010.xml" invalid.
Annotation file "train_CAP_0011.xml" invalid.
Annotation file "train_CAP_0014.xml" invalid.
Annotation file "train_CAP_0015.xml" invalid.
Annotation file "train_CAP_0016.xml" invalid.
Annotation file "train_CAP_0017.xml" invalid.
Annotation file "train_CAP_0018.xml" invalid.
Annotation file "train_CAP_0019.xml" invalid.
Annotation file "train_CAP_0020.xml" invalid.
Annotation file "train_CAP_0021.xml" invalid.
Annotation file "train_CAP_0022.xml" invalid.
Annotation file "train_CAP_0023.xml" invalid.
Annotation file "train_CAP_0024.xml" invalid.
Annotation file "train_CAP_0025.xml" invalid.
Annotation file "train_CAP_0026.xml" invalid.
Annotation file "train_CAP_0027.xml" invalid.
Annotation file "train_CAP_0028.xml" invalid.
Annotation file "train_CAP_0029.xml" invalid.
Annotation file "train_CAP_0030.xml" invalid.
Annotation file "train_CAP_0031.xml" invalid.
Annotation file "train_CAP_0032.xml" invalid.
Annotation file "train_CAP_0033.xml" invalid.
Annotation file "train_CAP_0034.xml" invalid.
Annotation file "train_CAP_0035.xml" invalid.
Annotation file "train_CAP_0036.xml" invalid.
Annotation file "train_CAP_0037.xml" invalid.
Annotation file "train_CAP_0038.xml" invalid.
Annotation file "train_CAP_0039.xml" invalid.
Annotation file "train_CAP_0040.xml" invalid.
Annotation file "train_CAP_0041.xml" invalid.
Annotation file "train_CAP_0042.xml" invalid.
Annotation file "train_CAP_0043.xml" invalid.
Annotation file "train_CAP_0044.xml" invalid.
Annotation file "train_CAP_0045.xml" invalid.
Annotation file "train_CAP_0046.xml" invalid.
Annotation file "train_CAP_0049.xml" invalid.
Annotation file "train_CAP_0050.xml" invalid.
Annotation file "train_CAP_0051.xml" invalid.
Annotation file "train_CAP_0052.xml" invalid.
Annotation file "train_CAP_0055.xml" invalid.
Annotation file "train_CAP_0056.xml" invalid.
Annotation file "train_CAP_0057.xml" invalid.
Annotation file "train_GOR_1001.xml" invalid.
Annotation file "train_GOR_1002.xml" invalid.
Annotation file "train_GOR_1003.xml" invalid.
Annotation file "train_GOR_1004.xml" invalid.
Annotation file "train_GOR_1005.xml" invalid.
Annotation file "train_GOR_1006.xml" invalid.
Annotation file "train_GOR_1010.xml" invalid.
Annotation file "train_GOR_1011.xml" invalid.
Annotation file "train_GOR_1012.xml" invalid.
Annotation file "train_GOR_1013.xml" invalid.
Annotation file "train_GOR_1014.xml" invalid.
Annotation file "train_GOR_1015.xml" invalid.
Annotation file "train_GOR_1016.xml" invalid.
Annotation file "train_GOR_1017.xml" invalid.
Annotation file "train_GOR_1018.xml" invalid.
Annotation file "train_GOR_1019.xml" invalid.
Annotation file "train_GOR_1020.xml" invalid.
Annotation file "train_GOR_1021.xml" invalid.
Annotation file "train_GOR_1022.xml" invalid.
Annotation file "train_GOR_1023.xml" invalid.
Annotation file "train_GOR_1024.xml" invalid.
Annotation file "train_GOR_1025.xml" invalid.
Annotation file "train_GOR_1026.xml" invalid.
Annotation file "train_GOR_1027.xml" invalid.
Annotation file "train_GOR_1028.xml" invalid.
Annotation file "train_GOR_1029.xml" invalid.
Annotation file "train_GOR_1030.xml" invalid.
Annotation file "train_GOR_1031.xml" invalid.
Annotation file "train_GOR_1032.xml" invalid.
Annotation file "train_GOR_1033.xml" invalid.
Annotation file "train_GOR_1034.xml" invalid.
Annotation file "train_GOR_1035.xml" invalid.
Annotation file "train_GOR_1036.xml" invalid.
Annotation file "train_GOR_1037.xml" invalid.
Annotation file "train_GOR_1045.xml" invalid.
Annotation file "train_GOR_1046.xml" invalid.
Annotation file "train_GOR_1047.xml" invalid.
Annotation file "train_GOR_1048.xml" invalid.
Annotation file "train_GOR_1049.xml" invalid.
Annotation file "train_GOR_1061.xml" invalid.
Annotation file "train_GOR_1062.xml" invalid.
Annotation file "train_GOR_1063.xml" invalid.
Annotation file "train_GOR_2010.xml" invalid.
Annotation file "train_GOR_2011.xml" invalid.
Annotation file "train_GOR_2015.xml" invalid.
Annotation file "train_GOR_2016.xml" invalid.
Annotation file "train_GOR_2017.xml" invalid.
Annotation file "train_GOR_2018.xml" invalid.
Annotation file "train_GOR_2019.xml" invalid.
Annotation file "train_GOR_2020.xml" invalid.
Annotation file "train_GOR_2021.xml" invalid.
Annotation file "train_GOR_2022.xml" invalid.
Annotation file "train_GOR_2023.xml" invalid.
Annotation file "train_GOR_2024.xml" invalid.
Annotation file "train_GOR_2025.xml" invalid.
Annotation file "train_GOR_2026.xml" invalid.
Annotation file "train_GOR_2027.xml" invalid.
Annotation file "train_GOR_2028.xml" invalid.
Annotation file "train_GOR_2030.xml" invalid.
Annotation file "train_GOR_2031.xml" invalid.
Annotation file "train_GOR_2032.xml" invalid.
Annotation file "train_GOR_2033.xml" invalid.
Annotation file "train_GOR_2034.xml" invalid.
Annotation file "train_GOR_2035.xml" invalid.
Annotation file "train_GOR_2036.xml" invalid.
Annotation file "train_GOR_2046.xml" invalid.
Annotation file "train_GOR_2047.xml" invalid.
Annotation file "train_GOR_2048.xml" invalid.
Annotation file "train_GOR_2049.xml" invalid.
Annotation file "train_GOR_2050.xml" invalid.
Annotation file "train_GOR_2051.xml" invalid.
Annotation file "train_GOR_2052.xml" invalid.
Annotation file "train_GOR_2054.xml" invalid.
Annotation file "train_GOR_2060.xml" invalid.
Annotation file "train_GOR_3047.xml" invalid.
Annotation file "train_GOR_3048.xml" invalid.
Annotation file "train_GOR_3051.xml" invalid.
Annotation file "train_GOR_3052.xml" invalid.
Annotation file "train_GOR_3073.xml" invalid.
Annotation file "train_GOR_3074.xml" invalid.
Annotation file "train_GOR_3075.xml" invalid.
Annotation file "train_GOR_3076.xml" invalid.
Annotation file "train_JAS_0001.xml" invalid.
Annotation file "train_JAS_0002.xml" invalid.
Annotation file "train_JAS_0003.xml" invalid.
Annotation file "train_JAS_0004.xml" invalid.
Annotation file "train_JAS_0005.xml" invalid.
Annotation file "train_JAS_0009.xml" invalid.
Annotation file "train_JAS_0010.xml" invalid.
Annotation file "train_JAS_0011.xml" invalid.
Annotation file "train_JAS_0012.xml" invalid.
Annotation file "train_JAS_0013.xml" invalid.
Annotation file "train_JAS_0014.xml" invalid.
Annotation file "train_JAS_0015.xml" invalid.
Annotation file "train_JAS_0016.xml" invalid.
Annotation file "train_JAS_0017.xml" invalid.
Annotation file "train_JAS_0018.xml" invalid.
Annotation file "train_JAS_0019.xml" invalid.
Annotation file "train_JAS_0020.xml" invalid.
Annotation file "train_JAS_0021.xml" invalid.
Annotation file "train_JAS_0022.xml" invalid.
Annotation file "train_JAS_0023.xml" invalid.
Annotation file "train_JAS_0024.xml" invalid.
Annotation file "train_JAS_0025.xml" invalid.
Annotation file "train_JAS_0026.xml" invalid.
Annotation file "train_JAS_0027.xml" invalid.
Annotation file "train_JAS_0028.xml" invalid.
Annotation file "train_JAS_0029.xml" invalid.
Annotation file "train_JAS_0030.xml" invalid.
Annotation file "train_JAS_0031.xml" invalid.
Annotation file "train_JAS_0032.xml" invalid.
Annotation file "train_JAS_0033.xml" invalid.
Annotation file "train_JAS_0034.xml" invalid.
Annotation file "train_JAS_0035.xml" invalid.
Annotation file "train_JAS_0036.xml" invalid.
Annotation file "train_JAS_0037.xml" invalid.
Annotation file "train_JAS_0038.xml" invalid.
Annotation file "train_JAS_0039.xml" invalid.
Annotation file "train_JAS_0040.xml" invalid.
Annotation file "train_JAS_0041.xml" invalid.
Annotation file "train_JAS_0042.xml" invalid.
Annotation file "train_JAS_0043.xml" invalid.
Annotation file "train_JAS_0044.xml" invalid.
Annotation file "train_JAS_0045.xml" invalid.
Annotation file "train_JAS_0046.xml" invalid.
Annotation file "train_JAS_0047.xml" invalid.
Annotation file "train_JAS_0048.xml" invalid.
Annotation file "train_JAS_0049.xml" invalid.
Annotation file "train_JAS_0050.xml" invalid.
Annotation file "train_JAS_0051.xml" invalid.
Annotation file "train_JAS_0052.xml" invalid.
Annotation file "train_JAS_0053.xml" invalid.
Annotation file "train_JAS_0054.xml" invalid.
Annotation file "train_JAS_0055.xml" invalid.
Annotation file "train_JAS_0056.xml" invalid.
Annotation file "train_JAS_0058.xml" invalid.
Annotation file "train_JAS_0059.xml" invalid.
Annotation file "train_JAS_0060.xml" invalid.
Annotation file "train_JAS_0061.xml" invalid.
Annotation file "train_JAS_0062.xml" invalid.
Annotation file "train_JAS_0071.xml" invalid.
Annotation file "train_JAS_0072.xml" invalid.
Annotation file "train_JAS_0088.xml" invalid.
Annotation file "train_JAS_0096.xml" invalid.
Annotation file "train_JAS_0097.xml" invalid.
Annotation file "train_JAS_0098.xml" invalid.
Annotation file "train_JAS_0099.xml" invalid.
Annotation file "train_JAS_0100.xml" invalid.
Annotation file "train_JAS_0101.xml" invalid.
Annotation file "train_JAS_0102.xml" invalid.
Annotation file "train_JAS_0103.xml" invalid.
Annotation file "train_JAS_0104.xml" invalid.
Annotation file "train_JAS_0105.xml" invalid.
Annotation file "train_JAS_0111.xml" invalid.
Annotation file "train_JAS_0115.xml" invalid.
Annotation file "train_JAS_0116.xml" invalid.
Annotation file "train_JAS_0117.xml" invalid.
Annotation file "train_JAS_0118.xml" invalid.
Annotation file "train_JAS_0119.xml" invalid.
Annotation file "train_JAS_0120.xml" invalid.
Annotation file "train_JAS_0121.xml" invalid.
Annotation file "train_JAS_0122.xml" invalid.
Annotation file "train_JAS_0123.xml" invalid.
Annotation file "train_JAS_0124.xml" invalid.
Annotation file "train_JAS_0125.xml" invalid.
Annotation file "train_JAS_0137.xml" invalid.
Annotation file "train_JAS_0138.xml" invalid.
Annotation file "train_JAS_0139.xml" invalid.
Annotation file "train_JAS_0140.xml" invalid.
Annotation file "train_JAS_0141.xml" invalid.
Annotation file "train_JAS_0142.xml" invalid.
Annotation file "train_JAS_0143.xml" invalid.
Annotation file "train_JAS_0155.xml" invalid.
Annotation file "train_JAS_0156.xml" invalid.
Annotation file "train_JAS_0162.xml" invalid.
Annotation file "train_JAS_0163.xml" invalid.
Annotation file "train_JAS_0164.xml" invalid.
Annotation file "train_JAS_0172.xml" invalid.
Annotation file "train_JAS_0173.xml" invalid.
Annotation file "train_JAS_0182.xml" invalid.
Annotation file "train_JAS_0183.xml" invalid.
Annotation file "train_JAS_0184.xml" invalid.
Annotation file "train_JAS_0185.xml" invalid.
Annotation file "train_JAS_0186.xml" invalid.
Annotation file "train_MED_3024.xml" invalid.
Annotation file "train_MED_3025.xml" invalid.
Annotation file "train_MED_3026.xml" invalid.
Annotation file "train_MED_3032.xml" invalid.
Annotation file "train_MED_3049.xml" invalid.
Annotation file "train_MED_3050.xml" invalid.
Annotation file "train_MED_3052.xml" invalid.
Annotation file "train_MED_3053.xml" invalid.
Annotation file "train_MED_3054.xml" invalid.
Annotation file "train_MED_3055.xml" invalid.
Annotation file "train_MED_3056.xml" invalid.
Annotation file "train_MED_3057.xml" invalid.
Annotation file "train_MED_3061.xml" invalid.
Annotation file "train_MED_4001.xml" invalid.
Annotation file "train_MED_4002.xml" invalid.
Annotation file "train_MED_4003.xml" invalid.
Annotation file "train_MED_4004.xml" invalid.
Annotation file "train_MED_4005.xml" invalid.
Annotation file "train_MED_4006.xml" invalid.
Annotation file "train_MED_4007.xml" invalid.
Annotation file "train_MED_4008.xml" invalid.
Annotation file "train_MED_4018.xml" invalid.
Annotation file "train_MED_4019.xml" invalid.
Annotation file "train_MED_4020.xml" invalid.
Annotation file "train_MED_4021.xml" invalid.
Annotation file "train_MED_4022.xml" invalid.
Annotation file "train_MED_4023.xml" invalid.
Annotation file "train_MED_4024.xml" invalid.
Annotation file "train_MED_4025.xml" invalid.
Annotation file "train_MED_4029.xml" invalid.
Annotation file "train_MED_4036.xml" invalid.
Annotation file "train_MED_4037.xml" invalid.
Annotation file "train_MED_4038.xml" invalid.
Annotation file "train_MED_4039.xml" invalid.
Annotation file "train_MED_4040.xml" invalid.
Annotation file "train_MED_4041.xml" invalid.
Annotation file "train_MED_4042.xml" invalid.
Annotation file "train_MED_4048.xml" invalid.
Annotation file "train_RAK_0004.xml" invalid.
Annotation file "train_RAK_0005.xml" invalid.
Annotation file "train_RAK_0006.xml" invalid.
Annotation file "train_RAK_0007.xml" invalid.
Annotation file "train_RAK_0008.xml" invalid.
Annotation file "train_RAK_0009.xml" invalid.
Annotation file "train_RAK_0016.xml" invalid.
Annotation file "train_RAK_0017.xml" invalid.
Annotation file "train_RAK_0018.xml" invalid.
Annotation file "train_RAK_0019.xml" invalid.
Annotation file "train_RAK_0020.xml" invalid.
Annotation file "train_RAK_0021.xml" invalid.
Annotation file "train_RAK_0022.xml" invalid.
Annotation file "train_RAK_0036.xml" invalid.
Annotation file "train_RAK_0037.xml" invalid.
Annotation file "train_RAK_0038.xml" invalid.
Annotation file "train_RAK_0039.xml" invalid.
Annotation file "train_RAK_0040.xml" invalid.
Annotation file "train_RAK_0041.xml" invalid.
Annotation file "train_RAK_0042.xml" invalid.
Annotation file "train_RAK_0043.xml" invalid.
Annotation file "train_RAK_0044.xml" invalid.
Annotation file "train_RAK_0045.xml" invalid.
Annotation file "train_RAK_0046.xml" invalid.
Annotation file "train_RAK_0047.xml" invalid.
Annotation file "train_RAK_0048.xml" invalid.
Annotation file "train_RAK_0049.xml" invalid.
Annotation file "train_RAK_0050.xml" invalid.
Annotation file "train_RAK_0051.xml" invalid.
Annotation file "train_RAK_0058.xml" invalid.
Annotation file "train_RAK_0059.xml" invalid.
Annotation file "train_RAK_0068.xml" invalid.
Annotation file "train_RAK_0080.xml" invalid.
Annotation file "train_VRD_0006.xml" invalid.
Annotation file "train_VRD_0017.xml" invalid.
Annotation file "train_VRD_0018.xml" invalid.
Annotation file "train_VRD_0019.xml" invalid.
Annotation file "train_VRD_0020.xml" invalid.
Annotation file "train_VRD_0021.xml" invalid.
Annotation file "train_VRD_0022.xml" invalid.
Annotation file "train_VRD_0023.xml" invalid.
Annotation file "train_VRD_0024.xml" invalid.
Annotation file "train_VRD_0025.xml" invalid.
Annotation file "train_VRD_0029.xml" invalid.
Annotation file "train_VRD_0030.xml" invalid.
Annotation file "train_VRD_0035.xml" invalid.
Annotation file "train_VRD_0036.xml" invalid.
Annotation file "train_VRD_0037.xml" invalid.
Annotation file "train_VRD_0038.xml" invalid.
Annotation file "train_VRD_0039.xml" invalid.
Annotation file "train_VRD_0040.xml" invalid.
Annotation file "train_VRD_0041.xml" invalid.
Annotation file "train_VRD_0042.xml" invalid.
Annotation file "train_VRD_0043.xml" invalid.
Annotation file "train_VRD_0044.xml" invalid.
Annotation file "train_VRD_0045.xml" invalid.
Annotation file "train_VRD_0046.xml" invalid.
Annotation file "train_VRD_0047.xml" invalid.
Annotation file "train_VRD_0048.xml" invalid.
Annotation file "train_VRD_0049.xml" invalid.
Annotation file "train_VRD_0050.xml" invalid.
Annotation file "train_VRD_0051.xml" invalid.
Annotation file "train_VRD_0052.xml" invalid.
Annotation file "train_VRD_0053.xml" invalid.
Annotation file "train_VRD_0067.xml" invalid.
Annotation file "train_VRD_0068.xml" invalid.
Annotation file "train_VRD_0069.xml" invalid.
Annotation file "train_VRD_0070.xml" invalid.
Annotation file "train_VRD_0071.xml" invalid.
Annotation file "train_VRD_0072.xml" invalid.
Annotation file "train_VRD_0073.xml" invalid.
Annotation file "train_VRD_0074.xml" invalid.
Annotation file "train_VRD_0075.xml" invalid.
Annotation file "train_VRD_0076.xml" invalid.
Annotation file "train_VRD_0077.xml" invalid.
Annotation file "train_VRD_0078.xml" invalid.
Annotation file "train_VRD_0079.xml" invalid.
Annotation file "train_VRD_0080.xml" invalid.
Annotation file "train_VRD_0092.xml" invalid.
Annotation file "train_VRD_0100.xml" invalid.
Annotation file "train_VRD_0101.xml" invalid.
Annotation file "train_VRD_0102.xml" invalid.
Annotation file "train_VRD_0103.xml" invalid.
Annotation file "train_VRD_0104.xml" invalid.
Annotation file "train_VRD_0105.xml" invalid.
Annotation file "train_VRD_0106.xml" invalid.
Annotation file "train_VRD_0107.xml" invalid.
Annotation file "train_VRD_0108.xml" invalid.
Annotation file "train_VRD_0122.xml" invalid.
Annotation file "train_VRD_0123.xml" invalid.
Annotation file "train_VRD_0124.xml" invalid.
Annotation file "train_VRD_0125.xml" invalid.
Annotation file "train_VRD_0126.xml" invalid.
Annotation file "train_VRD_0127.xml" invalid.
Annotation file "train_VRD_0128.xml" invalid.
Annotation file "train_VRD_0129.xml" invalid.
Annotation file "train_VRD_0131.xml" invalid.
Annotation file "train_VRD_0137.xml" invalid.
Annotation file "train_VRD_0138.xml" invalid.
Annotation file "train_VRD_0139.xml" invalid.
Annotation file "train_VRD_0140.xml" invalid.
Annotation file "train_VRD_0150.xml" invalid.
Annotation file "train_VRD_0151.xml" invalid.
Annotation file "train_VRD_0152.xml" invalid.
Annotation file "train_VRD_0153.xml" invalid.
Annotation file "train_VRD_2006.xml" invalid.
Annotation file "train_VRD_2015.xml" invalid.
Annotation file "train_VRD_2016.xml" invalid.
Annotation file "train_VRD_2017.xml" invalid.
Annotation file "train_VRD_2018.xml" invalid.
Annotation file "train_VRD_2019.xml" invalid.
Annotation file "train_VRD_2022.xml" invalid.
Annotation file "train_VRD_2026.xml" invalid.
Annotation file "train_VRD_2027.xml" invalid.
Annotation file "train_VRD_2028.xml" invalid.
Annotation file "train_VRD_2029.xml" invalid.
Annotation file "train_VRD_2038.xml" invalid.
Annotation file "train_VRD_2039.xml" invalid.
Annotation file "train_VRD_2040.xml" invalid.
Annotation file "train_VRD_2041.xml" invalid.
Annotation file "train_VRD_2042.xml" invalid.
Annotation file "train_VRD_2043.xml" invalid.
Annotation file "train_VRD_2044.xml" invalid.
Annotation file "train_VRD_2045.xml" invalid.
Annotation file "train_VRD_2052.xml" invalid.
Annotation file "train_VRD_2053.xml" invalid.
Annotation file "train_VRD_3011.xml" invalid.
Annotation file "train_VRD_3012.xml" invalid.
Annotation file "train_VRD_3020.xml" invalid.
Annotation file "train_VRD_3021.xml" invalid.
Annotation file "train_VRD_3022.xml" invalid.
Annotation file "train_VRD_3025.xml" invalid.
Annotation file "train_VRD_3026.xml" invalid.
Annotation file "train_VRD_3027.xml" invalid.
Annotation file "train_VRD_3029.xml" invalid.
Annotation file "train_VRD_3030.xml" invalid.
Annotation file "train_VRD_3031.xml" invalid.
Annotation file "train_VRD_3032.xml" invalid.
Annotation file "train_VRD_3033.xml" invalid.
Annotation file "train_VRD_3034.xml" invalid.
Annotation file "train_VRD_3035.xml" invalid.
Annotation file "train_VRD_3036.xml" invalid.
Annotation file "train_VRD_3037.xml" invalid.
Annotation file "train_VRD_3038.xml" invalid.
Annotation file "train_VRD_3039.xml" invalid.
Annotation file "train_VRD_3040.xml" invalid.
Annotation file "train_VRD_3041.xml" invalid.
Annotation file "train_VRD_3042.xml" invalid.
Annotation file "train_VRD_3043.xml" invalid.
Annotation file "train_VRD_3044.xml" invalid.
Annotation file "train_VRD_3045.xml" invalid.
Annotation file "train_VRD_3046.xml" invalid.
Annotation file "train_VRD_3047.xml" invalid.
Annotation file "train_VRD_3048.xml" invalid.
Annotation file "train_VRD_3049.xml" invalid.
Annotation file "train_VRD_3050.xml" invalid.
Annotation file "train_VRD_3051.xml" invalid.
Annotation file "train_VRD_3052.xml" invalid.
Annotation file "train_VRD_3053.xml" invalid.
Annotation file "train_VRD_3054.xml" invalid.
Annotation file "train_VRD_3055.xml" invalid.
Annotation file "train_VRD_3056.xml" invalid.
Annotation file "train_VRD_3057.xml" invalid.
Annotation file "train_VRD_3058.xml" invalid.
Annotation file "train_VRD_3059.xml" invalid.
Annotation file "train_VRD_3060.xml" invalid.
Annotation file "train_VRD_3061.xml" invalid.
Annotation file "train_VRD_3062.xml" invalid.
Annotation file "train_VRD_3063.xml" invalid.
Annotation file "train_VRD_3064.xml" invalid.
Annotation file "train_VRD_3065.xml" invalid.
Annotation file "train_VRD_3066.xml" invalid.
Annotation file "train_VRD_3067.xml" invalid.
Annotation file "train_VRD_3068.xml" invalid.
Annotation file "train_VRD_3069.xml" invalid.
Annotation file "train_VRD_3070.xml" invalid.
Annotation file "train_VRD_3071.xml" invalid.
Annotation file "train_VRD_3072.xml" invalid.
Annotation file "train_VRD_3073.xml" invalid.
Annotation file "train_VRD_3074.xml" invalid.
Annotation file "train_VRD_3075.xml" invalid.
Annotation file "train_VRD_3076.xml" invalid.
Annotation file "train_VRD_3077.xml" invalid.
Annotation file "train_VRD_3078.xml" invalid.
Annotation file "train_VRD_3079.xml" invalid.
Annotation file "train_VRD_3080.xml" invalid.
Annotation file "train_VRD_3081.xml" invalid.
Annotation file "train_VRD_3092.xml" invalid.
Annotation file "train_VRD_3093.xml" invalid.
Annotation file "train_VRD_3094.xml" invalid.
Annotation file "train_VRD_3110.xml" invalid.
Annotation file "train_VRD_3111.xml" invalid.
Annotation file "train_VRD_3112.xml" invalid.
Annotation file "train_VRD_3113.xml" invalid.
Annotation file "train_VRD_3114.xml" invalid.
Annotation file "train_VRD_3115.xml" invalid.
Annotation file "train_VRD_3116.xml" invalid.
Annotation file "train_VRD_3117.xml" invalid.
Annotation file "train_VRD_3118.xml" invalid.
Annotation file "train_VRD_3119.xml" invalid.
Annotation file "train_VRD_3120.xml" invalid.
Annotation file "train_VRD_3127.xml" invalid.
Annotation file "train_VRD_3128.xml" invalid.
Annotation file "train_VRD_3129.xml" invalid.
Annotation file "train_VRD_3131.xml" invalid.
Annotation file "train_ZRI_2003.xml" invalid.
Annotation file "train_ZRI_2036.xml" invalid.
Annotation file "train_ZRI_2039.xml" invalid.
Annotation file "train_ZRI_2081.xml" invalid.
Annotation file "train_ZRI_2085.xml" invalid.
Annotation file "train_ZRI_3028.xml" invalid.
Annotation file "train_ZRI_3029.xml" invalid.
Process completed with 563 bad xml files, 0 missing images, and 985 no errors. 1548 files processed total.
Skipping image "test_GRO_0005.JPG" as it does not exist in img directory.
Skipping image "test_SB_0004.JPG" as it does not exist in img directory.
Process completed with 0 bad xml files, 2 missing images, and 101 no errors. 103 files processed total.
"""