#!/bin/bash

convert -size 767x1151 xc:black $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +20+32 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+1 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+1 /tmp/tmp.bmp $2 $2

convert -extract 32x40+64+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+1 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +201+1 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +249+1 /tmp/tmp.bmp $2 $2

convert -extract 32x40+96+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +297+1 /tmp/tmp.bmp $2 $2

convert -extract 32x40+128+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+1 /tmp/tmp.bmp $2 $2

convert -extract 32x40+96+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+1 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +443+11 /tmp/tmp.bmp $2 $2

convert -extract 32x40+160+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+3 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+15 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +490+10 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+2 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +495+14 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +538+9 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+1 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +543+13 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+10 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+2 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +591+14 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+11 /tmp/tmp.bmp $2 $2

convert -extract 32x40+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+3 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +639+15 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +687+11 /tmp/tmp.bmp $2 $2

convert -extract 32x40+96+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+3 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+14 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+10 /tmp/tmp.bmp $2 $2

convert -extract 32x40+128+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+2 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+13 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+57 /tmp/tmp.bmp $2 $2

convert -extract 32x40+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+49 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+60 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+58 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+50 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+61 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +111+59 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+51 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+62 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+74 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+66 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +155+54 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+74 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+66 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+24 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +203+54 /tmp/tmp.bmp $2 $2

convert -extract 32x32+160+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+57 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+57 /tmp/tmp.bmp $2 $2

convert -extract 40x32+160+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +340+65 /tmp/tmp.bmp $2 $2

convert -extract 40x32+200+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +388+65 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+49 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+49 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+49 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+49 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +532+56 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+49 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+60 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +582+50 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+49 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +590+52 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +637+51 /tmp/tmp.bmp $2 $2

convert -extract 32x40+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+49 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +627+55 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +685+49 /tmp/tmp.bmp $2 $2

convert -extract 32x40+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+49 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +676+53 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +726+50 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+49 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+74 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +734+52 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +6+98 /tmp/tmp.bmp $2 $2

convert -extract 32x40+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +14+100 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +61+97 /tmp/tmp.bmp $2 $2

convert -extract 32x32+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+97 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+122 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +52+101 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +109+97 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +100+101 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+64 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+121 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+120 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+97 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+64 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+121 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+97 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+64 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+121 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+97 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+64 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+121 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +342+98 /tmp/tmp.bmp $2 $2

convert -extract 32x40+160+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +350+100 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +388+104 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +395+108 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +442+105 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+109 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +491+105 /tmp/tmp.bmp $2 $2

convert -extract 32x40+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +495+109 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +541+97 /tmp/tmp.bmp $2 $2

convert -extract 32x40+96+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +532+101 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +589+99 /tmp/tmp.bmp $2 $2

convert -extract 32x40+128+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +579+103 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +639+105 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+108 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +687+105 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+108 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +724+104 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+97 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+109 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +6+146 /tmp/tmp.bmp $2 $2

convert -extract 32x40+160+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +11+156 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +59+156 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +100+152 /tmp/tmp.bmp $2 $2

convert -extract 32x40+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +110+148 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +157+147 /tmp/tmp.bmp $2 $2

convert -extract 32x40+128+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+156 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +205+145 /tmp/tmp.bmp $2 $2

convert -extract 32x40+96+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+156 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +243+151 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +292+149 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +351+157 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +388+152 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +399+157 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +438+146 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+157 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +486+146 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +495+157 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +499+156 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +543+157 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +587+156 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +638+148 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +687+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+156 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+153 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+145 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +723+151 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+201 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+193 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +4+197 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+201 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+193 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+204 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +108+195 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+193 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+204 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +156+191 /tmp/tmp.bmp $2 $2

convert -extract 32x40+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+193 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+204 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+218 /tmp/tmp.bmp $2 $2

convert -extract 32x24+128+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+197 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+218 /tmp/tmp.bmp $2 $2

convert -extract 32x24+128+192 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+197 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +298+201 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+193 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+205 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +351+201 /tmp/tmp.bmp $2 $2

convert -extract 32x40+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+193 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+204 /tmp/tmp.bmp $2 $2

