#!/bin/bash

for f in *.bmp
do
    echo "converting $f"
    ./$1 $f "$f.png"
done

