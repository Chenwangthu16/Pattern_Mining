#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 1 13:45:12 2018

@author: chen
"""

def getFrequent_1_Itemset(contents,min_support):
    '''
    input:  original input data
    output: 
        1. a list of set with all frequent 1 items
        2. a dict with the support of each item
        3. reformated data set.
    '''
    #read support
    dict_all_items = {}
    t_data = []
    for i in range(len(contents)):
        items = contents[i].split()
        t_data.append(items)
        for item in items:
            if item not in dict_all_items:
                dict_all_items[item] = 1
            else:
                dict_all_items[item] +=1
    #find frequent ones           
    
    dict_freq_itemsets = dict((k, v) for k, v in dict_all_items.items() if v >= 2)
    #dict_freq_itemsets = dict()
    #for item in dict_all_items:
    #   if dict_all_items[item]>=min_support:
    #        dict_freq_itemsets[item] = dict_all_items[item]

    #item_set = [[item] for item in list(dict_freq_itemsets.keys())]
    return dict_freq_itemsets, t_data
#dict_freq_itemsets, item_set,t_data = getFrequent_1_Itemset(contents,2)
    
def generateFre_2_itemset(dict_freq_itemsets,t_data):
    '''
    frequent k+1 item sets must meet the following requirements:
        1. adjacent to frequent k - itemsets.  (the first k items must be frequent)
        2. new item added must be frequent.
        e.g.   [a,b, c]:  [a,b] is frequent, c is also frequent. 
    '''
    dict_fre_2_items = {}
    #freq_2_itemset = []
    for line in t_data:
        for i,item in enumerate(line):
            if item in dict_freq_itemsets:#if a item is frequent
                #check if its next is frequent:
                if (i < len(line)-1) and (line[i+1] in dict_freq_itemsets):
                    key = getCombinedKey([item, line[i+1]])
                    if key not in dict_fre_2_items:
                        #freq_2_itemset.append([item, line[i+1]])
                        dict_fre_2_items[key]  = 1
                    else:
                        dict_fre_2_items[key]  +=1
    dict_fre_2_items = dict((k, v) for k, v in dict_fre_2_items.items() if v >= 2)
    #freq_2_itemset  = [key.strip().split() for key in dict_fre_2_items.keys()]
    return dict_fre_2_items
                    
def generateFre_k_itemset(dict_freq_1_itemsets,dict_freq_itemsets,t_data,k):
    '''
    frequent k item sets must meet the following requirements:
        1. adjacent to frequent k-1  itemsets.  (the first k-1 items must be frequent)
        2. new item added must be frequent.
        e.g.   [a,b, c]:  [a,b] is frequent, c is also frequent. 
    input: 
        dict_freq_1_itemsets: frequent 1 item set
        dict_freq_itemsets: frequent k-1 item set
        length: k
    
    '''
    dict_fre_k_items = {}
    #freq_2_itemset = []
    for line in t_data:
        for i,item in enumerate(line):
            if getCombinedKey(line[i:i+k-1]) in dict_freq_itemsets:#if the k-1 length item is frequent
                #check if its next is frequent:
                if (i < len(line)-k+1) and (line[i+k-1] in dict_freq_1_itemsets):
                    key = getCombinedKey(line[i:i+k-1] + [line[i+k-1]])
                    if key not in dict_fre_k_items:
                        #freq_2_itemset.append([item, line[i+1]])
                        dict_fre_k_items[key]  = 1
                    else:
                        dict_fre_k_items[key]  += 1
    dict_fre_k_items = dict((k, v) for k, v in dict_fre_k_items.items() if v >= 2)
    #freq_k_itemset  = [key.strip().split() for key in dict_fre_k_items.keys()]
    return dict_fre_k_items               


def Apriori(contents,min_support):
    '''
    '''
    #get frequent 1 item sets
    dict_freq_1_itemsets,t_data = getFrequent_1_Itemset(contents,min_support)
    #get frequent 2 item sets
    
    dict_freq_2_itemsets = generateFre_2_itemset(dict_freq_1_itemsets,t_data)
    t_dict = {**dict_freq_2_itemsets}
    #get frequent 3,4,5 item sets
    current_dict = dict_freq_2_itemsets
    for i in range(3,6):
        new_dict = generateFre_k_itemset(dict_freq_1_itemsets,current_dict,t_data,i)
        t_dict.update(new_dict)
        current_dict = new_dict
    return t_dict

def getCombinedKey(pattern):
    '''
    pattern: a list of items. if more than 1, combien them as key of a dictionary.
    '''
    newKey = ''
    for item in pattern:
        newKey += (str(item) + ' ')
    return newKey

def sorted_itemset(dict_freq_itemsets):
    #get the sorted frequent itemsets
    sorted_key = [v[0] for v in sorted(dict_freq_itemsets.items(), key=lambda x: (-x[1],x[0]))     ]
    return sorted_key


if __name__ ==   '__main__':
    #read data from stdin

    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    min_support = 2
    t_dict = Apriori(contents,min_support)
    sorted_key = sorted_itemset(t_dict)
    #print
    i = 0
    for key in sorted_key:
        i+=1
        if i >= 21:
            break
        print("["+ str(t_dict[key]) + ", '" + key.strip() +"']")