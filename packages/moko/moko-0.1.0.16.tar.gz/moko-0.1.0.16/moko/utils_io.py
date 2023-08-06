from collections import defaultdict

import csv

def character_reader(character_file_path):
    character_list = []
    with open(character_file_path, 'r', encoding = 'utf-8') as character_file:
        while True:
            line = character_file.readline().replace('\n', '')
            if not line: break
            character_list.append(line)
        return character_list

def term_reader(term_extra):
    term_extra_dic = defaultdict(list)
    for line in csv_file_reader(term_extra):
        term_extra_dic[line[0]] = line[1]
    return term_extra_dic

def list_reader(file_path, header = True):
    filereader = csv_file_reader(file_path)
    if header:
        lst = [line[1] for line in filereader if len(line[1]) > 1] #line[1]:concept
    else:
        lst = [line for line in filereader]
        lst = sum(lst, [])
    return lst

def file_reader(file_path):
    f = open(file_path, 'r', encoding = 'utf-8')
    return f
    
def file_writer(file_path):
    f = open(file_path, 'w', encoding = 'utf-8')
    return f

def csv_file_reader(file_path):
    csv_file_reader = open(file_path, 'r', newline='', encoding = 'utf-8')
    filereader = csv.reader(csv_file_reader)
    next(filereader)
    return filereader

def csv_file_writer(file_path):
    f = open(file_path, 'w', newline='', encoding = 'utf-8')
    csvwriter = csv.writer(f)
    return csvwriter
