# ./bookstore_app/api/views.py
import django
django.setup()
import requests
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from salma import settings 
# Comented by tymaa to Run service via GPU
#from salma.word_sense_disambiguation import word_sense
from salma.word_sense_disambiguation import normalizearabert
from salma.word_sense_disambiguation import load_data_model
from salma.word_sense_disambiguation import GlossPredictor
from salma.parser import arStrip
from salma.parser import removePunctuation
from salma.parser import removeEnglish
from salma.tokenizers_words import simple_word_tokenize
from ALMA_multi_word_service.views import ALMA_multi_word
import re
import numpy as np
from arabiner.bin import infer
from api_clients_counter_month.ApikeyValidation import checkApikey
from ApiTrackingService.InsertApiLog import insertLog
import multiprocessing
from functools import partial
from lemmatizer_v2_DB.views import lemmatize_sentence
from arabiner.views import NER

# Added By Tymaa: 2023-02-05 to call GlossPredictor as a web service from GPU machine 
#from urllib.request import Request, urlopen

def delete_form_list(position, word_lemma):
    tmp_word_lemma = [] 
    output = []
    for wordLemma in word_lemma:
        if position == int(wordLemma[2]): # start 
           word = wordLemma[0]
           gloss = wordLemma[1]
           position = int(wordLemma[3]) 
           concept_count = int(wordLemma[4]) 
           undiac_multi_word_lemma = wordLemma[5]
           multi_word_lemma = wordLemma[6]
           output.append([word, gloss, concept_count, undiac_multi_word_lemma, multi_word_lemma])# word
        elif position < int(wordLemma[2]): 
           tmp_word_lemma.append(wordLemma)
    return tmp_word_lemma, output, position
    #return output

