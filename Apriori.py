#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 21:08:27 2018

@author: chen
A simple Apriori algorithm for:
    mining frequent patterns
    finding closed patterns
    finding maximal patterns

No extra packages used. 
Able to take care of all transctions that can be transformed into a string, with following input requirements.
input requirements: 
    stdin input per HW requirement.
    first line is min support
    each following line is a item set. Different items in a set is seperated by a space. (This is required in this code)
Output:
    print frequent patterns sorted by support and then alphabetically
    print closed patterns
    print maximal patterns
"""
           

def getFrequent_1_Itemset(contents):
    '''
    input:  original input data
    output: 
        1. a list of set with all frequent 1 items
        2. a dict with the support of each item
        3. transccation data reformated.
    '''
    #read support
    min_support = int(contents[0])
    dict_all_items = {}
    t_data = []
    for i in range(1, len(contents)):
        items = contents[i].split()
        t_data.append(set(items))
        for item in items:
            if item not in dict_all_items:
                dict_all_items[item] = 1
            else:
                dict_all_items[item] +=1
    #find frequent ones           
    dict_freq_itemsets = dict()
    for item in dict_all_items:
        if dict_all_items[item]>=min_support:
            dict_freq_itemsets[item] = dict_all_items[item]
    
    item_set = set(dict_freq_itemsets)
        
    return dict_freq_itemsets, list(item_set), t_data

def getCombinedKey(itemset):
    '''
    A set of string and a combinaiton of strings are transformed in this function:
    e.g. ['patterA','patternB','patternA patternB']<--> [{'patterA'},{'patternB'},{'patternA', 'patternB'}]
    Idea is to enable storing pattern in the key of a dict
    
    input: Itemset: a set of length k,k>1, containing several frequent items
    return:  a string that represent the pattern to store in dict
    '''
    new_key = ''
    for item in sorted(itemset): #alphabetaic order
        if len(new_key) == 0:
            new_key += str(item)
        else:
            new_key += (' '+ str(item))
    return new_key

def CreateNewSet(item_set, length):
    '''
    generate length+1 itemset based on current itemset.
    '''
    new_itemset = []
    for i in range(len(item_set)):
        for j in range(len(item_set)):
            if i != j :
                if type(item_set[i]) == str:
                    set_1 = set([item_set[i]])
                if type(item_set[i]) == set:
                    set_1 = set(item_set[i])
                if type(item_set[j]) == str:
                    set_2 = set([item_set[j]])
                if type(item_set[j]) == set:
                    set_2 = set(item_set[j])
                temp_set = set_1.union(set_2)
                #temp_set = set([item_set[i]]).union(set([item_set[j]]))
                if (len(temp_set) == length) and (temp_set not in new_itemset):
                    new_itemset.append(temp_set)
    return new_itemset  


def getFrequentItemset(generated_itemset,min_support,t_data ):
    '''
    return frequent items from generated itemset
    input: itemset with all generated items
    output: dict of frequent itemset
            frequent itemset
    '''
    dict_ = {}
    dict_freq = {}
    freq_itemset_list = []
    for item in generated_itemset:
        itemset_key = getCombinedKey(item)
        for record in t_data:
            if item.issubset(record): #if contains the pattern:
                if itemset_key in dict_:
                    dict_[itemset_key] +=1
                else:
                    dict_[itemset_key] = 1
                    
    #keep only frequent ones
    for key in dict_:
        if dict_[key]>=min_support:
            dict_freq[key]  = dict_[key]
    #print(dict_freq)
    #generate a list of set containing frequent patterns:
    for key in dict_freq:
        freq_itemset_list.append(set(key.split()))
    
    return dict_freq,freq_itemset_list

########################
#main Apriori algorithm
#######################
def Apriori(contents):
    '''
    main function
    find frequent patterns
    '''
    min_support = int(contents[0])
    #find frequent 1 itemset:
    dict_freq_itemsets, item_set, t_data = getFrequent_1_Itemset(contents)   
    
    for i in range(len(item_set)):
        #generate new itemsets with length (i+2) (length = 2,3,4,...)
        generated_itemset = CreateNewSet(item_set, length = i+2)
        #get frequent itemset from generated itemset
        dict_freq,freq_itemset_list = getFrequentItemset(generated_itemset,min_support,t_data )
        #unitl no freqent items available:
        if len(freq_itemset_list) == 0: 
            break
        #updata item_set and dict
        dict_freq_itemsets.update(dict_freq)
        item_set  = item_set + freq_itemset_list
        
    return dict_freq_itemsets, item_set


################################################
#find closed patterns from all frequent patterns
################################################
def findClosedPatterns(dict_freq_itemsets, item_set):
    '''
    find closed patterns from previous results.
    '''
    #create a deep copy
    closed_dict =  {key: value for key, value in dict_freq_itemsets.items()}
    
    for item_1 in item_set:
        if type(item_1) == str:
            item_1 = [item_1]
        value_1= dict_freq_itemsets[getCombinedKey(item_1)]
        for item_2 in item_set:
            if type(item_2) == str:
                item_2 = [item_2] 
            value_2= dict_freq_itemsets[getCombinedKey(item_2)]
            #delete patterns when:
            if set(item_1).issubset(set(item_2)) and value_1<=value_2 and item_1!=item_2:
                del closed_dict[getCombinedKey(item_1)]
                #print(item_1)
                #print(item_2)
                #print(closed_dict)
                break
    
    return closed_dict
    
################################################
#find maximal  patterns from all frequent patterns
################################################
def findMaxPatterns(closed_dict):    
    #construct a list with set contianing all closed itemsets
    closed_itemset_list = []
    for key in closed_dict:
        closed_itemset_list.append(set(key.split()))
    #find maximal patterns:
    #create a deep copy:
    max_dict =  {key: value for key, value in closed_dict.items()}
    
    for item_1 in closed_itemset_list:
        if type(item_1) == str:
                item_1 = [item_1]
        for item_2 in closed_itemset_list:
            if type(item_2) == str:
                item_2 = [item_2]  
            
            if set(item_1).issubset(set(item_2)) and item_1!=item_2:
                del max_dict[getCombinedKey(item_1)]
                break
    return max_dict
 

def sorted_itemset(dict_freq_itemsets):
    #get the sorted frequent itemsets
    sorted_key = [v[0] for v in sorted(dict_freq_itemsets.items(), key=lambda x: (-x[1],x[0]))     ]
    return sorted_key

    
if __name__ == '__main__':
    #create data
    '''
    contents = ['2', 'a b c d ', 'd f e a', 'a c', 'e d','a e d','a f e']
    contents = ['2','data mining','frequent pattern mining',
                'mining frequent patterns from the transaction dataset','closed and maximal pattern mining']
    '''
    #read data from stdin
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
        
    #find frequent itemsets
    dict_freq_itemsets, item_set = Apriori(contents)
    #find closed patterns
    closed_dict = findClosedPatterns(dict_freq_itemsets, item_set)
    #finf maximal patterns
    max_dict = findMaxPatterns(closed_dict)
    
    #sort three dicts:
    sorted_key_1 = sorted_itemset(dict_freq_itemsets)
    sorted_key_2 = sorted_itemset(closed_dict)
    sorted_key_3 = sorted_itemset(max_dict)
    
    #print by spedific requirements
    for key in sorted_key_1:
        print(str(dict_freq_itemsets[key]) + ' [' + key +']')
    print()
    for key in sorted_key_2:
        print(str(closed_dict[key]) + ' [' + key +']')
    print()
    for key in sorted_key_3:
        print(str(max_dict[key]) + ' [' + key +']')
    

    
    
    
    