# Pattern_Mining
The repo includes:
## 1. Apriori Algorithm for frequent pattern mining.
A simple Apriori algorithm for:
    (1)mining frequent patterns
    (2)finding closed patterns
    (3)finding maximal patterns

No extra packages used. 

Able to take care of all transctions that can be transformed into a string, with following input requirements.

Input requirements: 
    stdin input per HW requirement.
    first line is min support
    each following line is a item set. Different items in a set is seperated by a space. (This is required in this code)
    
Output:
    print frequent patterns sorted by support and then alphabetically
    print closed patterns
    
## 2. Modified GSP algorithm for Apriori-Based Sequential Pattern Mining
The GSP algorithm is modified to improve efficiency.

Core idea of the modification is to reduce the number of times we need to scan over the documents by only looking at neighbors of current k-1 frequent itemsets.

Input: 
A 20Kb text file is used as an example. (from: https://www.sample-videos.com/download-sample-text-file.php).
stdin input is also supported per homework requirement.

Output: 
The most frequent 20 sequential patterns mined out from the input dataset. Sorted by support and then ASCII order.



