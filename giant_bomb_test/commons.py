import re


def get_terms(text):
    # lower all the text
    text = text.lower()
    # remove unwanted character and replace them by space
    text = re.sub('[^a-z0-9]', ' ', text)
    # split 
    text = text.split()
    # only return words with length>2
    terms =  filter(lambda x: len(x)>=2, text)
    return terms