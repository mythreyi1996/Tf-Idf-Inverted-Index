# coding: utf-8
# In[1]:

import sys

# term_f = frequency of term t in file f.
class Postings:
    def __init__(self, val):
        self.val = val
        self.term_f = 1
        self.tf = 0.0
        self.idf = 0.0
        self.tf_idf = 0.0
        self.next = None

    def insert(self,val, no_of_terms):
        while self != None:
            if self.val == val:
                self.term_f =  self.term_f + 1
                self.tf = (float) (self.term_f / no_of_terms)
                return 0
            elif self.next == None:
                temp = Postings(val)
                self.next = temp
                temp.tf = (float) (temp.term_f / no_of_terms)
                return 1
            self = self.next

    def insert_tf_idf(self,val, tf_idf):
        while self != None:
            if self.val == val:
                self.term_f =  self.term_f + 1
                self.tf_idf = tf_idf
                return 0
            if self.next == None:
                temp = Postings(val)
                temp.tf_idf = tf_idf
                self.next = temp
                return 1
            self = self.next

    def update_idf(self, no_of_words, frequency):
        self.idf = (float) (no_of_words / frequency)
        self.tf_idf = (float) (self.tf  * self.idf)

    def display(self, f_output):
        f_output.write("\nPostings list:")
        while self != None:
            f_output.write(" " + self.val)
            self = self.next

dict = {}
#dict format : term : [address of first node in posting list, no.of documents containing term t]
# index takes a document n at a time and indexes it. The tf of the doc with respect to its term is also calculated in this function.
def index(n):
    docId = n.split("\t")
    words = docId[1].split(" ")
    no_of_words = len(words)
    for term in words:
        if term.endswith("\n"):
            term = term[0:-1]
        if term not in dict.keys():
            count = 1
            dict[term] = [Postings(docId[0]),count]
            dict[term][0].tf = (float) (dict[term][0].term_f / no_of_words)
        else :
            t = dict[term][0]
            if (t.insert(docId[0], no_of_words)):
                dict[term][1] = dict[term][1] + 1

# TF(t) = (Number of times term t appears in a document) / (Total number of terms in
#the document).
#IDF(t) = (Total number of documents / Number of documents with term t in it).


# In[2]:

#Print function is used to take care of the space issues.
def Print_terms(terms, f_output):
    for i in range (0, len(terms)):
        if( i == len(terms) - 1):
            f_output.write(terms[i])
        else:
            f_output.write(terms[i] + " ")

#Gets the postings for the given set of terms.
def GetPostings(terms, f_output):
    for term in terms:
        f_output.write("GetPostings")
        f_output.write("\n" + term)
        dict[term][0].display(f_output)
        f_output.write("\n")


# In[3]:

# Takes the positing list of the terms and merge with AND operation.
# Optimization ideas used : 
# 1)Find the term posting list with minimum length. Compare each node (docID) with the remaining lists, if present, add to results.
# 2) If DocId is not present in one of the posting list, break and move to next term in the minimum posting list.
# 3) Move simultaneouly, move until docId is greater the docId selected from the minium posting list. 
def DaatAnd(terms, f_output):
    min_count = 10000000000
    postings = []
    i = 0
    Final_postings = {}
    key_order = []
    count = 0
    for term in terms:
        if (dict[term][1] < min_count):
            min_count = dict[term][1]
            min_posting = dict[term][0]
    for term in terms:
        if dict[term][0] != min_posting:
            postings.append(dict[term][0])
    while(min_posting != None):
        value = min_posting.val
        i = 0
        index
        Flag = [0] * (len(terms) - 1)
        tf_idf = 0
        for j in range (0, len(postings)):
            while(postings[j] != None and postings[j].val <= value):
                count = count + 1
                if postings[j].val == min_posting.val:
                    tf_idf = tf_idf + postings[j].tf_idf
                    Flag[i] = 1
                    postings[j] = postings[j].next
                    break
                else:
                    postings[j] = postings[j].next
            if Flag[i] == 0 and postings[j] != None:
                count = count + 1
                break
            i = i + 1
        if len(Flag) > 0 :
            result = all(elem == 1 for elem in Flag)
        if result :
            Final_postings[value] = tf_idf
            key_order.append(value)
        min_posting = min_posting.next
    f_output.write("DaatAnd" + "\n")
    Print_terms(terms, f_output)
    f_output.write("\nResults: ")
    if Final_postings == {}:
        f_output.write("empty")
    else:
        Print_terms(key_order, f_output)
    f_output.write("\nNumber of documents in results: " + str(len(Final_postings)))
    f_output.write("\nNumber of comparisons: " + str(count))
    TF_IDF(Final_postings, f_output)
    return Final_postings
  
