#!/bin/bash

echo "converting $1 to $2"

convert -extract 48x32+80+456 -rotate -90 $1 $2
