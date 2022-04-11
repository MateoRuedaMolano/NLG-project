# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 13:49:33 2022

@author: mates
"""
from datasets import load_metric
from datasets import Dataset
import numpy as np
import random


def read_dataset2(path: str, contains_targets: bool = True) -> Dataset:
  """Reads in data from a text/tsv file and returns a Huggingface dataset.

  Each line of the file should contain a source-target pair separated by a tab
  when `contains_targets` is True. When it's False, each line should contain
  just a source (used for the test set that doesn't have targets).
  """
  sources = []
  target_lists = []
  with open(path, 'rb') as f:
    for line in f:
      line = line.rstrip(b'\n')
      line = line.rstrip(b'"\r')
      if contains_targets:
        try:
            source, target = line.split(b'\t')
            source = source.decode()
            if source[0] == '\"':
                source = source[1:]
            target = target.decode()
        except:
            continue
      else:
        source, target = line, ''
      sources.append([source])
      target_lists.append(target)
  features = {"sentence": target_lists, "corrections": sources}
  return Dataset.from_dict(features)

DatasetAll = read_dataset2('./Dataset10.tsv')
#Shuffle the dataset 
DatasetAll = DatasetAll.shuffle(seed=42)

dataDict = DatasetAll.train_test_split(test_size=0.0001)
training_set = dataDict['train']
validation_set =dataDict['test']