# In[5]:

# Sorting two posting lists.
def sort(a1, a2, count):
    Final_list = None
    tf_idf = 0
    while(a1 != None and a2 != None):
        count = count + 1
        if(a1.val == a2.val):
            t = a1.val
            tf_idf = a1.tf_idf + a2.tf_idf
            a1 = a1.next
            a2 = a2.next
        elif(a1.val > a2.val):
            t = a2.val
            tf_idf = a2.tf_idf
            a2 = a2.next
        elif(a1.val < a2.val):
            t = a1.val
            tf_idf = a1.tf_idf
            a1 = a1.next

        if (Final_list == None):
            Final_list = Postings(t)
            Final_list.tf_idf = tf_idf
        else:
            Final_list.insert_tf_idf(t, tf_idf)
    if(a1 == None):
        while(a2 != None):
            tf_idf = a2.tf_idf
            Final_list.insert_tf_idf(a2.val, tf_idf)
            a2 = a2.next
    else:
        while(a1 != None):
            tf_idf = a1.tf_idf
            Final_list.insert_tf_idf(a1.val, tf_idf)
            a1 = a1.next
    return Final_list, count    


# In[6]:

# Performs or operation on the posting lists of the terms.
# Optimization ideas used :
# 1) Merge consecutive postings lists. At each iteration, the no.of array reduces by 2. Divides the problem and reduces computation.
def DaatOr(terms, f_output):
    count = 0
    Final_postings = {}
    key_order = []
    postings_list = []
    for term in terms:
        postings_list.append(dict[term][0])
    while(len(postings_list) != 1):
        sorting_arr = []
        length = len(postings_list)
        if(len(postings_list) % 2 == 0):
            size = len(postings_list)
        else:
            sorting_arr.append(postings_list[length - 1])
            length = length - 1
        for i in range(0, length - 1,2):
            temp, count = sort(postings_list[i], postings_list[i+1], count)
            sorting_arr.append(temp)
        postings_list = sorting_arr
    while(postings_list[0] != None):
        Final_postings[ postings_list[0].val] = postings_list[0].tf_idf
        key_order.append(postings_list[0].val)
        postings_list[0] = postings_list[0].next
    f_output.write("\nDaatOr\n")
    Print_terms(terms, f_output)
    f_output.write("\nResults: ")
    if Final_postings == {}:
        f_output.write("empty")
    else:
        Print_terms(key_order, f_output)
    f_output.write("\nNumber of documents in results: " + str(len(Final_postings)))
    f_output.write("\nNumber of comparisons: " + str(count))
    TF_IDF(Final_postings, f_output)
    f_output.write("\n")
    return Final_postings   


# In[7]:

# Sorts the Results in decreasing order of TF-IDF
def TF_IDF(Results, f_output):
    f_output.write("\nTF-IDF")
    f_output.write("\nResults: ")
    temp = [] 
    if Results == {}:
        f_output.write("empty")
    else: 
        listofTuples = sorted(Results.items() ,  key=lambda x: x[1], reverse=True)
        for elem in listofTuples :
            temp.append(elem[0])
        Print_terms(temp, f_output)

# In[9]:

# Updates the idf for each document and computes tf-idf
def tf_idf_update(no_of_docs):
    for term in dict.keys():
        head = dict[term][0]
        while(head != None):
            head.update_idf(no_of_docs, dict[term][1])
            head = head.next

def main(argv):
    f= open(argv[1],"r")
    contents =f.readlines()

# index functions created the document index.
    for n in contents:
        index(n)
    f.close()

    tf_idf_update(len(contents))
    f_output= open(argv[2],"w+")
    f_input= open(argv[3],"r")

    lines = f_input.readlines()
    newline = ""
    for n in lines:
        terms = []
        words = n.split(" ")
        for word in words:
            if word.endswith("\n"):
                word = word[0:-1]
            terms.append(word)
        f_output.write(newline)
        GetPostings(terms, f_output)
        newline = "\n"
        DaatAnd(terms, f_output)
        DaatOr(terms, f_output)

if __name__ == "__main__":
    main(sys.argv)

