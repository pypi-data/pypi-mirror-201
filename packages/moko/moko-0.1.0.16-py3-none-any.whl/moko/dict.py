import hanja

def stopword_remove(word_lst, stopword_lst):
    lst = []
    for w in word_lst:
        if w in stopword_lst: continue
        else: lst.append(w)
    return lst

def adverb_remove(word_lst, adverb_lst):
    lst = []
    for w in word_lst:
        translated = hanja.translate(w,'substitution')
        if translated in adverb_lst: continue
        else: lst.append(w)
    return lst
