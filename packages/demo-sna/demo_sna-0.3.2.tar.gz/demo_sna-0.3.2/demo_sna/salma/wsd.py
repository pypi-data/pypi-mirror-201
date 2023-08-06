# Comented by tymaa to Run service via GPU
from salma.implication import Implication
from salma import settings 
from pandas import read_excel, concat
import re
from transformers import BertTokenizer,BertForSequenceClassification
from transformers import BertTokenizer,BertForSequenceClassification

import warnings
warnings.filterwarnings("ignore")
import torch

import numpy as np

import pandas as pd

from arabert.preprocess import ArabertPreprocessor

def word_sense(word, sentence):
    lemma = "مدخلة"
    pos = "اسم"
    concept_id = "39000001"
    return word, lemma, pos, concept_id

def normalizearabert(s):
  model_name = 'aubmindlab/bert-base-arabertv02'
  arabert_prep = ArabertPreprocessor(model_name.split("/")[-1])
  return arabert_prep.preprocess(str(s))


def load_data_model():
  file = './modern_examples4bert_true_v4_newcorrectData_BZUthes.xlsx'
  df = read_excel("{}".format(file))
  df['Example'] = df['Example'].apply(lambda x: str(x).upper())
  df['Example'] = df['Example'].apply(lambda x: re.sub(r'^((.?\[UNUSED0\].?){1})\[UNUSED0\]', r'\1[UNUSED1]', str(x)) )

  dftrain = df[df['Is_training'] == 1]

  dftrue = dftrain[dftrain['Label'] == 1]
 
  # Added by Tymaa 
  # l=[]
  # l.append("Concept_id")
  # l.append("Diac_lemma")
  # l.append("Undiac_lemma")
  # l.append("Gloss")
  # l.append("Target")
  # l.append("Example")
  # dftrue = "{}".format(l)
  # print("df :  \n ",dftrue)


#   dftrue['Lemma'] = dftrue['Lemma'].apply(normalizearabert)
  name = './bert-base-arabertv02_22_May_2021_00h_allglosses_unused01'
  model = BertForSequenceClassification.from_pretrained('{}'.format(name),
                                                        output_hidden_states = True,
                                                        num_labels=2
                                                        )
  tokenizer = BertTokenizer.from_pretrained('{}'.format('./bert-base-arabertv02'))
  tokenizer.add_special_tokens({ "additional_special_tokens": [ "[UNUSED0]" ] })
  tokenizer.add_special_tokens({ "additional_special_tokens": [ "[UNUSED1]" ] })

  model.resize_token_embeddings(len(tokenizer))

  return  dftrue,tokenizer, model


def glosses1(dfcand,target):
# """
# takes a dataframe 
# return 
	# 'none' if the maximum logistic regression score for TRUE class is less than -2 OR
	# the predicted gloss having the maximum logistic regression score
# """
  print("Before read data")
  wic_c = []
  wic_c, _ = read_data(dfcand,normalizearabert,target)
  print("After read data")
  tokenizedwic_c = np.array([settings.tokenizer.encode(x, max_length=512,padding='max_length',truncation='longest_first',add_special_tokens=True) for x in wic_c])
  max_len = 512
  segmentswic = torch.tensor([get_segments(settings.tokenizer.convert_ids_to_tokens(i),max_len) for i in tokenizedwic_c])
  paddedwic = tokenizedwic_c
  attention_maskwic = np.where(paddedwic != 0, 1, 0)
  input_idswic = torch.tensor(paddedwic)  
  attention_maskwic = torch.tensor(attention_maskwic)
  print("Before EVAL function")
  settings.model = settings.model.eval()
  print("After EVAL function")
  wicpredictions , wictrue_labels = [], []
  b_input_ids = input_idswic
  b_input_mask =  attention_maskwic
  b_input_seg = segmentswic

  print("BEFORE MODEL")
  with torch.no_grad():
    print("Inside model")
    outputs = settings.model(b_input_ids,token_type_ids=b_input_seg,attention_mask=b_input_mask)
    print("output")
  print("AFTER MODEL")

  logits = outputs[0]
  wicpredictions.append(logits)
  wicflat_predictions = np.concatenate(wicpredictions, axis=0)
  # if wicflat_predictions[np.argmax(wicflat_predictions, axis=0).flatten()[1]][1] < -2:
    # return 'none'
  # return dfcand['Gloss'].to_list()[np.argmax(wicflat_predictions, axis=0).flatten()[1]]
  
  ### These two lines are commented by Tymaa on 2021-06-28
  #if wicflat_predictions[np.argmax(wicflat_predictions, axis=0).flatten()[1]][1] < -2:
  #  return 'none','none'
  return dfcand['Concept_id'].to_list()[np.argmax(wicflat_predictions, axis=0).flatten()[1]],dfcand['Gloss'].to_list()[np.argmax(wicflat_predictions, axis=0).flatten()[1]]

