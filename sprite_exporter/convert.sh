#!/bin/bash

#for f in `ls shishi`; do ./shishi2bhps.sh "shishi/$f" "bhps/$f.png"; done
for f in `ls shishi`; do ./shishi2bdp.sh "shishi/$f" "bdp/"$(basename $f '.bmp')".png"; done
for f in `ls bdp`; do ./bdp2tethical.sh "bdp/$f" "tethical/"$(basename $f '.png')".png"; done
for f in `ls shishi`; do ./shishi2tethical_face.sh "shishi/$f" "tethical/"$(basename $f '.bmp')"_face.png"; done
