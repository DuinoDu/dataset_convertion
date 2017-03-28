#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''
Convert SLOTH to VOC2007 format
Usage: python convert.py [annotation_path] [image_path]
'''
import sys
import os
import os.path as osp
import copy
import Image
import json
import commands

Annnotation = """<annotation>
	<folder>sloth</folder>
	<filename>{}</filename>
	<source>
		<database>SLOTH</database>
		<annotation>none</annotation>
		<image>none</image>
		<flickrid>none</flickrid>
	</source>
	<owner>
		<flickrid>none</flickrid>
		<name>none</name>
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

def getImageSize(filename):
    return Image.open(filename).size

def convert(annopath, imgpath):
    if not os.path.exists('Annotations'):
        os.makedirs('Annotations')
    if not os.path.exists('JPEGImages'):
        os.makedirs('JPEGImages')
    if not os.path.exists('ImageSets'):
        os.makedirs('ImageSets')

    root = os.path.abspath(annopath)
    jsonfiles = os.listdir(root)
    for f in jsonfiles:
        if not f.endswith('.json'):
            print "Please use sloth to generate annotations."
            return
    classes = [x[:-5] for x in jsonfiles]

    imgroot = os.path.abspath(imgpath)
    img_classes = os.listdir(imgroot)
    img_classes.remove('.DS_Store')

    imagefiles = []
    allboxes = []
    classnames = []
    for f,classname in zip(jsonfiles, classes):
        anno_list = json.load(file(os.path.join(root, f))) 
        for anno in anno_list:
            imagefiles.append(os.path.split(anno['filename'])[1])
            boxes = []
            for b in anno['annotations']:
                assert b['class'] == 'rect', 'Only support rect annotation'
                xmin = int(b['x'])
                ymin = int(b['y'])
                xmax = int(b['x'] + b['width'])
                ymax = int(b['y'] + b['height'])
                boxes.append([xmin, ymin, xmax, ymax, classname])
            allboxes.append(boxes)
            classnames.append([x for x in img_classes if x.lower() in classname][0])

    global Annnotation
    global Object
    for i in xrange(len(imagefiles)):
        imgfilePath = os.path.join(imgroot, classnames[i], imagefiles[i])
        width, height = getImageSize(imgfilePath)
        objs = ""
        for b in allboxes[i]: 
            newObj = copy.deepcopy(Object).format(b[4], b[0], b[1], b[2], b[3])
            objs += newObj
        newAnno = copy.deepcopy(Annnotation).format("{:0>6}".format(i+1), width, height, objs)

        # write xml
        with open('Annotations/{:0>6}.xml'.format(i+1), 'w') as fid:
            fid.write(newAnno)

        # create image link
        (status, output) = commands.getstatusoutput('ln -s {} {}{:0>6}.jpg'.format(imgfilePath, 'JPEGImages/', i+1))
        output = output.split('\n')

        sys.stdout.flush()
        sys.stdout.write("{}/{}".format(i+1, len(imagefiles)))

    print '\nFinish!'

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return
    convert(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
