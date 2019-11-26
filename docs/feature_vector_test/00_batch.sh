rm -rf output/*
python3 01_process_images.py data/images/*.jpg
python3 04_build.py
python3 05_predict.py
python3 -m http.server
