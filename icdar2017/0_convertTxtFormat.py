#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python convertTxtFormat.py [file path, eg: train]
'''
import os, sys

def test(argv):
    if not os.path.exists('temp'):
        os.makedirs('temp')

    sumary = len(os.listdir(argv[1])) 
    i = 0
    for each in os.listdir(argv[1]):
        #print each
        if not each.endswith('.txt'):
            continue
        contents = []
        with open(argv[1]+'/{}'.format(each)) as fid:
            lines = fid.readlines()
            for line in lines:
                line = line.decode('utf-8-sig').encode('utf-8').split(',')[:8]
                contents.append(line)
        with open('temp/{}'.format(each), 'w') as fid:
            for c in contents:
                fid.write("{}\n".format(c))
        #print "saving {}".format(each)

        #print "{}/{}".format(i, sumary)
        sys.stdout.flush()
        sys.stdout.write('{}/{}\r'.format(i, sumary))
        i += 1
    print '\nFinish!'

def main():
    import sys
    if len(sys.argv) != 2:
        print(__doc__)
        return
    test(sys.argv)

if __name__ == "__main__":
    main()

