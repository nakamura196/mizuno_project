rm -rf output/*
python 01_process_images.py data/images/*.jpg
python 04_build.py
python 05_predict.py
python3 -m http.server
