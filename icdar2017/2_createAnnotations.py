#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''
Convert icdar2017rctw to VOC2007 format
Usage: python convert.py [annotation_path]
'''
import sys
import os
import os.path as osp
import copy
import Image

Annnotation = """<annotation>
	<folder>icdar2017</folder>
	<filename>{}</filename>
	<source>
		<database>The ICDAR2017 Database</database>
		<annotation>ICDAR2017</annotation>
		<image>flickr</image>
		<flickrid>341012865</flickrid>
	</source>
	<owner>
		<flickrid>Fried Camels</flickrid>
		<name>Jinky the Fruit Bat</name>
	</owner>
	<size>
		<width>{}</width>
		<height>{}</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
        {}
</annotation>
"""
Object = """
	<object>
		<name>{}</name>
		<pose>Left</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{}</xmin>
			<ymin>{}</ymin>
			<xmax>{}</xmax>
			<ymax>{}</ymax>
		</bndbox>
	</object>
"""

def getImageSize(imgPath, imgName):
    filename = os.path.join(imgPath, "{}.jpg".format(imgName))
    print filename
    return Image.open(filename).size

def convert(filepath):
    root = os.path.dirname(os.path.abspath(filepath))
    if not os.path.exists(osp.join(root, 'JPEGImages')):
        print "Please create JPEGImages."
        return
    if not os.path.exists(osp.join(root, 'Annotations')):
        os.makedirs('Annotations')

    global Annnotation
    global Object
    files = sorted([x for x in os.listdir(filepath) if not x.startswith('.') and x.endswith('.txt')])

    for txt in files: # image_0.txt
        imgname = '{:0>6}'.format(txt[6:-4])
        width, height = getImageSize(osp.join(root, 'JPEGImages'), imgname)
        name = 'text'
        objs = ""
        with open(os.path.join(filepath, txt), 'r') as fid:
            lines = [x.split('\n')[0] for x in fid.readlines()]
            for box in lines: # multi boxes for one class
                box = eval(box)
                assert(len(box) == 8)
                x1 = eval(box[0])
                y1 = eval(box[1])
                x2 = eval(box[2])
                y2 = eval(box[3])
                x3 = eval(box[4])
                y3 = eval(box[5])
                x4 = eval(box[6])
                y4 = eval(box[7])
                
                xmin = min(x1,x2,x3,x4)
                ymin = min(y1,y2,y3,y4)
                xmax = max(x1,x2,x3,x4)
                ymax = max(y1,y2,y3,y4)

                newObj = copy.deepcopy(Object).format(name, xmin, ymin, xmax, ymax)
                #newObj = Object.format(name, x1, y1, x2, y2)
                objs += newObj
        newAnno = copy.deepcopy(Annnotation).format(imgname, width, height, objs)

        with open('Annotations/{}.xml'.format(imgname), 'w') as fid:
            fid.write(newAnno)
        print "write to Annotations/{}".format(imgname)

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return
    convert(sys.argv[1])

if __name__ == "__main__":
    main()
