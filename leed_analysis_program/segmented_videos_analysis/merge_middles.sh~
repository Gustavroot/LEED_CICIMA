#!/bin/bash

#Part of the idea and code in this script was taken from a script written by Philip Klaus,
#check <https://gist.github.com/4572552> for newer versions

cd ./frames_replicate/
set -x

FRAMERATE=24

ffmpeg -framerate 0.5000 -start_number 1 -i img_%05d.JPG -vf fps=24 -qscale 1 output.wmv

mv output.wmv ../
cd ../
rm -R ./frames/
rm -R ./frames_replicate/
