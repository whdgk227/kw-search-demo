import sys
import time

import pandas as pd

from soynlp.hangle import jamo_levenshtein
from soynlp.hangle import levenshtein


def get_scores_dict(searching_keyword_list, target_word):
    distance_dict = {}
    cnt=0
    for searching_keyword in searching_keyword_list:
        if target_word in searching_keyword:
            if searching_keyword==target_word:
                distance_dict[cnt] = 0
            elif searching_keyword.startswith(target_word):
                distance_dict[cnt] = round(jamo_levenshtein(target_word, searching_keyword)*0.01,3)
            else:
                distance_dict[cnt] = round(jamo_levenshtein(target_word, searching_keyword)*0.1,3)
        # elif abs(len(target_word) - len(searching_keyword)) < 5:
            # distance_dict[cnt] = round(jamo_levenshtein(target_word, searching_keyword),3)
        else:
            pass
        cnt += 1

    return distance_dict

def get_scores_dict_dist(searching_keyword_list, target_word):
    distance_dict = {}
    cnt=0
    for searching_keyword in searching_keyword_list:
        if abs(len(target_word) - len(searching_keyword)) <= 5:
            distance_dict[cnt] = round(levenshtein(target_word, searching_keyword)*weight_including(target_word, searching_keyword),3)
        else:
            pass
        cnt += 1

    return distance_dict

def weight_including(target_word, searching_keyword):
    including_cnt = 0
    len_target_word = len(target_word)
    for i in range(len_target_word):
        if (target_word[i] in searching_keyword):
            including_cnt += 1
    return 0.1+0.9*((len_target_word-including_cnt) / (len_target_word))



def sort_dict(distance_list):
    return sorted(distance_list.items(), key=lambda item: item[1])

def preprocessing_target_word(target_word):
    return target_word.replace(" ","").lower().replace("-","").replace("*","").replace("_","").replace("!","").replace("@","").replace("/","")

def preprocessing_searching_keyword(searching_keyword_list):
    return searching_keyword_list.str.replace(" ","").str.lower()

def searchKeyword(target_word, searching_keyword_list, df_RepKeyword, df_SearchingKeyword, out_length = 5,  out_msg = False, debug=False):
    if(out_length > 20):
        print('3rd parameter(out_length) must be under 20!')
        return

    start = time.time()
    length_result = 0
    output_keyword_list = ['' for _ in range(out_length+1)]
    output_score_list = ['' for _ in range(out_length)]
    output_keyword_sn_list = ['' for _ in range(out_length)]
    output_searching_keyword_sn_list = ['' for _ in range(out_length)]

    #Preprocessing
    target_word = preprocessing_target_word(target_word)
    searching_keyword_list = preprocessing_searching_keyword(searching_keyword_list)
    if debug:
        time_pre = time.time()
        print("pre:", time_pre-start)

    #Calculate Score
    distance_dict = get_scores_dict(searching_keyword_list, target_word)
    print(len(distance_dict))
    if(len(distance_dict)<1):
        distance_dict = get_scores_dict_dist(searching_keyword_list, target_word)

    #Sort Score
    sort_output = sort_dict(distance_dict)

    for i in range(len(sort_output)):
        if (length_result >= out_length):
            break
        rep_keyword_sn = df_SearchingKeyword["representation_keyword_sn"][sort_output[i][0]]
        if (rep_keyword_sn in output_keyword_sn_list):
            continue
        output_searching_keyword_sn_list[length_result] = df_SearchingKeyword["searching_keyword"][sort_output[i][0]]
        output_keyword_list[length_result] = df_RepKeyword[df_RepKeyword["representation_keyword_sn"]==rep_keyword_sn].iloc[0]["representation_keyword"]
        output_keyword_sn_list[length_result] = rep_keyword_sn
        output_score_list[length_result] = sort_output[i][1]
        length_result+=1

    # print results
    if (out_msg):
        print("Target Word : ", target_word)
        for i in range(out_length):
            print("Rep_keyword : ", output_keyword_list[i], ", searching keyword : ", output_searching_keyword_sn_list[i], ", score : ", output_score_list[i], ", rep_keyword_sn : ", output_keyword_sn_list[i])

        print(f"소요시간: {time.time() - start:.4f}")
    output_keyword_list[-1] = f"검색 시간 : {time.time() - start:.4f}"
    return output_keyword_list#, output_score_list

def searchKeywordFunction(target_keyword: str, out_length: int, df_RepKeyword, df_SearchingKeyword)->tuple:
    # df_RepKeyword = pd.read_excel("./keyword_table/xlsx/Table_RepKeyword_xlsx.xlsx", header=0)
    # df_SearchingKeyword = pd.read_excel("./keyword_table/xlsx/Table_SearchingKeyword_xlsx.xlsx", header=0)
    searching_keyword_list = df_SearchingKeyword["searching_keyword"]
    sizeSearchingKeyword = searching_keyword_list.shape[0]
    return tuple(searchKeyword(target_keyword, searching_keyword_list, df_RepKeyword=df_RepKeyword, df_SearchingKeyword=df_SearchingKeyword, out_length=out_length, out_msg=True, debug=False))