convert -extract 32x32+160+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+201 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+160 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +404+210 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+201 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +500+224 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +548+224 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +596+224 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +644+224 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +692+224 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +740+224 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +20+272 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +68+272 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +116+272 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +164+272 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +211+243 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+248 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +209+242 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +203+252 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +260+244 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+248 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +257+242 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +251+252 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +301+244 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+248 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +305+242 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +299+252 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+247 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+249 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +350+244 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +350+254 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +389+250 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+249 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +398+244 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +398+254 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +438+251 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+249 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +446+244 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +446+254 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +483+257 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+249 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +491+249 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +498+255 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+258 /tmp/tmp.bmp $2 $2

convert -extract 32x32+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+249 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +538+250 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +546+254 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +587+251 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+248 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +593+242 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +589+251 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +637+249 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+248 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +641+242 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +637+251 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+251 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+249 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +686+244 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +686+254 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+249 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+249 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +734+244 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +734+254 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +5+296 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +14+292 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+301 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+299 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +62+292 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +62+302 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +101+303 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +107+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +110+306 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +147+304 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +155+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +158+306 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +201+300 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +206+292 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +206+302 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +246+301 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +251+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +254+306 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +291+305 /tmp/tmp.bmp $2 $2

convert -extract 32x32+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +298+298 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +301+307 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +353+299 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+296 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +353+290 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +349+298 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +401+300 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+296 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +401+290 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +397+298 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+299 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +446+292 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +443+302 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +484+300 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +491+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +486+306 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+302 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +542+292 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+302 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+304 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +587+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+306 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +639+298 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +638+292 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +635+302 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +681+304 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +683+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+306 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +726+307 /tmp/tmp.bmp $2 $2

convert -extract 32x32+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+297 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +730+298 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+308 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +17+347 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+344 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +17+338 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +13+346 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +65+347 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+344 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +65+338 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +61+346 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +109+349 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +110+340 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+348 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+349 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +158+340 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+348 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +202+349 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +203+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+354 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+347 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +254+340 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +251+350 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +298+350 /tmp/tmp.bmp $2 $2

convert -extract 32x32+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +298+346 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+356 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +353+347 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+344 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +353+338 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +349+346 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +399+347 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +398+340 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+348 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+348 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +446+340 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+348 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +491+346 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +494+340 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +491+350 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +540+349 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +542+340 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+350 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +588+347 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +590+340 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +587+349 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +630+343 /tmp/tmp.bmp $2 $2

convert -extract 32x32+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +639+337 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +639+349 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +678+343 /tmp/tmp.bmp $2 $2

convert -extract 32x32+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +687+337 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +687+349 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +724+343 /tmp/tmp.bmp $2 $2

convert -extract 32x32+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+345 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+337 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+349 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +4+391 /tmp/tmp.bmp $2 $2

convert -extract 32x32+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+385 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+397 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +52+391 /tmp/tmp.bmp $2 $2

convert -extract 32x32+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+385 /tmp/tmp.bmp $2 $2

convert -extract 8x8+0+480 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +67+396 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+397 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +108+386 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+392 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +113+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +109+395 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+391 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +158+388 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +158+398 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +198+403 /tmp/tmp.bmp $2 $2

convert -extract 32x32+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +202+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+404 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +260+388 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +253+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +309+389 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +301+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +348+389 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +349+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+389 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +393+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +390+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +437+392 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +441+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +438+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +484+389 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +530+394 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +533+388 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+396 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +580+399 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +577+390 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +588+395 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +641+394 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +637+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +634+395 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +689+394 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +685+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +682+395 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+390 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+393 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +729+386 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +726+394 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+434 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +9+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +6+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +54+432 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +57+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +54+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +109+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +105+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +102+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +149+439 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +149+436 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +195+438 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +197+436 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +253+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +249+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +246+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +293+436 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +340+442 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +337+438 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +340+442 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +401+442 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+442 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +397+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +449+442 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+442 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +445+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +493+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +484+437 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +537+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +533+436 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +529+438 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +589+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +585+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +582+443 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +633+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +629+436 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +626+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +685+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +681+434 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +678+442 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +729+441 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+441 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +725+436 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +722+446 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +5+490 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +1+486 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +0+494 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +66+488 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+490 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +61+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+492 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +114+488 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+490 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +109+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+492 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+487 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +153+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +147+488 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +207+487 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +201+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +196+485 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +251+489 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +245+484 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +242+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+487 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +297+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +291+488 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+489 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +337+486 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +336+494 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +402+488 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+490 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +397+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+491 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+487 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +441+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +438+491 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +495+487 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +484+485 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +543+487 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +537+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +531+488 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +591+487 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +585+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +579+488 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +639+487 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +633+482 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +630+490 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +687+490 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +683+481 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +677+485 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+490 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+489 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +731+481 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +725+485 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+538 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+537 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +11+529 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +1+536 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+538 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+537 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +59+529 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +49+536 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +111+538 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+537 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +107+529 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +97+536 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+530 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+538 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +157+530 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+538 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +204+530 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+537 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +201+530 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +195+536 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +239+535 /tmp/tmp.bmp $2 $2

