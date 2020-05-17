import re

dataset = {}

def extract_hashtags(s):
    return list(set(part[1:] for part in s.split() if part.startswith('#')))

def remove_hashtags(s):
    #s = re.sub("([^A-Za-z0-9]+#|^#)"," #",s)
    s = str(s)
    return ' '.join(re.sub("#.*?(?=\s|$)","", s).split())
    #return ' '.join(re.sub(" #[A-Za-z0-9_]+"," ",s).split())

if __name__=="__main__":
    test = "#qdqsd #xDDD #xdqsd_qsdqs aeaze.#123eaze"

    print("Hashtags only: "+str(extract_hash_tags(test)))
    print("Without hashtags: "+remove_hash_tags(test))



#Problems:
#high_res image always available?
#hash tag functions testing