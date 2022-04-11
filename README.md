# Grammatical Error Correction

This repository contains the final project of the course Recent Advances in Language Generation CS-E407505 of Aalto University.


# Summary 

The project consists of generating synthetic data of grammatical errors in a novel way. Subsequently, T5 small version is trained on this data and the evaluation is performed on BEA test data.

## Inspiration 

Some ideas were taken and/or modified from specific GEC papers: 

### **Neural GEC Systems with unsupervised pre-training on synthetic data by Grundkiewicz et al.**

-Word level operations: 
- Substitution using spellcheckers 
- Deletion
- Insertion with random words
- Swapping with the next word (word(i+1))
    

-Character level operations: Similar to word operations

### **A simple recipe for Multilingual Error Correction by Rothe et al.**

-Word level operations: 
- Lowercase a word
- Uppercase the first letter of a word


## Approach
![GeneralApp.](https://github.com/MateoRuedaMolano/NLG-project/blob/main/Images/Flowchart.jpg)
