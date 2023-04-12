import numpy as np
import string

def PreprocessingTextData(text1, text2):
  text_1 = text1.translate(str.maketrans('', '', string.punctuation))
  text_2 = text2.translate(str.maketrans('', '', string.punctuation))
  text_1 = text_1.split(' ')
  text_2 = text_2.split(' ')
  text_1 = [w.lower() for w in text_1 if w.isalpha()]
  text_2 = [w.lower() for w in text_2 if w.isalpha()]
  
  text1_set = set(text_1)
  text2_set = set(text_2)
  return text1_set, text2_set

def word_to_numerical(set1 , set2):
  l1=[]
  l2=[]
  rvector = set1.union(set2)
  for word in rvector:
    if word in set1:
      l1.append(1)
    else:
      l1.append(0)
    if word in set2:
      l2.append(1)
    else:
      l2.append(0)
  return rvector, l1, l2

def cosine_fomula(l1, l2):
  l1 = np.array(l1)
  l2 = np.array(l2)
  s = np.sum(l1*l2)
  return s / float((np.sum(l1**2)*np.sum(l2**2))**0.5)

def checkAuthorName(realauthorname, inputauthorname):
    realauthorname = realauthorname.replace('-', ' ')
    text1_set, text2_set = PreprocessingTextData(realauthorname, inputauthorname)
    rvector, l1, l2 = word_to_numerical(text1_set, text2_set)
    if cosine_fomula(l1, l2) >= 0.98:
       return 1
    else:
       return 0