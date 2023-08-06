     
def word_count(word_list):
    wordCount = {}
    for word in word_list:
        wordCount[word] = wordCount.get(word, 0) + 1
        sorted_dict = sorted(wordCount.items(), key=lambda x: x[1], reverse=True)
    return sorted_dict

def co_occurence_count(word_lst):
    co_dic = {}
    for i,a in enumerate(word_lst):
        #for b in word_lst[i+1:i+11]:
        for b in word_lst[i+1:]:
            if a == b: continue
            #print(i,a,b)
            if a > b: c, d = b, a
            else: c, d = a, b
            co_dic[c, d] = co_dic.get((c, d), 0) + 1
    return co_dic

def extract_window(lst, kwd, window=5):
    wpairs = []    

    print(lst)
    if kwd in lst:
        locs = [i for i, word in enumerate(lst) if word in kwd]
        last = len(lst)-1

        ext_pairs = []
        pairs = []; 
        for loc in locs:
            pair = (max(0,loc-window),min(loc+(window), last)) # before and after n words
            pairs.append(pair)
            
            for begin, end in sorted(pairs): # merge ranges overlap
                if ext_pairs and ext_pairs[-1][1] > begin - 1: ext_pairs[-1][1] = max(ext_pairs[-1][1], end)
                else: ext_pairs.append([begin, end])

        for ext_pair in ext_pairs:
            p = lst[ext_pair[0]:(ext_pair[1]+1)]
            #rgs = [str(ext_pair[0]), str(ext_pair[1])]
            wpairs.append(p)

    return wpairs
