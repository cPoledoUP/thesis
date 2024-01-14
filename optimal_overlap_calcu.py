import os
import xml.etree.ElementTree as ET
import math


def optimize_overlap(label_folder, target_crop_w, target_crop_h):
    files = os.listdir(label_folder)

    max_w = 0
    max_h = 0
    all_w = list()
    all_h = list()

    for file in files:
        if file.endswith(".xml"):
            # read xml and calculate width and height of objects
            tree = ET.parse(os.path.join(label_folder, file))
            root = tree.getroot()

            for object in tree.findall("object"):
                min_x = int(object.find("bndbox").find("xmin").text)
                min_y = int(object.find("bndbox").find("ymin").text)
                max_x = int(object.find("bndbox").find("xmax").text)
                max_y = int(object.find("bndbox").find("ymax").text)

            curr_w = max_x - min_x + 1
            curr_h = max_y - min_y + 1

            if max_w < curr_w:
                max_w = curr_w
            if max_h < curr_h:
                max_h = curr_h

            all_w.append(curr_w)
            all_h.append(curr_h)

    # worst case is when crop is directly in the middle (both side is 50% of orig object)
    # calculating optimal overlaps
    optimal_overlap_w = max_w / 2 / target_crop_w * 100
    optimal_overlap_h = max_h / 2 / target_crop_h * 100
    print(f"\n>>> Optimal overlap for {target_crop_w} x {target_crop_h} crop\n")
    print(f"===== Based on largest width({max_w}) and height({max_h}) =====")
    print("width overlap:", math.ceil(optimal_overlap_w) / 100)
    print("height overlap:", math.ceil(optimal_overlap_h) / 100)
    ave_w = sum(all_w) / len(all_w)
    ave_h = sum(all_h) / len(all_h)
    optimal_overlap_w = ave_w / 2 / target_crop_w * 100
    optimal_overlap_h = ave_h / 2 / target_crop_h * 100
    print(
        f"\n===== Based on average width({round(ave_w)}) and height({round(ave_h)}) ====="
    )
    print("width overlap:", math.ceil(optimal_overlap_w) / 100)
    print("height overlap:", math.ceil(optimal_overlap_h) / 100)


# note to future self, accept objects that are still 75% whole after crop to remove dupes while minimizing crops for a bit faster training
# optimize_overlap(
#     "C:/Users/Japh/Documents/Thesis2/heridal/trainImages/labels/", 320, 320
# )
# optimize_overlap(
#     "C:/Users/Japh/Documents/Thesis2/heridal/trainImages/labels/", 640, 640
# )
# optimize_overlap(
#     "C:/Users/Japh/Documents/Thesis2/heridal/trainImages/labels/", 512, 512
# )
optimize_overlap(
    "C:/Users/Japh/Documents/Thesis2/heridal/trainImages/labels/", 1280, 1280
)
