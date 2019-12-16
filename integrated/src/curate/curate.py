import curate_images
import create_curation
import os

if __name__ == "__main__":
    hojo_name = "泉州本淳化閣帖 八 [A006099-05]"
    characterIsBlack = False

    if not os.path.exists("../../output/{}/curated_lines".format(hojo_name)):
        os.mkdir("../../output/{}/curated_lines".format(hojo_name))

    create_curation.create_curation(hojo_name, characterIsBlack)
    #curate_images.curate_images(hojo_name)
