import datetime
import json
import hashlib

if __name__ == "__main__":
    list1 = ["hfkdlsmj jkflqsmjd", "global warming fhdklsqmf ff climate change", "jfklsdqm"]


    keywords = []
    for item in list1:
        if "global warming" in item and "climate change" in item:
            keywords.append(item)
    

    keywords = list(filter(None,keywords))

    hashed = hashlib.md5(str(list1[1]).encode('utf-8')).hexdigest()
    print(datetime.datetime.now())
