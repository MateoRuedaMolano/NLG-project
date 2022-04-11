# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 16:49:19 2022

@author: 1013449
"""
import random
import bisect
import sklearn

#################### CDF distributions for symbol and character level substitution
symbolProbs = [0.294, 0.276, 0.122, 0.109, 0.068, 0.028, 0.013, 0.013, 0.013, 0.032, 0.032]
specialSymbols = ['.', ',', '"', '\'', '-', '?', ':', '!', ';', '(', ')']


################### CDF distribution for characters 
characterProbs = [0.082, 0.010, 0.027, 0.047, 0.13, 0.022, 0.02, 0.062, 0.069, 0.0016, 0.0081, 0.04, 0.027,
                  0.067, 0.078, 0.019, 0.001, 0.059, 0.062, 0.096, 0.027, 0.0097, 0.024, 0.0015, 0.01, 0.0001]

characterSymbols = ['a','b','c','d', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                    'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


###################### LIST OF WORDS TO BE ADDED
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
stopwords[0] = 'I'

######################## CONJUGATOR
from pattern.en import *

########################################### CORRUPTION FUNCTIONS


############# LOWER CASE:
def lowerCase(word):
    return word[0].lower() + word[1:]

########## SYMBOL CORRUPTIONS

#Symbol elimination
def symbolElimination(word, tokenIndex):
    return word[:tokenIndex] + word[tokenIndex+ 1:]


#Calculate cdf and choice an item based on the probabilities
def cdf(probs):
    sumProbs = sum(probs)
    cdfList = []
    cdfSum = 0
    for p in probs:
        cdfSum += p
        cdfList.append(cdfSum / sumProbs)
    return cdfList

def choiceBasedOnCDF(symbols, probs):
    assert len(symbols) == len(probs)
    cdf_vals = cdf(probs)
    value = random.random()
    idx = bisect.bisect(cdf_vals, value)
    return symbols[idx]


def symbolSubstitution(word, tokenIndex):
    newSymbol = choiceBasedOnCDF(specialSymbols,symbolProbs)
    return word[:tokenIndex] + newSymbol + word[tokenIndex+1:]

############## TOKEN LEVEL CORRUPTIONS

def tokenAddition(word, tokenIndex):
    direction = random.randint(0,1)
    #Left
    newSymbol =  choiceBasedOnCDF(characterSymbols,characterProbs)
    if direction == 0:
        return word[:tokenIndex] + newSymbol + word[tokenIndex:] 
    #Right
    if direction == 1:
        return word[:tokenIndex+1] + newSymbol + word[tokenIndex+1:] 

def tokenSubstitution(word, tokenIndex):
    newSymbol =  choiceBasedOnCDF(characterSymbols,characterProbs)
    return word[:tokenIndex] + newSymbol + word[tokenIndex+1:]       

def tokenElimination(word, tokenIndex):
    return word[:tokenIndex] + word[tokenIndex+ 1:]     
        
def tokenSwap(word, tokenIndex):
    if tokenIndex < len(word)-1:
        return word[:tokenIndex]+word[tokenIndex+1]+word[tokenIndex]+ word[tokenIndex+2:]
    else:
        return word[tokenIndex]+word[1:tokenIndex]+ word[0]
    
def tokenMultiAddition(word, tokenIndex):
    
    direction = random.randint(0,1)
    newSymbol =  choiceBasedOnCDF(characterSymbols,characterProbs)
    newSymbol2 =  choiceBasedOnCDF(characterSymbols,characterProbs)
    #Left
    if direction == 0:
        return word[:tokenIndex] + newSymbol+ newSymbol2 + word[tokenIndex:] 
    #Right
    if direction == 1:
        return word[:tokenIndex+1] + newSymbol + newSymbol2+ word[tokenIndex+1:]
    

def tokenMultiSubstitution(word, tokenIndex):
    
    newSymbol =  choiceBasedOnCDF(characterSymbols,characterProbs)
    newSymbol2 =  choiceBasedOnCDF(characterSymbols,characterProbs)
    
    if tokenIndex < len(word)-1:
        return word[:tokenIndex] + newSymbol + newSymbol2 + word[tokenIndex+2:]    
    else:
        return newSymbol + word[1:tokenIndex] + newSymbol2
       

def tokenMultiElimination(word, tokenIndex):
    if tokenIndex < len(word)-1:
        return word[:tokenIndex] + word[tokenIndex+2:]     
    else:
        return word[1]+word[2:tokenIndex]    
        
def tokenMultiSwap(word, tokenIndex):
    if tokenIndex < len(word)-1:
        return word[:tokenIndex]+word[tokenIndex+1]+word[tokenIndex]+ word[tokenIndex+2:]
    else:
        return word[tokenIndex]+word[1:tokenIndex]+ word[0]



############################# WORD LEVEL FUNCTIONS
def wordUpperCase(word):
    return word[0].upper() + word[1:]


# Arguments
# Index = word that will be deleted
# Words- List of words of that sentence
def wordElimination(index, words):
    words.pop(index)
    return words
    

def wordAddition(index, words):
    continuation = 1
    while True:
        direction = random.randint(0,1)
        
        #Choose the word to be added randomly
        randomIndex = random.randint(0, len(stopwords)-1)
        stopWord = stopwords[randomIndex]
        
        continuation = continuation*0.5
        #Left
        if direction == 0:
            words.insert(index, stopWord)
            index = index-1
        #Right
        if direction == 1:
            words.insert(index+1, stopWord)
            index = index+1
        
        #Decision of add more words
        if random.random() > continuation:
            break
    return words

def wordSwap(index, words):
    continuation = 1
    while True:
        if index < len(words)-1:
            temp = words[index]
            words[index] = words[index + 1]
            words[index + 1] = temp
            continuation = continuation*0.5
            index = index+1
        else:
            temp = words[index]
            words[index] = words[0]
            words[0] = temp
            continuation = continuation*0.5
            index = 0
            
        if random.random() > continuation:
             break
    
def wordPunctuation(word):
    direction = random.randint(0,1)
    punctuation = choiceBasedOnCDF(specialSymbols,symbolProbs)
    if direction == 0:
        return word+punctuation
    else:
        return punctuation+word
    
def wordSubstitution(word):
    

    wordType = parse(word).split('/')[1]    
    ############################## CHECK IF WORD IS A VERB
    if wordType.startswith('V'):
        counter = 0
        conjugations = lexeme(word)
        #If the conjugation is the same as the word, try another conjugation
        while(True):
            idx = random.randint(0,len(conjugations)-1)
            #Preventing an infinite loop
            if counter>3:
                return word
            if word == conjugations[idx]:
                counter+=1
            else:
                return conjugations[idx]
     
        # WORD is an adjective or Adverb
    elif wordType.startswith('J') or wordType.startswith('R'):
        decision= random.randint(0,5)
        #Comparative form of adjective
        if decision<3:
            comp = comparative(word)
        elif decision >= 3 and decision < 5:
            comp = superlative(word)
        else:
            if random.randint(0,1)> 0:
                comp = pluralize(word)
            else:
                comp = singularize(word)
        
        return comp
    else:
        if random.randint(0,3)> 0:
            comp = pluralize(word)
        else:
            comp = singularize(word)
        return comp
        
        
                
                
    
