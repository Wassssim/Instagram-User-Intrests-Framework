import re

dataset = {}

def extract_hash_tags(s):
    return list(set(part[1:] for part in s.split() if part.startswith('#')))

def remove_hash_tags(s):
    return ' '.join(re.sub(" #[A-Za-z0-9_]+"," ",s).split())


test = "qdqsd #xDDD #xdqsd_qsdqs aeaze#123eaze"

print("Hashtags only: "+str(extract_hash_tags(test)))
print("Without hashtags: "+remove_hash_tags(test))



#Problems:
#high_res image always available?
#hash tag functions testing