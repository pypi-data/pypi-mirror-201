import unicodedata
import re
import hanja

import moko.configure as con

cp_path = con.CHARACTER_PATH
num_char = con.NUM_CHAR_LIST
prefix = con.PREFIX_LIST
exp_noun = con.EXCEPTION_WORD_LIST
counter_noun = con.COUNT_NOUN_LIST
last_char = con.LAST_CHAR_LIST
demon_noun = con.DEMON_WORD_LIST

def pre_processing(text):
    text = re.sub('[▣◎△◆△◆.,「」『』【】{}〔〕(/)▲◇▼●○"]', ' ', text)
    text = re.sub('[、]', ' ', text)
    text = text.strip().replace('\n', ' ')
    return text

def load_dict():
    character_pair = {}
    with open(cp_path, 'r', encoding = 'utf-8') as character_file:
        while True:
            line = character_file.readline().replace('\n', '')
            if not line: break
            pair_list = line.split('\t')
            old_character = pair_list[0]
            new_character = pair_list[1]
            character_pair[old_character] = new_character
    return character_pair

def unicode_normalize(text, character_pair={}):
    for char in text:
        n_char = unicodedata.normalize('NFC',char) 
        text = text.replace(char,n_char)
        if char in character_pair.keys():
            text = text.replace(char, character_pair[char])
    return text

def num_word_check(word):
    cnt = 0
    word_length = len(word)
    is_num_word, is_skip = False, False
    for char in word:
        if char in num_char : cnt += 1
    if word_length == cnt : is_num_word = True

    for c in prefix:
        if word_length > 1 and word.startswith(c) and word_length-1 == cnt: is_skip = True 

    for c in counter_noun:
        if word_length > 1 and word.endswith(c) and word_length-1 == cnt: is_skip = True
    
    return is_num_word, is_skip, cnt

def prefix_remove(word):
    cnt = 1
    is_measure, is_num = False, False
    for s in prefix:
        if word.startswith(s): is_measure = True
    
    for char in word[1:]:
        if is_measure and char in num_char: 
            is_num = True
            cnt+=1
        else:
            is_num = False
            if is_measure and is_num==False: word = word[cnt-1:]
            continue
    return word

def date_check(word, cnt):
    word_length = len(word)
    is_date, is_year = False, False
    regex_lst = ['\w{2,4}年\w{1,3}月\w{1,3}日$', '\w{1,3}月\w{1,3}日$', '\w{1,4}年\w{1,3}月$']
    for regex in regex_lst:
        r = re.compile(regex)
        m = r.match(word)
        if m: is_date = True
    for char in last_char: # exception word
        if word_length > 1 and word.endswith(char) and (word_length-1 == cnt) and word not in exp_noun : is_year = True
    return is_date, is_year

def last_char_remove(word):
    word_length = len(word)
    for char in last_char: # exception word
        if word_length > 2 and (word.endswith(char) and word not in exp_noun): word = word[:-1]
    return word

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
