#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python createJPEGImages.py [file path containing jpg] [img_ext, eg:jpg]
'''
import os,sys,commands

def createJPEGImages(argv):
    if not os.path.exists('JPEGImages'):
        os.makedirs('JPEGImages')
    os.chdir('JPEGImages')

    root = argv[1]
    if not root.endswith('/'):
        root += '/'

    img_ext = argv[2]
    files = sorted([x for x in os.listdir(root) if x.endswith('.{}'.format(img_ext))]);

    i = 0
    for f in files:
        index = f[6:-4] # image_0.jpg
        cmd = 'ln -s {}{} {:0>6}.jpg'.format(root, f, index)
        #print cmd
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            print "Error when run \"ln\""
            return

        sys.stdout.flush()
        sys.stdout.write('{}/{}\r'.format(i, len(files)))
        i += 1
    print '\nFinish!'

def main():
    import sys
    if len(sys.argv) != 3:
        print(__doc__)
        return
    createJPEGImages(sys.argv)

if __name__ == "__main__":
    main()

##!/usr/bin/env bash
#
#if [ ! -n "$1" ] || [ ! -n "$2" ];then
#    echo "Usage: ./getImageLink.sh [file path containing jpg] [img_ext, eg:jpg]"
#    exit 1
#fi
#
#if [ ! -d JEPGImages ];then
#    mkdir JEPGImages
#fi
#
#for i in ${files};do
#    
#    length=${#i}
#    echo ${i:6:${length}};
#    ln -s `pwd`/${i} JEPGImages/${i:6:${length}}
#done
