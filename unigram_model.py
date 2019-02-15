#Author: Andre Dugas
#File: Unigram Model
#Date: February 6, 2019
#Course: Natural Language Processing

#Imported Libraries
from collections import Counter #To count word frequencies
import random #For Shannon Generation using random value

'''File input and unigram/bigram list creation'''

#File Input
text = open("berp-training.txt") #gather words from berp training document
training_words = text.read().split() #list of all individual words stored

#Unigrams
uni_counts = Counter(training_words) #Dict of only unique words and their frequency counts

#Accounting for unk
uni_counts['<UNK>']=0 #add token <UNK> to dictionary
unk_words=[]
for (key, value) in uni_counts.items(): #for loop to find words occuring once, delete them, and change unk count
    if value == 1:
        uni_counts['<UNK>']+=1
        unk_words.append(key)
for key in unk_words:
    if key in uni_counts:
        del uni_counts[key]
for i in range(len(training_words)): #remove words that have replaced by unk
    if training_words[i] in unk_words:
        training_words[i] = "<UNK>"
Nu = sum(uni_counts.values()) #Nu is the total number of tokens
Vu = len(uni_counts) #Vu is the number of unique tokens

#Bigrams
ngrams = zip(*[training_words[i:] for i in range(2)]) #Generates bigrams of length 2 (Note: referenced Stack Exchange)
bigram_list = [" ".join(ngram) for ngram in ngrams]
bi_counts = Counter(bigram_list) #Dict of only unique bigrams and their frequency counts
Nb = sum(bi_counts.values()) #Nb is the total number of bigrams
Vb = len(bi_counts) #Vb is the number of unique bigrams


'''Test helper functions: Product of list, unigram prob, laplace prob, shannon prob distribution'''

#Function to calculate the product of values in a dictionary
def prod(probs_dict):
    ans = 1
    for item in probs_dict.values():
         ans = ans * item
    return ans

#Function to generate a list of unigram probabilities that correlates to the given list of words
def uni_word_prob(unigram_list):
    probs_dict = {}
    for word in unigram_list:
        if word not in uni_counts.keys(): #Account for words appearing once using UNK
            word="<UNK>"
        probs_dict[word] = (uni_counts[word]/Nu) #Simple probability calculation
    return(prod(probs_dict))

#Function to generate a list of bigram probabilities (w/ smoothing) that correlates to the given list of words
def laPlace_smooth(bigram_list):
    probs_dict = {}
    for bigram in bigram_list:
        for word in bigram:
            if word not in uni_counts.keys(): #Account for words appearing once using UNK
                word="<UNK>"
        probs_dict[bigram] = ((bi_counts[bigram]+1)/(uni_counts[bigram[0]]+Vb)) #LaPlace equation
    return(probs_dict)

#Function to select a bigram from a random uniform distribution
def distribution(distributions_list, last_word):
    hash_dict = {} #Hash table for probability distribution
    distr_sum=0 #Used to create a distribution hash of bigrams
    for (key, value) in distributions_list.items(): #Full hash table with sum of distributions
        if key.split()[0] == last_word: #Check for bigrams that start with the last one's 2nd word
            hash_dict[key] = value+distr_sum
            distr_sum=value+distr_sum #Update a corresponding bucket size for the word in the hash table
    n=random.uniform(0,distr_sum) #random number
    for (key, value) in hash_dict.items(): #find the word that corresponds to the randomly generated number
        if value < n:
            location=value
        else:
            return (key.split())
    return("error") #Catch any errors if random number fails


'''Main Unigram, Bigram, and Shannon function Calls'''

#Return the probabililty of a sentence based on unigrams
def unigram(sentence, filename):
    sentence_list=sentence.split() #split into list of words
    filename.write(str(uni_word_prob(sentence_list))) #write results to file

#Return the probabililty of a sentence based on bigrams
def bigram(sentence, filename):
    sentence_list=sentence.split() #split into list of words
    bigrams = zip(*[sentence_list[i:] for i in range(2)]) #Generates bigrams of length 2 (Note: referenced Stack Exchange)
    grams_list = [" ".join(ngram) for ngram in bigrams]
    probs_dict = laPlace_smooth(grams_list) #laplace smoothing probabilities
    filename.write(str(prod(probs_dict))) #write results

#Generates a corpus of 100 sentences using generated bigrams from their corresponding probabilities
def shannon(filename):
    distr = laPlace_smooth(bigram_list) #dictionary of words and corresponding probabilities
    s = 0 #number of sentences generated
    lst = []
    while s<100: #generate 100 sentences
        new_bigram = distribution(distr, '<s>') #defualt with a <s> to begin each sentence
        lst.append('<s>')
        while(new_bigram[1] != '</s>'): #Continue adding new words to sentence until </s> is found
            lst.append(new_bigram[1]) #only add second word in bigram because first word is already accounted for
            new_bigram = distribution(distr, new_bigram[1]) #Call for next bigram
        lst.append(new_bigram[1])
        s+=1 #increment number of sentences created
        sentence = ''
        #Format sentence as a string and write to results file
        for item in lst:
            if item != '</s>':
                sentence += (item + ' ')
            else:
                sentence += '</s>'
        filename.write(sentence)
        lst=[] #reset sentence list for next iteration


'''Main program for user interaction'''

#Main function
def main(args):
    #file opening to write answers
    unigram_results = open("dugas-andre-assgn2-unigram-out.txt","w")
    bigram_results = open("dugas-andre-assgn2-bigram-out.txt","w")
    shannon_results = open("dugas-andre-assgn2-bigram-rand-corpus.txt", 'w')
    test_input = open("100_test.txt", "r") #gather words from testing document
    all_test_words = test_input.read().split() #list of all individual words stored
    #seperate list of test words into sentences
    lst=""
    for word in all_test_words:
        if word != '</s>':
            lst += (word + " ")
        else:
            lst += '</s>'
            unigram(lst, unigram_results) #call unigram model on each sentence
            bigram(lst, bigram_results) #call bigram model on each sentence
            lst=""
    #Shannon Generation
    shannon(shannon_results)

    #Close files
    unigram_results.close()
    bigram_results.close()
    shannon_results.close()
    test_input.close()
    text.close()
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
