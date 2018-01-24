#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from PIL import Image
from PIL import ImageEnhance

def set_opacity(im, opacity):
    """设置透明度"""

    assert opacity >= 0 and opacity < 1
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, type, args, opacity=1.0):
    """添加水印"""
    try:
        if opacity < 1:
            mark = set_opacity(mark, opacity)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        if im.size[0] < mark.size[0] or im.size[1] < mark.size[1]:
            print "The mark image size is larger size than original image file."
            return False

        print u"image size:", im.size
        print u"watermark size:", mark.size
        print u"space:", args.space
        layer = Image.new('RGBA', im.size, (0,0,0,0))
        for x_index in range(0, int(im.size[0]/mark.size[0])+1):
            for y_index in range(0, int(im.size[1]/mark.size[1])+1):
                # print x_index, y_index
                layer.paste(mark, (x_index * (mark.size[0] + args.space), y_index * (mark.size[1] + args.space)))

        return Image.composite(layer, im, layer)
    except Exception as e:
        print "Sorry, Exception: " + str(e)
        return False




def add_mark(imagePath, watermarkPath, args):
    print "\nprocessing image", imagePath
    im = Image.open(imagePath)
    mark = Image.open(watermarkPath)
    image = watermark(im, mark, args.type, args, 1)
    if image:
        name = os.path.basename(imagePath)
        if not os.path.exists(args.out):
            os.mkdir(args.out)

        new_name = os.path.join(args.out, name)
        if os.path.splitext(new_name)[1] != '.png':
            image = image.convert('RGB')
        image.save(new_name)
        if args.show:
            image.show()

        print "Success add watermark " + watermarkPath + " on " + imagePath + " to " + os.path.abspath(new_name)
    else:
        print "Sorry, Failed."


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("filepath", type=str, help="image file path or directory")
    parse.add_argument("watermarkpath", type=str, help="watermark file path")
    parse.add_argument("-o", "--out", default="./output", help="image output directory")
    parse.add_argument("-t", "--type", default="tile", choices=['tile'], help="type of add watermark. allowed [tile, ]")
    parse.add_argument("-s", "--space", type=int, default=0, help="space of tile watermark image")
    parse.add_argument("--show", action="store_true", help="is show watermark result if set true.")
    parse.add_argument("--opacity", default=1, help="opacity of add watermark, default is 1.0")

    args = parse.parse_args()
    print args

    if os.path.isdir(args.filepath):
        names = os.listdir(args.filepath)
        for name in names:
            image_file = os.path.join(args.filepath, name)
            add_mark(image_file, args.watermarkpath, args)
    else:
        add_mark(args.filepath, args.watermarkpath, args)

if __name__ == '__main__':
    main()
