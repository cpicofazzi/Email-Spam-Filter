############################################################
# CMPSC442: Homework 5
############################################################

student_name = "Christian Picofazzi"

############################################################
# Imports
############################################################
import email
import os
import math
import collections


# Include your imports here, if any are used.

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    fd = open(email_path,'Ur')
    messageObj = email.message_from_file(fd)
    Chunks = email.iterators.body_line_iterator(messageObj)
    fd.close()
    messageChunks = list(Chunks)
    tokens = []
    for string in messageChunks:
        tokens = tokens + string.split()
        #print(string.split())

    return tokens



def log_probs(email_paths, smoothing):
    listV = []
    for path in email_paths:
        listV += load_tokens(path)
    wordCounts = collections.Counter(listV)
    cntsLen = len(wordCounts)
    #print(wordCounts)

    probDict = dict()
    wordCountSum = len(listV)
   


    for word in wordCounts:
        #print(word,wordCounts[word])
        prob = ((wordCounts[word] + smoothing) / (wordCountSum + (smoothing*((cntsLen + 1)))))
        probDict[word] = math.log(prob)
    
    probDict['<UNK>'] = math.log(((smoothing) / (wordCountSum + (smoothing*((cntsLen + 1))))))

    return probDict

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        self.spam_dir = spam_dir
        self.ham_dir = ham_dir
        self.smoothing = smoothing
        #print("one")
        spamPaths = [spam_dir+"/%s" %word for word in  os.listdir(spam_dir)]
        self.spam_log_prob_dict = log_probs(spamPaths,smoothing)
        #print("two")
        hamPaths = [ham_dir+"/%s" %word for word in  os.listdir(ham_dir)]
        self.ham_log_prob_dict = log_probs(hamPaths,smoothing)
        #print("three")
        self.spam_prob = float(len(spamPaths) / float(len(spamPaths)+len(hamPaths)))
        self.nspam_prob = 1 - self.spam_prob
         
    
    def is_spam(self, email_path):
        wordCounts = collections.Counter(load_tokens(email_path))


        wordProd = 0
        wordProdH = 0
        for word in wordCounts:
            if word in self.spam_log_prob_dict:
                wordProd += wordCounts[word] * self.spam_log_prob_dict[word]
                #print(wordCounts[word] , self.spam_log_prob_dict[word])
            else:
                wordProd += self.spam_log_prob_dict['<UNK>']
                #print("UNK", self.spam_log_prob_dict['<UNK>'])
            if word in self.ham_log_prob_dict:
                wordProdH += wordCounts[word] * self.ham_log_prob_dict[word]
                #print(wordCounts[word] , self.ham_log_prob_dict[word])
            else:
                wordProdH += self.ham_log_prob_dict['<UNK>']
                #print("UNK", self.ham_log_prob_dict['<UNK>'])
        


        spamProb = math.log(self.spam_prob) + wordProd
        hamProb = math.log(self.nspam_prob) + wordProdH

        #print(spamProb)
        #print(hamProb)
        if(spamProb > hamProb):
            return True
        else:
            return False
        
        #print(math.exp(spamProb))

    


    def most_indicative_spam(self, n):
        Set = set()
        for word in self.spam_log_prob_dict:
            if word in self.ham_log_prob_dict:
                #calc indication
                ind = self.ham_log_prob_dict[word] - math.log(math.exp(self.ham_log_prob_dict[word])+ math.exp(self.spam_log_prob_dict[word]))
                Set.add((ind,word))
        orderedSet = sorted(Set, key = lambda tup:tup[0])
        #print(orderedSet[0:n])
        return [group[1] for group in orderedSet[0:n]]

    def most_indicative_ham(self, n):
        Set = set()
        for word in self.ham_log_prob_dict:
            if word in self.spam_log_prob_dict:
                #calc indication
                ind = self.spam_log_prob_dict[word] - math.log(math.exp(self.ham_log_prob_dict[word])+ math.exp(self.spam_log_prob_dict[word]))
                Set.add((ind,word))
        orderedSet = sorted(Set, key = lambda tup:tup[0])
        #print(orderedSet[0:n])
        return [group[1] for group in orderedSet[0:n]]

############################################################
# Section 2: Feedback
############################################################



feedback_question_1 = """
15 hours
"""

feedback_question_2 = """
Trying to understand what the question was asking. Trying to figure out if my solution was correct or not (TESTNG)
"""

feedback_question_3 = """
I liked how it was simple but I feel like the functions did not have alot of meeting.
"""
