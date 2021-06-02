import time
import json
from sys import path_importer_cache, stderr
import nltk
import re
from nltk.sem.logic import QuantifiedExpression
from urllib.parse import urlparse

from nltk.data import load

def load_index() -> dict: # load the index into a dict
    with open('D:\Codes\CS121\indexes_test_ver2.json', 'r') as j:
        dict_index = json.load(j)
    return dict_index

def load_doc_id_dict() -> dict:
    with open('D:\Codes\CS121\doc_id_ver2.json', 'r') as d:
        doc_id_dict = dict(json.load(d))
    return doc_id_dict

def load_word_count_dict():
    with open('D:\Codes\CS121\word_count_page_ver2.json') as d:
        word_count_dict = dict(json.load(d))
    return word_count_dict

def get_url(doc_id_dict, doc_id) -> str: # pass in a doc_id and give you the corresponding url
    print("    doc_id: ", doc_id)
    return doc_id_dict[doc_id]

def get_query() -> list: # split and stem the query into a list of string
    query = input("Search(enter nothing to quit): ")
    if query == '':
        exit()
    list_query = re.split(pattern=r'\W+', string=query)
    stemmer = nltk.PorterStemmer()
    stemmed_query = [stemmer.stem(token) for token in list_query if token != '']
    return stemmed_query

def get_id2ind(index, lst_ovlp, query_list):
    dict_id2ind = dict()
    for id in lst_ovlp:
        lst_ind = []
        for q in query_list:
            lst_ind.append(index[q][str(id)][1]) # this will get the index list in the posting
        dict_id2ind[id] = lst_ind
    return dict_id2ind

def get_phrase_count(dict_id2ind):
    phrase_count_dict = dict()
    for k in dict_id2ind: # k is the doc id
        phrase_count = len(dict_id2ind[k][0])
        for i in range(len(dict_id2ind[k])):
            if i == 0:
                word_ind = dict_id2ind[k][0]
            else:
                for ind in word_ind:
                    if ind+1 not in dict_id2ind[k][i]:
                        phrase_count -= 1
                        break
        phrase_count_dict[k] = phrase_count
    return phrase_count_dict

def filter_url(q, doc_id_lst, doc_id_dict):
    url_set = set()
    lst_dup = []
    for doc_id in doc_id_lst:
        p = urlparse(doc_id_dict[doc_id])
        if p.netloc+p.path not in url_set:
            url_set.add(p.netloc+p.path)
        else:
            lst_dup.append(doc_id)
    return [id for id in doc_id_lst if id not in lst_dup]
            
        

def searching(index, doc_id_dict, query_list, word_count_dict): # this is where the actual searching is happening
    start_time = time.time()
    lst_all_words = []
    search_result = [] # list of doc ids
    # search machine learning
    # step1. find list of doc_id that contains both machine and learning.
    # step2. for each doc_id, for the ind_list in the index, count how many machine ind+1 is in learning ind list.
    # step3. based on the count you got, calculate tf-idf score.
    for q in query_list[:]:
        if q in index:
            lst_all_words.append([int(doc_id) for doc_id in index[q].keys()])
        else:
            query_list.remove(q)
    if len(query_list) == 0:
        print('No record')
        return
    lst_ovlp = lst_all_words[0]
    for i in range(len(lst_all_words)):
        lst_ovlp = list(set(lst_ovlp) & set(lst_all_words[i]))
    # we now have the overlapping doc_ids list
    #step2.
    dict_id2ind = get_id2ind(index, lst_ovlp, query_list)
    phrase_count = get_phrase_count(dict_id2ind)
    search_result = sorted([doc_id for doc_id in phrase_count], key=lambda x: (phrase_count[x]/word_count_dict[x]*(55394/len(list(phrase_count.keys()))) * index[query_list[0]][str(x)][0]),reverse=True)
    search_result = filter_url(query_list[0], search_result, doc_id_dict)
    for doc_id in search_result[:5]:
        print('Search found @:', get_url(doc_id_dict, doc_id))
        #print(word_count_dict[doc_id])
    
    print('Search used', time.time()-start_time,'to execute.')
    
    


def run():
    dict_index = load_index()
    doc_id_dict = load_doc_id_dict()
    word_count_dict = load_word_count_dict()
    while True:
        searching(dict_index, doc_id_dict, get_query(),word_count_dict)

if __name__ == '__main__':
    print('--------\nThis is a skeleton of the search.\nIt will give you the top ranking document for the word(s) you entered.\nAdjust the path of index and path to doc id accordingly\n--------\n')
    run()

# Structure of the index posting:
            # {token: [doc_id, td_idf_scoring]}

            #                           I   eat   apple
            #document tf_idf : doc1:   0.3  0.1   0.2
            # q tf_idf                 0.3  0.3   0.3
