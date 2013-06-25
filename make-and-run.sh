#!/bin/sh
python3 ./setup.py install --user
rm -rf ./py_video_reupload.egg-info
rm -rf ./bin
rm -rf ./build 
rm -rf ./dist
clear
~/.local/bin/py_video_reupload $@