def find_two_word_lemma(input_sentence):
    i = 0
    output = []
    length = len(input_sentence)
    while i < length - 1:
        two_grams = input_sentence[i] +" "+ input_sentence[i + 1] 
      #   r = requests.get("https://ontology.birzeit.edu/sina/v2/api/ALMA_multi_wordDB/"+two_grams+"?apikey=samplekey", verify=False)
      #   data = json.loads(r.text)
        data = ALMA_multi_word(two_grams,2)
        try :
            # found two_grams
            found_2Word_lemma = [two_grams,data[0]['glosses'], i, i + 1,data[0]['concept_count'], data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
            output.append(found_2Word_lemma) 
            i = i + 1    
        except: # no record found on this multi_lema
            i = i + 1 
    return output


def find_three_word_lemma(input_sentence):
    i = 0
    output = []
    length = len(input_sentence)
    while i < length - 2:
        three_grams = input_sentence[i] +" "+ input_sentence[i + 1] + " "+ input_sentence[i + 2]
        #r = requests.get("https://ontology.birzeit.edu/sina/v2/api/ALMA_multi_wordDB/"+three_grams+"?apikey=samplekey", verify=False)
        #data = json.loads(r.text) 
        data = ALMA_multi_word(three_grams,3)
        try:
           found_3Word_lemma = [three_grams, data[0]['glosses'], i, i + 2,data[0]['concept_count'], data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
           output.append(found_3Word_lemma) 
           i = i + 1    
        except:  
           i = i + 1 
    return output

def find_four_word_lemma(input_sentence):
   i = 0
   output = []
   length = len(input_sentence)
   while i < length - 3:
      four_grams = input_sentence[i] +" "+ input_sentence[i + 1] + " "+ input_sentence[i + 2] + " "+ input_sentence[i + 3]
      data = ALMA_multi_word(four_grams,4)
      try:
         found_4Word_lemma = [four_grams, data[0]['glosses'], i, i + 3,data[0]['concept_count'], data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
         output.append(found_4Word_lemma) 
         i = i + 1    
      except:  
         i = i + 1 
   return output


def find_five_word_lemma(input_sentence):
   i = 0
   output = []
   length = len(input_sentence)
   while i < length - 4:
      five_grams = input_sentence[i] +" "+ input_sentence[i + 1] + " "+ input_sentence[i + 2] + " "+ input_sentence[i + 3] + " "+ input_sentence[i + 4]
      data = ALMA_multi_word(five_grams,5)
      try:
         found_5Word_lemma = [five_grams, data[0]['glosses'], i, i + 4,data[0]['concept_count'], data[0]['undiac_multi_word_lemma'], data[0]['multi_word_lemma']]
         output.append(found_5Word_lemma) 
         i = i + 1    
      except:  
         i = i + 1 
   return output

def find_named_entities(string):
   found_entities = []
   entites = NER(string, "4")
   tag_gloss = {
      "PERS": "اسم شخص",
      "ORG": "اسم مؤسسة",
      #"NORP": "مجموعة من الناس", 
      #"OCC": "منصب/مسمى وظيفي",
      "LOC": "اسم منطقة جغرافية",
      "FAC": "اسم لمَعلَم",
      #"EVENT": "حدث",
      "DATE": "فترة زمنية تدل على تاريخ",
      "UNIT": "وحدة قياس",
      "CURR": "عملة",
      "GPE": "اسم بلد، له حدود إدارية/جيوسياسية",
      "TIME": "فترة زمنية تدل على الوقت",
      "CARDINAL": "عدد يدل على معدود",
      "ORDINAL": "رقم، لا يدل على معدود",
      "PERCENT": "نسبة مئوية",
      "QUANTITY": "كمية",
      "MONEY": "مبلغ مالي",
      "LANGUAGE": "اسم للغة طبيعية",
      "PRODUCT": "اسم منتج",
      "LAW": "قانون"
   }

   for entity in entites:
      gloss_ner = ""
      if entity[1] in tag_gloss.keys():
         gloss_ner = tag_gloss[entity[1]]  

      if gloss_ner != "":
         gloss = [{'concept_id': '', 'resource_id': '', 'resource_name': '', 'gloss': gloss_ner}]   
         entity = [entity[0],gloss,int(entity[2]), int(entity[3]),1,arStrip(entity[0],True,True,True,False,True,False),entity[0]]   
         found_entities.append(entity)
   #print("list : ",found_entities)
   return found_entities   


def find_glosses_using_ALMA(word):
   #r = requests.post('https://ontology.birzeit.edu/sina/v2/api/ALMADB/', json= {"sentence":word}, verify=False)
   #data = json.loads(r.text)
   data = lemmatize_sentence(word)
   Diac_lemma = ""
   pos = ""
   Undiac_lemma = ""
   glosses = []
   #for values in data['resp']: ### Think about bugs in lemmatizer .ex: connection error...
   Diac_lemma = data[0][1]
   pos = data[0][2]
   Undiac_lemma = arStrip(Diac_lemma, True, True, True, True, True, False) # Remove diacs , smallDiacs , shaddah ,  digit , alif , specialChars
   glosses = data[0][4]
   concept_count = data[0][3]
   return word, Undiac_lemma, Diac_lemma, pos , concept_count, glosses
   
def disambiguate_glosses_using_SALMA(glosses, Diac_lemma, Undiac_lemma, word, sentence):
   word = normalizearabert(word)
   #print(" word After normalized : ", word)
   glosses_dictionary = {}
   if glosses != None:
      for gloss in glosses:
         # result = json.loads(gloss)
         glosses_dictionary.update({gloss['concept_id'] : gloss['gloss']})
      # Commented by Tymaa (2023-02-05) to call GlossPredictor as a web service from GPU machine 
      print(" Before GlossPredictor on word = ", word)
      concept_id, gloss = GlossPredictor(Diac_lemma, Undiac_lemma,word,sentence,glosses_dictionary)
      print(" After GlossPredictor on word = ", word, " Concept_id : ", concept_id, " gloss : ", gloss)


      # Added By Tymaa: 2023-02-05 to call GlossPredictor as a web service from GPU machine 
      #data = {}
      #data["Diac_lemma"] = Diac_lemma 
      #data["Undiac_lemma"] = Undiac_lemma
      #data["word"] = word
      #data["sentence"] = sentence
      #data["glosses_dictionary"] = glosses_dictionary
      #print("Data : ", data)
      #data = json.dumps(data).encode('utf8')
      #req = Request(
      #      url="http://185.19.228.221:8000/word_sense_disambiguation/",
      #      data=data,
      #      headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
      #      method='POST'
      #)
      #print("url decode : ", urlopen(req).read().decode())
      #webpage = urlopen(req).read().decode()
      #concept_id = json.loads(webpage)['concept_id']
      #gloss = json.loads(webpage)['Gloss']

      #url = "http://185.19.228.221:8000/word_sense_disambiguation/"
      
      #data = json.dumps(data).encode('utf8')
      #print("encode data: " , data)
      #response = requests.post(url, data=data, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
      #print(response.status_code)
      #if response.status_code == 200:
      #    resp_text = json.loads(response.text)
      #    concept_id = resp_text["concept_id"]
      #    gloss = resp_text["Gloss"]  
      #else:
      #    concept_id = None
      #    gloss = None
      ##

      my_json = {}    
      my_json['Concept_id'] = concept_id
      my_json['Gloss'] = gloss
      my_json['word'] = word
      my_json['Undiac_lemma'] = Undiac_lemma
      my_json['Diac_lemma'] = Diac_lemma
      return my_json
   else:
      #print(" word with gloss = None ", word)
      my_json = {}    
      my_json['word'] = word
      my_json['Undiac_lemma'] = Undiac_lemma
      my_json['Diac_lemma'] = Diac_lemma
      return my_json




def find_glosses(input_sentence, three_word_lemma, two_word_lemma, four_word_lemma, five_word_lemma, ner):
      output_list = []
      position = 0
      while position < len(input_sentence):    
         flag = "False"
         output_from5word = delete_form_list(position, five_word_lemma)
         five_word_lemma = output_from5word[0]
         if output_from5word[1] != []: # output
            position = output_from5word[2]  
            flag = "True"
            my_json = {}    
            my_json['word'] = output_from5word[1][0][0]
            my_json['concept_count'] = output_from5word[1][0][2]
            my_json['glosses'] = output_from5word[1][0][1]
            my_json['Diac_lemma'] = output_from5word[1][0][4]
            my_json['Undiac_lemma'] = output_from5word[1][0][3]
            output_list.append(my_json)
            position = position + 1                



         output_from4word = delete_form_list(position, four_word_lemma)
         four_word_lemma = output_from4word[0]
         if output_from4word[1] != []: # output
            position = output_from4word[2]  
            flag = "True"
            my_json = {}    
            my_json['word'] = output_from4word[1][0][0]
            my_json['concept_count'] = output_from4word[1][0][2]
            my_json['glosses'] = output_from4word[1][0][1]
            my_json['Diac_lemma'] = output_from4word[1][0][4]
            my_json['Undiac_lemma'] = output_from4word[1][0][3]
            output_list.append(my_json)
            position = position + 1                
         
         output_from3word = delete_form_list(position, three_word_lemma)
         three_word_lemma = output_from3word[0]
         if output_from3word[1] != []: # output
            position = output_from3word[2]  
            flag = "True"
            my_json = {}    
            my_json['word'] = output_from3word[1][0][0]
            my_json['concept_count'] = output_from3word[1][0][2]
            my_json['glosses'] = output_from3word[1][0][1]
            my_json['Diac_lemma'] = output_from3word[1][0][4]
            my_json['Undiac_lemma'] = output_from3word[1][0][3]
            output_list.append(my_json)
            position = position + 1                



         output_from2Word = delete_form_list(position, two_word_lemma)
         two_word_lemma = output_from2Word[0] 
         if output_from2Word[1] != []:  
            position = output_from2Word[2]
            flag = "True"
            my_json = {}    
            word = output_from2Word[1][0][0]
            my_json['word'] = word
            my_json['concept_count'] = output_from2Word[1][0][2]
            my_json['glosses'] = output_from2Word[1][0][1]
            my_json['Diac_lemma'] = output_from2Word[1][0][4]
            my_json['Undiac_lemma'] = output_from2Word[1][0][3] 
            output_list.append(my_json)
            position = position + 1                 
               


         output_from_ner = delete_form_list(position, ner)
         ner = output_from_ner[0] 
         if output_from_ner[1] != []:  
            position = output_from_ner[2]
            flag = "True"
            my_json = {}    
            word = output_from_ner[1][0][0]
            my_json['word'] = word
            my_json['concept_count'] = output_from_ner[1][0][2]
            my_json['glosses'] = output_from_ner[1][0][1]
            my_json['Diac_lemma'] = output_from_ner[1][0][4]
            my_json['Undiac_lemma'] = output_from_ner[1][0][3] 
            output_list.append(my_json)
            position = position + 1                             
         
         if flag == "False": # Not found in ner or in multi_word_dictionary, ASK ALMA 
            word = input_sentence[position]
            word, Undiac_lemma, Diac_lemma, pos , concept_count, glosses = find_glosses_using_ALMA(word)   
            my_json = {}    
            my_json['word'] = word
            my_json['concept_count'] = concept_count
            my_json['glosses'] = glosses
            my_json['Diac_lemma'] = Diac_lemma
            my_json['Undiac_lemma'] = Undiac_lemma
            output_list.append(my_json)
            position = position + 1  
      return output_list                    

def disambiguate_glosses_main(word, sentence):
   concept_count = word['concept_count']
   if concept_count == 0:
      print(" word : ", word['word'], " with concept count = 0", concept_count)
      my_json = {}    
      my_json['word'] = word['word']
      my_json['Diac_lemma'] = word['Diac_lemma']
      my_json['Undiac_lemma'] = word['Undiac_lemma']
      return my_json
   elif concept_count == 1:
      print(" word : ", word['word'], " with concept count = 1", concept_count)
      my_json = {}    
      my_json['word'] = word['word']
      #my_json['Gloss'] = word['glosses']
      #glosses = json.loads(word['glosses'][0])
      glosses = word['glosses'][0]
      my_json['Gloss'] = glosses['gloss']
      my_json['Concept_id'] = glosses['concept_id']
      my_json['Diac_lemma'] = word['Diac_lemma']
      my_json['Undiac_lemma'] = word['Undiac_lemma']
      return my_json
   else:   
      print(" word : ", word['word'], " with concept count > 1", concept_count)
      input_word = word['word']
      concept_count = word['concept_count']
      glosses = word['glosses']
      Diac_lemma = word['Diac_lemma']
      Undiac_lemma = word['Undiac_lemma']
      return disambiguate_glosses_using_SALMA(glosses, Diac_lemma, Undiac_lemma, input_word, sentence)

def WSD(sentence):
   
   input_sentence = simple_word_tokenize(sentence)
   
   five_word_lemma = find_five_word_lemma(input_sentence)
   
   four_word_lemma = find_four_word_lemma(input_sentence)
   
   three_word_lemma = find_three_word_lemma(input_sentence)
   
   two_word_lemma = find_two_word_lemma(input_sentence)
   
   ner = find_named_entities(" ".join(input_sentence))
   #ner = []

   output_list = find_glosses(input_sentence, three_word_lemma, two_word_lemma, four_word_lemma, five_word_lemma, ner)
   
   results = []
   #with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
   #    results = pool.map(partial(disambiguate_glosses_main, sentence= sentence), output_list)
   for word in output_list:
      results.append(disambiguate_glosses_main(word, sentence))
   #print("Number of processors: ", mp.cpu_count())   
   #print("After multiProcessing : ", results)
   return results

@api_view(["POST"])
def SALMA(request):
      apikey = "" # defult apikey
      if 'apikey' in request.GET: # check if user entered the apikey
         apikey = request.GET['apikey'] # get apikey from URL request
      else:
         # if no apikey in URL return these message 
         return JsonResponse({"statusText":"User is not authenticated","statusCode":-3} ) 
      body_unicode = request.body.decode('utf-8')
      body = json.dumps(json.JSONDecoder().decode(body_unicode))
      d = json.loads(body)
      sentence = d['sentence']
      
      if len(sentence) > 500:
         content = {"statusText":"Input is too long","statusCode":-7}
         return JsonResponse(content, safe=False, json_dumps_params={'ensure_ascii': False}) 
      else: 
         serviceName = request.path.split("/")[4] # get service_url from request to check if service_groups table contains this url
         insertLog(request) # if apiKey is not null insert log in table api_tracking_logs
         apikeyValidation = checkApikey(apikey , serviceName) # call checkApikey function to check apikey validation and limitation
         if apikeyValidation == True: # if apikey valid, limitation not exceeded, and date has not expired
            #try:
               #print("Start with sentence : ", sentence)
               results = WSD(sentence)
               content = {"resp": results, "statusText":"OK","statusCode":0}
               return JsonResponse(content, safe=False, json_dumps_params={'ensure_ascii': False})  
            #except:
            #   return JsonResponse({"statusText":"Error !!","statusCode":"-1"} )    # Note: check statusCode number ?-1         
         else: # if apikey not valid return error message which came from checkApikey
            return JsonResponse(apikeyValidation)           