convert -extract 32x32+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+537 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +241+534 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +240+542 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+176 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +308+560 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+529 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+543 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+529 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+168 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+543 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+529 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+543 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+529 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+168 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+543 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +537+529 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +537+543 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +585+529 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +585+543 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+529 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+543 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+529 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+543 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +731+539 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+531 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+545 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+543 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +10+586 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+578 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+592 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+590 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +58+585 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+577 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+591 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+589 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+586 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+578 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+592 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +111+590 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+587 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+579 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+593 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+591 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +207+587 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+579 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+593 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+590 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+586 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+578 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+592 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+589 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+585 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+577 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+591 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+588 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +351+586 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+578 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+592 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+589 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +399+587 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+579 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+593 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+590 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+594 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +443+582 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+594 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+24 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +491+582 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +540+589 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+8 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +588+589 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +638+588 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+208 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +684+590 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+577 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+591 /tmp/tmp.bmp $2 $2

convert -extract 32x32+32+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+577 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+639 /tmp/tmp.bmp $2 $2

convert -extract 32x32+64+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+625 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +52+632 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+639 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +59+636 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +102+626 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+639 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +110+628 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +157+627 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+639 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +147+631 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +205+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+639 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +196+629 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +246+626 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+650 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +254+628 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +294+626 /tmp/tmp.bmp $2 $2

convert -extract 32x40+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+625 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +302+628 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +349+625 /tmp/tmp.bmp $2 $2

convert -extract 32x32+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+650 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +340+629 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +397+625 /tmp/tmp.bmp $2 $2

convert -extract 32x40+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+625 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +388+629 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+120 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+625 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+625 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+184 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+625 /tmp/tmp.bmp $2 $2

convert -extract 32x32+0+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+625 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +630+626 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+639 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +638+628 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +676+632 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+639 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +683+636 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +730+633 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+625 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+639 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+637 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +11+681 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+685 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +61+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +52+677 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +109+675 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +99+679 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+681 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+684 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +207+681 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+684 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +244+680 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+685 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +294+674 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +299+684 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+681 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +347+684 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +388+680 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +398+676 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +445+675 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+684 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +493+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+684 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +543+681 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +531+679 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +591+681 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +580+677 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+681 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +639+685 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +676+680 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +687+685 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +726+674 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+673 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+687 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+685 /tmp/tmp.bmp $2 $2

convert -extract 24x24+128+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +6+722 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+733 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +19+732 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+729 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+733 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+729 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +107+732 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+729 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +158+724 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +207+729 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+732 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+729 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +243+727 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+729 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +292+725 /tmp/tmp.bmp $2 $2

convert -extract 24x24+176+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +351+729 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+152+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+732 /tmp/tmp.bmp $2 $2

convert -extract 24x24+200+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +396+723 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+104+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+732 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+56 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +444+719 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+721 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+735 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+732 /tmp/tmp.bmp $2 $2

convert -extract 32x24+128+152 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+725 /tmp/tmp.bmp $2 $2

convert -extract 32x24+128+192 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+725 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +587+724 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+24 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +634+724 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +684+733 /tmp/tmp.bmp $2 $2

convert -extract 8x8+240+160 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +692+741 /tmp/tmp.bmp $2 $2

convert -extract 24x16+224+8 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +732+733 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+779 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+771 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+785 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+783 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+778 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+770 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+784 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+777 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+769 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+200 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+783 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +111+781 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+778 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+770 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+784 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+779 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+771 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+785 /tmp/tmp.bmp $2 $2

