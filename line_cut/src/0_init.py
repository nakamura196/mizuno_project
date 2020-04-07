import urllib.request
import json
import os
import time
import sys
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from statistics import mean
from PIL import Image, ImageFilter
import numpy as np
from scipy import signal
import hashlib

#場所の準備
if not os.path.exists("../input"):
    os.makedirs("../input")
if not os.path.exists("../input/collection"):
    os.makedirs("../input/collection")
if not os.path.exists("../input/manifest"):
    os.makedirs("../input/manifest")
if not os.path.exists("../input/images"):
    os.makedirs("../input/images")
if not os.path.exists("../output"):
    os.makedirs("../output")
