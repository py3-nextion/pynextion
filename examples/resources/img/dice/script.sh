#!/usr/bin/env bash
for i in {0..6}
do
   #svgexport $i.svg $i.png 135x135
   convert -density 1200 -resize 135x135 $i.svg $i.png
   #convert temp_$i.png -size 200,135 -rotate 90 +append $i.png
done
#rm temp_*.png
