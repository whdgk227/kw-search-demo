import time
import pandas as pd
from soynlp.hangle import jamo_levenshtein
from soynlp.hangle import levenshtein
import sys

target_keyword = sys.argv[1]
out_length = int(sys.argv[2])

# put keyword data
df_RepKeyword = pd.read_excel("../../keyword_table/xlsx/Table_RepKeyword_xlsx.xlsx", header=0)
df_SearchingKeyword = pd.read_excel("../../keyword_table/xlsx/Table_SearchingKeyword_xlsx.xlsx", header=0)
searching_keyword_list = df_SearchingKeyword["searching_keyword"]
sizeSearchingKeyword = searching_keyword_list.shape[0]

def get_scores_dict(searching_keyword_list, target_word):
    distance_dict = {}
    cnt=0
    for searching_keyword in searching_keyword_list:
        distance_dict[cnt] = round(jamo_levenshtein(target_word, searching_keyword), 2)
        if(searching_keyword.startswith(target_word)):
            distance_dict[cnt] = round(distance_dict[cnt]*0.05,3)
        elif(target_word in searching_keyword):
            distance_dict[cnt] = round(distance_dict[cnt]*0.3,3)
        if(searching_keyword==target_word):
            distance_dict[cnt] = 0
        cnt+=1

    return distance_dict

def sort_dict(distance_list):
    return sorted(distance_list.items(), key=lambda item: item[1])

def preprocessing_target_word(target_word):
    return target_word.replace(" ","").lower().replace("-","").replace("*","").replace("_","").replace("!","").replace("@","")

def preprocessing_searching_keyword(searching_keyword_list):
    return searching_keyword_list.str.replace(" ","").str.lower()

def searchKeyword(target_word, searching_keyword_list, out_length = 5, out_msg = False):
    if(out_length > 20):
        print('3rd parameter(out_length) must be under 20!')
        return

    start = time.time()
    output_keyword_list = ['' for _ in range(out_length)]
    output_score_list = ['' for _ in range(out_length)]

    #Preprocessing
    target_word = preprocessing_target_word(target_word)
    searching_keyword_list = preprocessing_searching_keyword(searching_keyword_list)

    #Calculate Score
    distance_dict = get_scores_dict(searching_keyword_list, target_word)

    #Sort Score
    sort_output = sort_dict(distance_dict)

    for i in range(out_length):
        rep_keyword_sn = df_SearchingKeyword["representation_keyword_sn"][sort_output[i][0]]
        output_keyword_list[i] = df_RepKeyword[df_RepKeyword["representation_keyword_sn"]==rep_keyword_sn].iloc[0]["representation_keyword"]
        output_score_list[i] = sort_output[i][1]

    # print results
    if (out_msg):
        print("Target Word : ", target_word)
        for i in range(out_length):
            print("searching_keyword_sn : ", sort_output[i][0], ", score : ", sort_output[i][1], ", Rep_keyword : ", output_keyword_list[i])

        print(f"소요시간: {time.time() - start:.4f}")
    return output_keyword_list, output_score_list

searchKeyword(target_keyword, searching_keyword_list, out_length, out_msg=True)
