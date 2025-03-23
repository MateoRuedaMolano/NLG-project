# Grammatical Error Correction

This repository contains the final project of the course Recent Advances in Language Generation CS-E407505 of Aalto University.


# Summary 

The project consists of generating synthetic data of grammatical errors in a novel way. Subsequently, T5 small version is trained on this data and the evaluation is performed on BEA test data.

## Inspiration 

Some ideas were taken and/or modified from specific GEC papers: 

### **Neural GEC Systems with unsupervised pre-training on synthetic data by Grundkiewicz et al.**

* Word level operations: 
    * Substitution using spellcheckers 
    * Deletion
    * Insertion with random words
    * Swapping with the next word (word(i+1))
    

* Character level operations: Similar to word operations

### **A simple recipe for Multilingual Error Correction by Rothe et al.**

* Word level operations: 
    * Lowercase a word    
    * Uppercase the first letter of a word

## Data
**Seed Corpus:** Wikipedia, scraped on 1st of May 2020.
Data paragraphs were cleaned and separated into sentences.

## Approach

For every sentence, each word with a probability of 0.3 is modified following this flow chart:
![GeneralApp.](https://github.com/MateoRuedaMolano/NLG-project/blob/main/Images/FlowchartC.jpg)

### Word addition: 
Using STOPWORDS from NLTK.corpus which is a list of very common words such as prepositions, articles, pronouns, among others.

### Word substitution:
The selected word to be modified follows the following procedure:

![GeneralApp.](https://github.com/MateoRuedaMolano/NLG-project/blob/main/Images/Untitled.jpg)

### Word punctuation
If the character to be modified is a punctuation mark, this is replaced by another one with probability of 0.25 or deleted with probability of 0.75.

# Running the code:
To create the dataset with the chosen parameters, run:
```
python dataset.py
```
Run the jupyter notebook for training, you will also get the BEA prediction results. Keep in mind to change the path for the training dataset.


