#!/usr/bin/env bash

if [ ! -n "$1" ] || [ ! -n "$2" ];then
    echo "Usage: ./pushToVOCdevkit.sh [VOCdevkit path] [dataset name, eg,ICDAR2017]"
    exit 1
fi

if [ ! -d Annotations ];then
    echo "Annotations not found. Please create it."
    exit 1
fi

if [ ! -d JPEGImages ];then
    echo "JPEGImages not found. Please create it."
    exit 1
fi

if [ ! -d ImageSets ];then
    echo "ImageSets not found. Please create it."
    exit 1
fi

mkdir -p $1/$2 
mv Annotations $1/$2/
mv JPEGImages $1/$2/
mv ImageSets $1/$2/
rm temp

echo "Creating $1/$2"
