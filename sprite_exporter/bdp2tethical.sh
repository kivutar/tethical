#!/bin/bash

echo "converting $1 to $2"

input=$1
output=$2
tile="48x48"
l1=0
l2=48
l3=96
l4=144

transpose() {
    convert -extract $tile+$(($2*48))+$(($3*48)) -transparent black $input /tmp/tmp.bmp
    composite -compose atop -geometry +$(($1*48))+$l1 /tmp/tmp.bmp $output $output

    convert -flop /tmp/tmp.bmp /tmp/tmp.bmp
    composite -compose atop -geometry +$(($1*48))+$l2 /tmp/tmp.bmp $output $output

    convert -extract $tile+$(($4*48))+$(($5*48)) -transparent black $input /tmp/tmp.bmp
    composite -compose atop -geometry +$(($1*48))+$l4 /tmp/tmp.bmp $output $output

    convert -flop /tmp/tmp.bmp /tmp/tmp.bmp
    composite -compose atop -geometry +$(($1*48))+$l3 /tmp/tmp.bmp $output $output
}

convert -size 672x192 xc:black $output

transpose  0   2 0   8 0
transpose  1   9 0  14 0
transpose  2  10 0  15 0
transpose  3  11 0   0 1
transpose  4  12 0   1 1
transpose  5  13 0   2 1
transpose  6   4 4   5 4
transpose  7   8 4   9 4
transpose  8   7 1   8 1
transpose  9  12 5  13 8
transpose 10  13 5  14 8
transpose 11   2 6   3 9
transpose 12   3 6   4 9
transpose 13   4 6   5 9

convert -transparent black $output $output
