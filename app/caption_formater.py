import re
def extract_hash_tags(s):
    return list(set(part[1:] for part in s.split() if part.startswith('#')))

def remove_hash_tags(s):
    s = re.sub("([^A-Za-z0-9]+#|^#)"," #",s)
    return ' '.join(re.sub(" #[A-Za-z0-9_]+"," ",s).split())

def deEmojify(inputString): #remove emojis
    if(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')
    return ''