convert -extract 24x24+56+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +207+783 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+779 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+771 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+216 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+785 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+778 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+770 /tmp/tmp.bmp $2 $2

convert -extract 32x16+32+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+784 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+781 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +351+777 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+769 /tmp/tmp.bmp $2 $2

convert -extract 32x16+64+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+783 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+780 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +399+778 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+40 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+770 /tmp/tmp.bmp $2 $2

convert -extract 32x16+96+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+784 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+781 /tmp/tmp.bmp $2 $2

convert -extract 24x24+80+104 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+779 /tmp/tmp.bmp $2 $2

convert -extract 32x16+0+80 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+771 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+232 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+785 /tmp/tmp.bmp $2 $2

convert -extract 24x24+32+128 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +499+771 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+776 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +497+770 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +491+780 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +548+772 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+776 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +545+770 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+780 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +589+772 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+776 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +593+770 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +587+780 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+775 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+777 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+783 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +638+772 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +638+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +677+778 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+777 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+783 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +686+772 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +686+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +726+779 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+777 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+783 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +734+772 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +734+782 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +3+833 /tmp/tmp.bmp $2 $2

convert -extract 32x8+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +11+825 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +18+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+834 /tmp/tmp.bmp $2 $2

convert -extract 32x8+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +58+826 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +66+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +107+827 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+824 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +113+818 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +109+827 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +157+825 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+824 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +161+818 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +157+827 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+827 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +206+820 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +206+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+825 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +254+820 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +254+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +293+824 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +302+820 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+829 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+827 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +350+820 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +350+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +389+831 /tmp/tmp.bmp $2 $2

convert -extract 32x8+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +395+825 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +398+834 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +435+832 /tmp/tmp.bmp $2 $2

convert -extract 32x8+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +443+825 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +446+834 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+828 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +494+820 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +494+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +534+829 /tmp/tmp.bmp $2 $2

convert -extract 32x8+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+825 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +542+834 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +579+833 /tmp/tmp.bmp $2 $2

convert -extract 32x8+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +586+826 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +589+835 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +641+827 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+824 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +641+818 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +637+826 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +689+828 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+824 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +689+818 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +685+826 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+827 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+825 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+831 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +734+820 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +731+830 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +4+876 /tmp/tmp.bmp $2 $2

convert -extract 32x8+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +11+873 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +6+882 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +59+878 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +62+868 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +59+878 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+880 /tmp/tmp.bmp $2 $2

convert -extract 32x8+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +107+873 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+882 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+874 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +152+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +158+868 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +155+878 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +201+880 /tmp/tmp.bmp $2 $2

convert -extract 32x8+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +203+873 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +200+882 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +246+883 /tmp/tmp.bmp $2 $2

convert -extract 32x8+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +250+874 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+884 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +305+875 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+872 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+878 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +305+866 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +301+874 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +353+875 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+872 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +344+878 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +353+866 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +349+874 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +397+877 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +398+868 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+876 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+877 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +446+868 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+876 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +490+877 /tmp/tmp.bmp $2 $2

convert -extract 32x8+64+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +491+873 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+882 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +543+875 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +542+868 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+878 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +586+878 /tmp/tmp.bmp $2 $2

convert -extract 32x8+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +586+874 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+884 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +641+875 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+872 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+878 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +641+866 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +637+874 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +687+875 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +686+868 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+876 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+876 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+873 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+879 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +734+868 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+876 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +11+922 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +8+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +14+916 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +11+926 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +60+925 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +56+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +62+916 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +59+926 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +108+923 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +104+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +110+916 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +107+925 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +150+919 /tmp/tmp.bmp $2 $2

convert -extract 32x8+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+913 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+925 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +198+919 /tmp/tmp.bmp $2 $2

convert -extract 32x8+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +207+913 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +207+925 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +244+919 /tmp/tmp.bmp $2 $2

convert -extract 32x8+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+913 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+925 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +292+919 /tmp/tmp.bmp $2 $2

convert -extract 32x8+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+913 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+925 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +340+919 /tmp/tmp.bmp $2 $2

convert -extract 32x8+128+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +351+913 /tmp/tmp.bmp $2 $2

