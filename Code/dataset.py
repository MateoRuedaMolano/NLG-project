# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 20:07:35 2022

@author: 1013449
"""
import re
from datasets import load_dataset
import random
import functions
import os
import csv

########################## OPEN FILE FOR WRITING
f = open(os.path.abspath("./Dataset1302070.tsv"), 'w', encoding='utf-8', newline='\n')
writer = csv.writer(f)


########################## LOADING THE DATASET

wikipedia = load_dataset("wikipedia", "20200501.en")


letters= "([A-Za-z])"
prefix = "(Mr|St|Mrs|Ms|Dr|DrSc)[.]"
suffix = "(Inc|Ltd|Jr|Sr|Co)"
st = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
urlW = "[.](com|net|org|io|gov|yhtml)"
chinese = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)   


############################# DATA CLEANING
#Separating the Wikipedia Paragraphs into sentences
def split_paragraph(paragraph):
    paragraph = " " + paragraph + "  "
    paragraph = paragraph.replace("\n"," ")
    paragraph = re.sub(prefix,"\\1<prd>",paragraph)
    paragraph = re.sub(urlW,"<prd>\\1",paragraph)
    if "Ph.D" in paragraph: paragraph = paragraph.replace("Ph.D.","Ph<prd>D<prd>")
    paragraph  = chinese.sub('', paragraph)
    paragraph = re.sub('(?:\s)https[^, ]*', '', paragraph)
    paragraph = re.sub('(?:\s)http[^, ]*', '', paragraph)
    paragraph = re.sub('(?:\s)www[^, ]*', '', paragraph)
    paragraph = re.sub('(?:\s)url[^, ]*', '', paragraph)
    paragraph = re.sub("\s" + letters + "[.] "," \\1<prd> ",paragraph)
    paragraph = re.sub(acronyms+" "+st,"\\1<stop> \\2",paragraph)
    paragraph = re.sub(letters + "[.]" + letters + "[.]" + letters + "[.]","\\1<prd>\\2<prd>\\3<prd>",paragraph)
    paragraph = re.sub(letters + "[.]" + letters + "[.]","\\1<prd>\\2<prd>",paragraph)
    paragraph = re.sub(" "+suffix+"[.] "+st," \\1<stop> \\2",paragraph)
    paragraph = re.sub(" "+suffix+"[.]"," \\1<prd>",paragraph)
    paragraph = re.sub(" " + letters + "[.]"," \\1<prd>",paragraph)
    
    if "”" in paragraph: paragraph = paragraph.replace(".”","”.")
    if "\"" in paragraph: paragraph = paragraph.replace(".\"","\".")
    if "!" in paragraph: paragraph = paragraph.replace("!\"","\"!")
    if "?" in paragraph: paragraph = paragraph.replace("?\"","\"?")
    paragraph = paragraph.replace(".",".<stop>")
    paragraph = paragraph.replace("?","?<stop>")
    paragraph = paragraph.replace("!","!<stop>")
    paragraph = paragraph.replace("<prd>",".")
    paragraph = re.sub(' +', ' ', paragraph)
    phrases = paragraph.split("<stop>")
    phrases = phrases[:-1]
    phrases = [s.strip() for s in phrases if len(s)>10]
    return phrases

#Dataframe that has all corrected sentences
dataDict = {'train': []}
#n = len(wikipedia['train'])

#### NUMBER OF PARAGRAPHS TO BE PROCESSED
n = 100000


for i in range(0, n):
    paragraph = wikipedia['train'][i]['text']
    sentences = split_paragraph(paragraph)
    for s in sentences:
        dataDict['train'].append(s)
 
        
#Shuffle the dataset 
random.shuffle(dataDict['train'])


################################################## PARAMETERS
percentCorrupted = 30
percentMayusLower = 10
percentageToken = 20
percentageSymbolElimination = 75

#Token level operations

tokenProbs = [0.2, 0.25, 0.2, 0.25, 0.1]
# a: Addition, s: Substitution, e: Elimination, i:Swap, m:Multi-Token
tokenOperations = ['a', 's', 'e', 'i', 'm']

### Multitoken operations
tokenMultiProbs = [0.25, 0.25, 0.25, 0.25]
# a: Addition, s: Substitution, e: Elimination, i:Swap
tokenMultiOperations = ['ma', 'ms', 'me', 'mi']


#Word level operations

wordProbs = [0.01, 0.05, 0.13, 0.10, 0.01, 0.7]
# m: Uppercase, s: Elimination, a: Addition, i:Swap, p: Punctuation, s: Substition 
wordOperations = ['m','e','a','i', 'p', 's']


################ 
nSentences = len(dataDict['train'])- int(len(dataDict['train'])/50)

########################################## GENERATE THE NEW SENTENCES
for j in range(0, nSentences):
    
    sentence = dataDict['train'][j]
    words = sentence.split()
    
    # Iterate over the words
    for i in range(0, len(words)):
        try:
            word = words[i]
        except IndexError:
            break
        ########################### WORD IS CORRUPTED ###############
        if random.randint(1, 100) <= percentCorrupted:
            try:
                c = word[0].isupper()
            except:
                print('why god')
                continue                
            if c:    
                
                ##### MAYUS corruption
                if  random.randint(1, 100) <= percentMayusLower:
                    words[i] = functions.lowerCase(word)
                    word = words[i]
                
            ############# CHECK TOKEN LEVEL CORRUPTION OR WORD LEVEL CORRUPTION
           
            if  random.randint(1, 100) <= percentageToken:
                
                #Choose a RANDOM TOKEN from the word
                tokenIndex = random.randint(0,len(word)-1)
                token = word[tokenIndex]
                
                #Do not consider digits in GEC
                if token.isdigit():
                    continue
                
                
                ############ Token level corruption
                #Punctuation and special symbols have their own corruptions
                if not(token.isalpha()):
                    if  random.randint(1, 100) <= percentageSymbolElimination:
                        words[i] = functions.symbolElimination(word, tokenIndex)
                    else:
                        words[i] = functions.symbolSubstitution(word, tokenIndex)
                 
                #TOKENS THAT ARE NOT PUNCTUATION OR SPECIAL SYMBOLS
                else:
                    #Token operation
                    tokenOp = functions.choiceBasedOnCDF(tokenOperations, tokenProbs)
                    if tokenOp =='a':
                        words[i] = functions.tokenAddition(word, tokenIndex)
                    elif tokenOp =='s':
                        words[i] = functions.tokenSubstitution(word, tokenIndex)
                    elif tokenOp =='e':
                        words[i] = functions.tokenElimination(word, tokenIndex)
                    elif tokenOp =='i':
                        words[i] = functions.tokenSwap(word, tokenIndex)
                    else:
                        tokenMOp = functions.choiceBasedOnCDF(tokenMultiOperations, tokenMultiProbs)
                        if tokenOp =='ma':
                            words[i] = functions.tokenMultiAddition(word, tokenIndex)
                        elif tokenOp =='ms':
                            words[i] = functions.tokenMultiSubstitution(word, tokenIndex)
                        elif tokenOp =='me':
                            words[i] = functions.tokenMultiElimination(word, tokenIndex)
                        else:
                            words[i] = functions.tokenMultiSwap(word, tokenIndex)
                 
            ############ WORD LEVEL CORRUPTION
            
            else:
                wordOp = functions.choiceBasedOnCDF(wordOperations, wordProbs)
                if wordOp =='m':
                    words[i] = functions.wordUpperCase(word)
                elif wordOp == 'p':
                    words[i] = functions.wordPunctuation(word)
                elif wordOp == 'e':
                    words = functions.wordElimination(i, words)
                elif wordOp == 'a':
                    words = functions.wordAddition(i, words)
                elif wordOp == 'i':
                    functions.wordSwap(i, words)
                else:
                    words[i] = functions.wordSubstitution(word)
                    
            
         ########################### WORD NOT CORRUPTED   ################
        else:
            continue
        
        
        ################################# PRINT THE SENTENCE IN A TSV FILE
    newSentence = ' '.join(words)
    sentencePair = sentence+'\t'+newSentence
    writer.writerow([sentencePair])
                
for z in range(nSentences, len(dataDict['train'])):
    sentence = dataDict['train'][z]
    sentencePair = sentence+'\t'+sentence
    writer.writerow([sentencePair])
    

f.close()


#df = pd.DataFrame(dataDict)
#dataset_CorrectSentences = Dataset(pa.Table.from_pandas(df))
#dataset_CorrectSentences.save_to_disk("./")
