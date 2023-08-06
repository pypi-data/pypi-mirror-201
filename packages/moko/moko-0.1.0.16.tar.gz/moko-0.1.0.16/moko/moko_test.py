# -*- coding: utf-8 -*-
import moko.noun_chunker as nc
import moko.term_analyzer as ta

def moko_demo():
    text = "泱泱大風이 固由於萬籟齊應이나 其初也엔 起於一蓬之末고 彼文明國之所謂 文明이 固謂其國民全軆之文明이나 其文明開發之原動力은"

    dct_lst = nc.noun_chunk_dict(text,char_num=4)
    print("=== noun list with a dictionary ===")
    print(dct_lst)

    mdl_lst = nc.noun_chunk_model(text)
    print("=== noun list with a model ===")
    print(mdl_lst)
    
    win = ta.extract_window(dct_lst,"文明",2)
    print(win)
    win = ta.extract_window(mdl_lst,"文明",2)
    print(win)

moko_demo()