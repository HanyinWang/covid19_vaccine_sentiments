
import sys
sys.path.append('./')
import os
import cv2
import dlib
import numpy as np
import argparse
from contextlib import contextmanager
from wide_resnet import WideResNet
from keras.utils.data_utils import get_file
import csv

pretrained_model = "https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/weights.28-3.73.hdf5"
modhash = 'fbe63257a054c1c5466cfd7bf14646d6'

wd = '../../data'
print(os.getcwd())

os.chdir(wd)

class MyImage:
    def __init__(self, img_name):
        # self.img = cv2.imread(wd + "profile_img/"+img_name)
        self.img = cv2.imread(img_name)
        self.__name = img_name

    def __str__(self):
        return self.__name

def get_args():
    parser = argparse.ArgumentParser(description="This script detects faces from web cam input, "
                                                 "and estimates age and gender for the detected faces.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--weight_file", type=str, default=None,
                        help="path to weight file (e.g. weights.28-3.73.hdf5)")
    parser.add_argument("--depth", type=int, default=16,
                        help="depth of network")
    parser.add_argument("--width", type=int, default=8,
                        help="width of network")
    parser.add_argument("--margin", type=float, default=0.4,
                        help="width of network")
    parser.add_argument('--part', type = str,
                        help='part of data (starting from 1)')
    args = parser.parse_args()
    return args


def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=1, thickness=2):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness)


def yield_images(images):
    for img in images:
        yield(MyImage(img))


def main():
    args = get_args()
    depth = args.depth
    k = args.width
    weight_file = args.weight_file
    margin = args.margin
    part = args.part

    # for earlier parts
    # f = open('/projects/b1131/Hanyin/Twitter/profile_img_paths.txt', 'r')
    # all_images = f.readlines()
    # f.close()
    # images = all_images[((int(part) - 1) * 600000):(int(part) * 600000)]
    # images = [img[:-1] for img in images]
    #
    # print('Number of images: ', len(images))

    # for extraction of more recent daily data
    images = os.listdir("profile_img/part_%s"%(part))
    # images = os.listdir("/projects/b1131/Hanyin/Twitter/test_img")


    if not weight_file:
        weight_file = get_file("weights.28-3.73.hdf5", pretrained_model, cache_subdir="pretrained_models",
                               file_hash=modhash, cache_dir=os.path.dirname(os.path.abspath(__file__)))

    # for face detection
    detector = dlib.get_frontal_face_detector()
    print('detector ready')

    # load model and weights
    img_size = 64
    model = WideResNet(img_size, depth=depth, k=k)()
    model.load_weights(weight_file)
    print('model loaded')

    for img in images:
        img = MyImage("profile_img/part_%s/"%(part)+img)
        # processed_file = open('/projects/b1131/Hanyin/Twitter/age_gender/age_gender_part%s.csv'%(part))
        # processed_img = []
        # for lines in processed_file.readlines():
        #     lst = lines.split('|$|')
        #     processed_img.append(lst)
        # if img not in processed_img:
        try:
            name = str(img)
            print('name: ', name)
            img = img.img
            input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_h, img_w, _ = np.shape(input_img)

            # detect faces using dlib detector
            detected = detector(input_img, 1)
            print('detected: ', detected)
            faces = np.empty((len(detected), img_size, img_size, 3))
        except:
            print('empty image')
            continue

        if len(detected) > 0:
            for i, d in enumerate(detected):
                x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
                xw1 = max(int(x1 - margin * w), 0)
                yw1 = max(int(y1 - margin * h), 0)
                xw2 = min(int(x2 + margin * w), img_w - 1)
                yw2 = min(int(y2 + margin * h), img_h - 1)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
                faces[i, :, :, :] = cv2.resize(img[yw1:yw2 + 1, xw1:xw2 + 1, :], (img_size, img_size))

            # predict ages and genders of the detected faces
            results = model.predict(faces)
            predicted_genders = results[0]
            ages = np.arange(0, 101).reshape(101, 1)
            predicted_ages = results[1].dot(ages).flatten()

            # draw results
            for i, d in enumerate(detected):
                label = "{}, {}".format(int(predicted_ages[i]),
                                        "F" if predicted_genders[i][0] > 0.5 else "M")
                draw_label(img, (d.left(), d.top()), label)

            s = '|$|'
            output_str = s.join([name, str(predicted_ages), str(predicted_genders)])
            csv_file = open('age_gender/age_gender_part%s.csv'%(part), 'a')
            csv_file.write(output_str)
            csv_file.write('\n')
            csv_file.close()
        # cv2.imshow("result", img)
        # key = cv2.waitKey(30)
        #
        # if key == 27:
        #     break


if __name__ == '__main__':
    main()