convert -extract 8x8+0+480 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +355+924 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +351+925 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +396+914 /tmp/tmp.bmp $2 $2

convert -extract 32x8+0+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+920 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +392+926 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +401+914 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +397+923 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+919 /tmp/tmp.bmp $2 $2

convert -extract 32x8+32+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +446+916 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+288 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +446+926 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+312 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +486+931 /tmp/tmp.bmp $2 $2

convert -extract 32x8+96+256 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+272 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +488+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+280 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +490+922 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+932 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +548+916 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+922 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+928 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +541+914 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +536+922 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +597+917 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+922 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+928 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +589+914 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +584+922 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +636+917 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+922 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+928 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +637+914 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +632+922 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+917 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +681+914 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +678+922 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +725+920 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+921 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+927 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +729+914 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +726+922 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +4+965 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +9+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +9+969 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +50+970 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +53+964 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +59+972 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +100+975 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+464 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +97+966 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +108+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +161+970 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+970 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+976 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +157+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +154+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +209+970 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+970 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+976 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +205+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +202+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +248+966 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +249+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +246+970 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +296+962 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +297+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +294+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +342+960 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +345+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +342+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +397+969 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +393+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +390+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +437+967 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +437+964 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +483+966 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +485+964 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +541+969 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +537+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +534+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+969 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +581+964 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+120+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +628+970 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+969 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+464 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+975 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +625+966 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +628+970 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +689+970 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+970 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+976 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +685+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +737+970 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+970 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+976 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +733+962 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +728+971 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +13+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +9+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +4+1013 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +57+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +53+1012 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+360 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +49+1014 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +109+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +105+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +102+1019 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +153+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +149+1012 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +146+1017 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +205+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +201+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +198+1018 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +249+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +245+1012 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +242+1022 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +293+1018 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+464 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +289+1014 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +288+1022 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +354+1016 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+1018 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+1024 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +349+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+1020 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +402+1016 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+1018 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+1024 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +397+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+168+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+1020 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+1015 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +441+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +435+1016 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +495+1015 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +484+1013 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +539+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+368 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +533+1012 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +530+1017 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +591+1015 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +583+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +585+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +579+1016 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+464 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +631+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +625+1014 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +624+1022 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +690+1016 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+1018 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +679+1024 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +685+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +680+1019 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +735+1015 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+1017 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +727+1023 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +729+1010 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +726+1019 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +15+1063 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +7+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +9+1058 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +4+1061 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +63+1063 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +55+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +57+1058 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +51+1064 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +111+1063 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +103+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +105+1058 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +99+1064 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +159+1063 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +151+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +153+1058 /tmp/tmp.bmp $2 $2

convert -extract 24x24+24+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +150+1066 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +207+1066 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +199+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +203+1057 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +197+1061 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +255+1066 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +247+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +251+1057 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +245+1061 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +303+1066 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +295+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +299+1057 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +289+1064 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +351+1066 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +343+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +347+1057 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +337+1064 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+448 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +399+1066 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+128+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +391+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +395+1057 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +385+1064 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +447+1058 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+304 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+1066 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+456 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +439+1072 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +445+1058 /tmp/tmp.bmp $2 $2

convert -extract 24x24+0+384 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +440+1066 /tmp/tmp.bmp $2 $2

convert -extract 24x24+72+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +492+1058 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+336 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+160+472 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +487+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+376 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +489+1058 /tmp/tmp.bmp $2 $2

convert -extract 24x24+144+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +483+1064 /tmp/tmp.bmp $2 $2

convert -extract 24x24+96+408 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +527+1063 /tmp/tmp.bmp $2 $2

convert -extract 32x8+192+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+1065 /tmp/tmp.bmp $2 $2

convert -extract 32x16+192+464 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +535+1071 /tmp/tmp.bmp $2 $2

convert -extract 24x24+224+400 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +529+1062 /tmp/tmp.bmp $2 $2

convert -extract 24x24+48+432 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +528+1070 /tmp/tmp.bmp $2 $2

convert -extract 1x1+0+0 -transparent black $1 /tmp/tmp.bmp
composite -compose atop -geometry +767+1151 /tmp/tmp.bmp $2 $2

convert -transparent black $2 $2
