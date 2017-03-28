#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python createImageSets.py args [file path containing image, eg:JPEGImages]
'''

import os,sys

def createImageSets(argv):
    root = os.path.dirname(os.path.abspath(argv[1]))
    if not os.path.exists(os.path.join(root, 'JPEGImages')):
        print "Please create JPEGImages."
        return
    if not os.path.exists(os.path.join(root, 'Annotations')):
        print "Please create Annotations."
        return
    if not os.path.exists(os.path.join(root, 'ImageSets/Main')):
        os.makedirs('ImageSets/Main')

    filenames = sorted([x[:-4] for x in os.listdir('JPEGImages') if not x.startswith('.') and x.endswith('.jpg')])
    amount = len(filenames)
    trainval = int(amount*0.8)
    train = int(amount*0.8*0.8)

    print 'create trainval.txt'
    with open('ImageSets/Main/text_trainval.txt', 'w') as fid:
        for name in filenames[ : trainval]:
            fid.write('{} 1\n'.format(name))

    print 'create train.txt'
    with open('ImageSets/Main/text_train.txt', 'w') as fid:
        for name in filenames[ : train]:
            fid.write('{} 1\n'.format(name))

    print 'create val.txt'
    with open('ImageSets/Main/text_val.txt', 'w') as fid:
        for name in filenames[train : trainval]:
            fid.write('{} 1\n'.format(name))

    print 'create test.txt'
    with open('ImageSets/Main/text_test.txt', 'w') as fid:
        for name in filenames[trainval : ]:
            fid.write('{} 1\n'.format(name))

def main():
    import sys
    if len(sys.argv) != 2:
        print(__doc__)
        return
    createImageSets(sys.argv)

if __name__ == "__main__":
    main()
