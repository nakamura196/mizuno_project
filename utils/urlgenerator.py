import sys
import webbrowser

original_url = sys.argv[1]
curation     = original_url.lstrip("https://github.com/nakamura196/mizuno_project/blob/master/docs/curation/")
curaView_url = "http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation=https://raw.githubusercontent.com/nakamura196/mizuno_project/master/docs/curation/{}&mode=annotation&lang=ja".format(curation)

browser = webbrowser.get("open -a /Applications/Google\ Chrome.app %s")
browser.open_new(curaView_url)
