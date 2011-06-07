#!/bin/bash

#for f in `ls shishi`; do ./shishi2bhps.sh "shishi/$f" "bhps/$f.png"; done
#for f in `ls shishi`; do ./shishi2bdp.sh "shishi/$f" "bdp/$f.png"; done
for f in `ls bdp`; do ./bdp2tethical.sh "bdp/$f" "tethical/$f.png"; done
for f in `ls shishi`; do ./shishi2tethical_face.sh "shishi/$f" "tethical/"$f"_face.png"; done
