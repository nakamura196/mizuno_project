import os
import get_iiif_images
import manifest2info

info = manifest2info.manifest2info("淳化閣帖第1-10。[8]")
get_iiif_images.get_iiif_images(info, "淳化閣帖第1-10。[8]")
