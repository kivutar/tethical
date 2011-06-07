#!/bin/bash

echo "converting $1 to $2"

convert -size 256x72 xc:black $2

convert -extract 160x040+000+000 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +032+000 /tmp/tmp.bmp $2 $2

convert -extract 032x016+128+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +192+020 /tmp/tmp.bmp $2 $2

convert -extract 032x024+128+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +192+000 /tmp/tmp.bmp $2 $2

convert -extract 032x016+128+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +224+020 /tmp/tmp.bmp $2 $2

convert -extract 032x024+128+192 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +224+000 /tmp/tmp.bmp $2 $2

convert -extract 064x032+160+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +032+040 /tmp/tmp.bmp $2 $2

convert -extract 080x032+160+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +096+040 /tmp/tmp.bmp $2 $2

convert -transparent black $2 $2
