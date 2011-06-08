#!/bin/bash

echo "converting $1 to $2"

convert -size 32x64 xc:black $2

convert -extract 48x32+80+456 -rotate -90 $1 /tmp/tmp.bmp
composite -compose atop -geometry +0+8 /tmp/tmp.bmp $2 $2

convert -transparent black $2 $2
