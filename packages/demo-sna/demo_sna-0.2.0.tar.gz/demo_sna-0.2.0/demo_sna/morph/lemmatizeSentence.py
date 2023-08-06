from demo_sna.morph.tokenizers_words import simple_word_tokenize
from demo_sna.morph import settings 
import re
import numpy as np
def lemmatize_word(word):
   word = word.strip()
   solution = [word,word+"_0",""]
   # word_undiac = re.sub('[َّ؞ٝٞﱢۚۙ ۭ۠ﱠۡ ۦ ّْـ]+', '',word)
   word_undiac = re.sub(r'[\u064B-\u0650]+', '',word) # Remove all Arabic diacretics [ ًَ]
   word_undiac = re.sub(r'[\u0652]+', '',word_undiac) # Remove SUKUN
   word_undiac = re.sub(r'[\u0651]+', '',word_undiac) # Remove shddah
   word_undiac = re.sub('[\\s]+',' ',word_undiac)
   word_with_unify_alef = re.sub('[أ]','ا',word)
   word_with_unify_alef = re.sub('[ﺇ]','ا',word_with_unify_alef)
   word_with_unify_alef = re.sub('[ٱ]','ا',word_with_unify_alef)
   word_with_unify_alef = re.sub('[ﺃ]','ا',word_with_unify_alef)
   word_with_unify_alef = re.sub('[ﺁ]','ا',word_with_unify_alef)
    
   if word.isdigit():
      solution[2] = "digit"
      return solution

   if re.match("^[a-zA-Z]*$", word):
      solution[2] = "ENGLISH" 
      return solution
   # if settings.lemma_source.strip() == "DATABASE":
      # print("################################################################### DATABASE ###################################################################")
      # return "RESULTING "
   # elif settings.lemma_source.strip() == "DIC":
   if word in settings.div_dic.keys():
      solution[1] = settings.div_dic[str(word)][1]
      solution[2] = settings.div_dic[str(word)][2]
      return solution 
   if re.sub('[ﻩ]$','ﺓ',word) in settings.div_dic.keys():
      word_with_taa = re.sub('[ﻩ]$','ﺓ',word)
      solution[1] = settings.div_dic[word_with_taa][1]
      solution[2] = settings.div_dic[word_with_taa][2] 
      return solution
   if word_undiac in settings.div_dic.keys():
      solution[1] = settings.div_dic[word_undiac][1]
      solution[2] = settings.div_dic[word_undiac][2] 
      return solution
   if word_with_unify_alef in settings.div_dic.keys():
      solution[1] = settings.div_dic[word_with_unify_alef][1]
      solution[2] = settings.div_dic[word_with_unify_alef][2]
      return solution
   if len(re.sub('^[ﻝ]','',re.sub('^[ﺍ]','',word))) > 5 and re.sub('^[ﻝ]','',re.sub('^[ﺍ]','',word)) in settings.div_dic.keys():
      word_without_al = re.sub('^[ﻝ]','',re.sub('^[ﺍ]','',word))
      solution[1] = settings.div_dic[word_without_al][1]
      solution[2] = settings.div_dic[word_without_al][2]
      return solution 
   return [word,word+"_0",""]


def lemmatize_sentence(sentence):
   output_list = []
   sentence_list = []
   sentence_list = simple_word_tokenize(sentence)
   for word in sentence_list:
      output_list.append(lemmatize_word(word)) 
   return output_list