def read_data(data,normalize,target):
  c = []
  labels = []
  for i,row in data.iterrows():
      # lemma = normalize(row['Undiac_lemma'])
      example = normalize(row['Example'])
      gloss = normalize(row['Gloss'])
      label = row['Label']
      # target = normalize(row['Target'])
      c.append('{} [SEP] {}: {}'.format(example,target,gloss))
      if label == 1.0:
          labels.append(1)
      else:
          labels.append(0)
  return c,labels

def inserttag1(sentence,tag,start,end):
    before = sentence[:start]
    after = sentence[end:]
    target = sentence[start:end]
    return before+tag+sentence[start:end]+tag+after

def get_segments(tokens, max_seq_length):
    # """Segments: 0 for the first sequence, 1 for the second"""
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    segments = []
    current_segment_id = 0
    for token in tokens:
        segments.append(current_segment_id)
        if token == "[SEP]":
            current_segment_id = 1
    return segments + [0] * (max_seq_length - len(tokens))

def senttarget(target,example): ### Make sure to tag words correctely ex:  ذهب الرجل ليشتري ذهب، / عند& عندهم
  start = -1
  try:
    start = example.index(target)
  except ValueError:
    return -1
  end = example.index(target)+len(target)
  return inserttag1(example,"[UNUSED0]",start,end)


def GlossPredictor(diac_lemma, undiac_lemma,target,example,glosses):
# """ 
# takes 
	# a lemma
	# corresponding target word 
	# an example
	# glosses as a dictionay, following an example:
	#	glosses =	{"Concept_id1": "gloss1",  "Concept_id2": "gloss2",  "Concept_id3": "gloss3"}
# returns 
	# -1   if the example does not contain the target word  OR
	# 'none' if no records in dftrue for the lemma and if the maximum logistic regression score for TRUE class is less than -2 OR
	# the predicted gloss for the target word 
	# 
# """
  example = senttarget(target,example)
  if example == -1:
    return -1,-1
  # All records for Undiac_lemma
  #dfcand1 = settings.dftrue[settings.dftrue['Undiac_lemma'] == undiac_lemma]
  #m = dfcand1['Diac_lemma'].apply(lambda x: samelemma(x,diac_lemma))
  ### Added by Tymaa ON 2021-06-13 in case m is empty 
  #if len(m) <= 0:
  #  m = dfcand1
  # All records for Diac_lemma from dfcand1
  #dfcand = dfcand1[m]
  
  data = []
  for g in glosses:
      data.append([g,diac_lemma,undiac_lemma, glosses[g], target,example,0,1,'','',''])
  dfcolumns = ['Concept_id', 'Diac_lemma', 'Undiac_lemma', 'Gloss', 'Target', 'Example', 'Is_training', 'Label', 'concept_id', 'lemma_id', 'POS']
  dfcand = pd.DataFrame(data,columns=dfcolumns)
  
  
  if len(dfcand) > 0:
    dfcand['Example'] = dfcand['Example'].apply(lambda x: example)
    dfcand['Target'] = dfcand['Target'].apply(lambda x: target)
    dfcand = dfcand.drop_duplicates()
  
    dfcand['Example'] = dfcand['Example'].apply(lambda x: x.upper())
    dfcand['Example'] = dfcand['Example'].apply(lambda x: re.sub(r'^((.?\[UNUSED0\].?){1})\[UNUSED0\]', r'\1[UNUSED1]', x) )
    print("Before glosses1 into GlossPredictor function  dfcand : ",dfcand, "  target: ",target)
    return glosses1(dfcand,target)
  else:
    return 'none','none'


def samelemma(w1,w2):
  implication =  Implication(w1 , w2)
  if implication.getResult() == 'Same':
    return True
  else:
    return False      