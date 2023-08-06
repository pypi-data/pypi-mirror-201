from hanja import hangul
from hanja import split_hanja

from soyspacing.countbase import RuleDict
from soyspacing.countbase import CountSpace

import moko.processor as processor
import moko.configure as con

#from moko.dict import stopword_remove,adverb_remove
from moko.utils_io import list_reader

adv_path = con.ADVERB_PATH
stw_path = con.STOPWORD_PATH
cpt_path = con.CONCEPT_NOUN_PATH
usr_path = con.USER_DICT_PATH

concept_lst = list_reader(cpt_path)
adverb_lst = list_reader(adv_path, False)
stopword_lst = list_reader(stw_path, False)
usrword_lst = list_reader(usr_path, False)

model = CountSpace()
model.load_model(con.SPACING_MODEL_PATH, json_format=False)
rule_dict = RuleDict(con.SPACING_RULE_PATH)

def noun_chunk_dict(text, stopword_lst=stopword_lst, usrword_lst=usrword_lst, char_num = 4):
    lst = []
    uni = processor.load_dict()

    line = processor.pre_processing(text)
    line = processor.unicode_normalize(line,uni)

    word_list = hanja_text_to_list(line)
    for word in word_list:
        word_length = len(word)
        word = word.replace('\n', '').replace(' ', '').replace(',','')
        
        is_all_hanja = True
        for char in word:
            if hangul.is_hangul(char): is_all_hanja = False
            
        is_num_word, is_skip, cnt = processor.num_word_check(word)
        if is_num_word or is_skip: continue
        is_date, is_year = processor.date_check(word, cnt)
        if is_date or is_year: continue
        
        word = processor.last_char_remove(word)
        word = processor.prefix_remove(word)
        
        if is_all_hanja and word_length > 1 and word.isalpha()== True: 
            if word_length > char_num: # long word
                '''
                sent_corrected, tags = model.correct(word, rules=rule_dict) # soyspacing 모델, space_rule을 적용
                candidate = [w for w in sent_corrected.split() if len(w) > 1]
                '''
                cnt_cnd = long_word_processing(word, concept_lst) # list mapping for concept word
                lst.extend(cnt_cnd)
                usr_cnd = long_word_processing(word, usrword_lst)
                lst.extend(usr_cnd)
            else: 
                lst.append(word)

    #adverb_lst = list_reader(adv_path, False)
    #stopword_lst = list_reader(stw_path, False)
    
    lst = processor.stopword_remove(lst, stopword_lst)
    lst = processor.adverb_remove(lst, adverb_lst)

    return lst

def noun_chunk_model(text, stopword_lst=stopword_lst, char_num = 4):
    lst = []
    uni = processor.load_dict()

    line = processor.pre_processing(text)
    line = processor.unicode_normalize(line,uni)

    word_list = hanja_text_to_list(line)
    for word in word_list:
        word_length = len(word)
        word = word.replace('\n', '').replace(' ', '').replace(',','')
        
        is_all_hanja = True
        for char in word:
            if hangul.is_hangul(char): is_all_hanja = False
            
        is_num_word, is_skip, cnt = processor.num_word_check(word)
        if is_num_word or is_skip: continue
        is_date, is_year = processor.date_check(word, cnt)
        if is_date or is_year: continue
        
        word = processor.last_char_remove(word)
        word = processor.prefix_remove(word)
        
        if is_all_hanja and word_length > 1 and word.isalpha()== True: 
            if word_length > char_num: #긴 단어 처리
                sent_corrected, tags = model.correct(word, rules=rule_dict) # soyspacing 모델, space_rule을 적용
                candidate = [w for w in sent_corrected.split() if len(w) > 1]
                candidate = [processor.prefix_remove(cnd) for cnd in candidate]
                lst.extend(candidate)
            else: lst.append(word)
    
    #adverb_lst = list_reader(adv_path, False)
    #stopword_lst = list_reader(stw_path, False)

    lst = processor.stopword_remove(lst, stopword_lst)
    lst = processor.adverb_remove(lst, adverb_lst)

    return lst

def long_word_processing(word, concept_lst=concept_lst):
    candidate, rm_lst = [], []
    for concept in concept_lst:
        if concept in word: candidate.append(concept)
    candidate.sort(key=len)
    length = len(candidate)
    for i in range(0, length-1):
        for j in range(i+1, length):
            if candidate[j].startswith(candidate[i]):rm_lst.append(candidate[i])
            elif candidate[j].endswith(candidate[i]):rm_lst.append(candidate[i])
    for remove_word in set(rm_lst):
        candidate.remove(remove_word)
    return candidate

def hanja_text_to_list(line):
    is_all_hanja = True
    for char in line: 
        if hangul.is_hangul(char): is_all_hanja = False
    if is_all_hanja : #모두 한자, 띄어쓰기가 있는 경우: 띄어쓰기로 쪼갬
        all_hanja = [word for word in line.split() if len(word) > 1]
        hanja_list = all_hanja
    else:             #국한문혼용, 한글로 된 부분과 한자로 된 부분을 분리
        words_list = [word for word in split_hanja(line) if len(word) > 1]
        hanja_list = words_list
    return hanja_list
