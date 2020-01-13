import curate_images
import create_curation
import junkakaku_curation
import os

if __name__ == "__main__":
    hojo_list = ["泉州本淳化閣帖 八 [A006099-05]", "偽絳帖 三 [A005936-03]", "淳化閣帖第1-10。[8]", "星鳳楼帖 卯 [A005935-04]", "淳化閣帖"]
    characterIsBlack = False


    for hojo_name in hojo_list:
        if hojo_name != "淳化閣帖第1-10。[8]":
            continue
        if not os.path.exists("../../output/{}/curated_lines".format(hojo_name)):
            os.mkdir("../../output/{}/curated_lines".format(hojo_name))
        if not os.path.exists("../../../docs/akaze_search/{}".format(hojo_name)):
            os.mkdir("../../../docs/akaze_search/{}".format(hojo_name))

        create_curation.create_curation(hojo_name, characterIsBlack)
        #if hojo_name == "淳化閣帖":
        curate_images.curate_images(hojo_name)
        #junkakaku_curation.create_curation("淳化閣帖第1-10。[8]")
