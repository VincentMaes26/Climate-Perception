import datetime
import json

if __name__ == "__main__":
    list1 = ["hfkdlsmj jkflqsmjd", "global warming fhdklsqmf ff climate change", "jfklsdqm"]

    keywords = []
    for item in list1:
        if "global warming" in item and "climate change" in item:
            keywords.append(item)
    

    keywords = list(filter(None,keywords))

    print(keywords)