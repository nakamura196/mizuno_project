import collection2list
import get_json

colle = collection2list.collection2list()
for col in colle:
    get_json.get_json(col["url"], col["label"])
