import pickle
from demo_sna.morph import settings 
import re
from demo_sna.morph.lemmatizeSentence import lemmatize_sentence
from demo_sna.morph.tokenizers_words import simple_word_tokenize
from demo_sna.parser import arStrip

# def load_ALMA_dic():
#    # Open the Pickle file in binary mode
#    with open('demo\ALMA_dic_testing.pickle', 'rb') as f:
#        #Load the serialized data from the file
#        ALMA_dic = pickle.load(f)
#        print(ALMA_dic)
#        return ALMA_dic
   
# def lockup_lemma(word):
#    if word in settings.div_dic.keys():
#        # form, pos_ar, lemma, lemma_freq
#        result_word = [word, settings.div_dic[word][1][1], settings.div_dic[word][1][0], settings.div_dic[word][1][2]] 
#    else:
#       result_word = []
#    return result_word

def load_ALMA_dic(file_path):
    """
    Load the ALMA dictionary from a binary pickle file.

    Args:
    - file_path: str - The path of the binary pickle file containing the ALMA dictionary.

    Returns:
    - dict: A dictionary containing the ALMA dictionary data.

    Raises:
    - FileNotFoundError: If the file specified in file_path cannot be found.
    - pickle.UnpicklingError: If an error occurred while unpickling the data.
    """
    try:
        with open(file_path, 'rb') as f:
            ALMA_dic = pickle.load(f)
            return ALMA_dic
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        raise e
    except pickle.UnpicklingError as e:
        print("Error while unpickling the data.")
        raise e
# def lookup_lemma(word):
#     """
#     Looks up a given Arabic word in a dictionary to find its lemma (root form), part of speech, and frequency.
#     The dictionary used is stored in settings.div_dic, which is a dictionary where keys are words and values are
#     lists of [form, pos_ar, lemma, lemma_freq]. If the word is not found in the dictionary, an empty list is returned.

#     Args:
#         word (str): The Arabic word to be looked up in the dictionary.

#     Returns:
#         list: A list of [word, lemma, pos_ar, lemma_freq], where:
#             - word: the original input word
#             - lemma: the lemma (root form) of the word, if found in the dictionary
#             - pos_ar: the part of speech of the word in Arabic, if found in the dictionary
#             - lemma_freq: the frequency of the lemma in the dictionary, if found
#             If the word is not found in the dictionary, an empty list is returned.
#     """
#     if word in settings.div_dic:
#         form, pos_ar, lemma, lemma_freq = settings.div_dic[word]
#         result_word = [word, lemma, pos_ar, lemma_freq]
#     else:
#         result_word = []
#     return result_word

def lookup_lemma(word, lang, task):
    """
    Looks up a given Arabic word in a dictionary to find its lemma, part of speech, and frequency,
    filtered by the specified language and task. The dictionary used is assumed to be a nested dictionary where keys
    are words and values are lists of lemma entries, where each lemma entry is a list of the form
    [form_id, form, pos_ar, lemma, lemma_freq, lang, task].

    Args:
        word (str): The Arabic word to be looked up in the dictionary.
        lang (str): The language to filter the results by [MSA, Pal, ].
        task (str): The task to filter the results by [lemmatizer, pos, full].

    Returns:
        list: A list of [word, lemma, pos_ar, lemma_freq, lang, task], where:
            - word: the original input word
            - lemma: the lemma of the word, if found in the dictionary
            - pos_ar: the part of speech of the word in Arabic, if found in the dictionary
            - lemma_freq: the frequency of the lemma in the dictionary, if found
            - lang: the language of the lemma entry, if found and matching the specified language
            - task: the task of the lemma entry, if found and matching the specified task
            If the word is not found in the dictionary, an empty list is returned.
    """
    #settings.div_dic = load_ALMA_dic(r'C:\Users\Alaa\Documents\demo\demo\demo\dic_data\ALMA_dic_first_500records_with_language_and_task.pickle')
    # return settings.div_dic
    if word in settings.div_dic.keys():

        soluation =settings.div_dic[word][1]
        if task =='full' and soluation[-2] == lang:
            return  [word, soluation[3], soluation[2],  soluation[-2], soluation[-1]]
        elif soluation[-2] == lang and soluation[-1] ==task:
            return [word, soluation[3], soluation[2],  soluation[-2], soluation[-1]]
       # for entry in settings.div_dic[word][1]:
        #     if entry[-2] == lang and entry[-1] == task:
        #         return [word, entry[3], entry[2], entry[4], entry[-2], entry[-1]]
        return []
    else:
        return []

# databse to be deleted
# internal use 
# def getLemma(sentence, task):
#    settings.lemma_source = "DATABASE"
#    sentence_list = []
#    output_list = [] 
#    sentence_list = simple_word_tokenize(sentence) # tokenization of the sentence
#    for word in sentence_list:   
#       word = word.strip()
#       solution = [word,word+"_0",""] # not in the dictionary  
#       word_undiac = re.sub(r'[\u064B-\u0650]+', '',word) # Remove all Arabic diacretics [ ًَ]
#       word_undiac = re.sub(r'[\u0652]+', '',word_undiac) # Remove SUKUN
#       word_undiac = re.sub(r'[\u0651]+', '',word_undiac) # Remove shddah
#       word_undiac = re.sub('[\\s]+',' ',word_undiac)
#       word_with_unify_alef = re.sub('[أ]','ا',word)
#       word_with_unify_alef = re.sub('[ﺇ]','ا',word_with_unify_alef)
#       word_with_unify_alef = re.sub('[ٱ]','ا',word_with_unify_alef)
#       word_with_unify_alef = re.sub('[ﺃ]','ا',word_with_unify_alef)
#       word_with_unify_alef = re.sub('[ﺁ]','ا',word_with_unify_alef)
      
#       # queryset = models.Lemmatization.objects.all().filter(form=word)
#       # JsonLemma = serializers.serialize('json', queryset) # convert queryset to json
#       # j = json.loads(JsonLemma)        # Convert list to json, We can use >> queryset.lemma_id , "\t" , queryset.pos_en , "\t" , queryset.lemma  to return as string
#       result_word = json.loads(serializers.serialize('json',models.Lemmatization.objects.filter(inALMA__isnull=True).filter(form=word)))
#       result_word_without_taa = json.loads(serializers.serialize('json',models.Lemmatization.objects.filter(inALMA__isnull=True).filter(form=re.sub('[ﻩ]$','ﺓ',word))))
#       result_word_undiac = json.loads(serializers.serialize('json',models.Lemmatization.objects.filter(inALMA__isnull=True).filter(form=word_undiac)))
#       result_word_with_unify_alef = json.loads(serializers.serialize('json',models.Lemmatization.objects.filter(inALMA__isnull=True).filter(form=word_with_unify_alef)))
#       result_word_without_al = json.loads(serializers.serialize('json',models.Lemmatization.objects.filter(inALMA__isnull=True).filter(form=re.sub('^[ﻝ]','',re.sub('^[ﺍ]','',word)))))

#       if word.isdigit():
#          #print("digit")
#          solution[2] = "digit"
#          output_list.append(solution)
      
#       elif re.match("^[a-zA-Z]*$", word):
#          #print("English")
#          solution[2] = "ENGLISH" 
#          output_list.append(solution)

#       elif result_word != []:
#          #print("word ")
#          solution[1] = result_word[0]['fields']['lemma']
#          solution[2] = result_word[0]['fields']['POS']
#          output_list.append(solution)
      
#       elif result_word_without_taa != [] :
#          #print("word with taa")
#          solution[1] = result_word_without_taa[0]['fields']['lemma']
#          solution[2] = result_word_without_taa[0]['fields']['POS']
#          output_list.append(solution)

#       elif result_word_undiac != []:
#          #print("word with undiac")
#          solution[1] = result_word_undiac[0]['fields']['lemma']
#          solution[2] = result_word_undiac[0]['fields']['POS']
#          output_list.append(solution)

#       elif result_word_with_unify_alef != []:
#          #print("word with unify alef")
#          solution[1] = result_word_with_unify_alef[0]['fields']['lemma']
#          solution[2] = result_word_with_unify_alef[0]['fields']['POS']
#          output_list.append(solution)

#       elif len(re.sub('^[ﻝ]','',re.sub('^[ﺍ]','',word))) > 5 and result_word_without_al != []:
#          #print("word with Al ta3reef")
#          solution[1] = result_word_without_al[0]['fields']['lemma']
#          solution[2] = result_word_without_al[0]['fields']['POS']
#          output_list.append(solution)
#       else:
#          solution = [word,word+"_0",""]
#          output_list.append(solution)
      
#    content = {"resp": output_list,"statusText":"OK","statusCode":0}
#    return content 
#    #return JsonResponse(j[0]) 
  
def lemmatize_sentence(sentence ,lang, task):
   """
    This function takes in a sentence and returns a list of lemmatized words with their corresponding
    part-of-speech (POS) tags and lemma frequencies. It uses Arabic-specific lemmatization techniques
    to handle different forms of Arabic words.

    Args:
    - sentence (str): The input sentence to be lemmatized.
    - task (str): The type of task being performed (e.g., 'POS tagging', 'text classification').
    - lang (str): The language of the input sentence (e.g., 'Arabic', 'English').

    Returns:
    - output_list (list): A list of lemmatized words with their corresponding POS tags and lemma frequencies.

    """
   output_list = []
   # tokenize sentence into words
   words = simple_word_tokenize(sentence)
   # for each word 
   for word in words:
         result_word =[]
         # Trim spaces 
         word = word.strip()
         # Remove smallDiac
         word = arStrip(word , False , True , False , False , False , False) 
         # Unify ٱ 
         word = re.sub('[ٱ]','ﺍ',word)
         # Initialize solution [word, lemma, pos]
         solution = [word,word+"_0","",0]
         
         # if word is digit, update pos to be digit 
         if word.isdigit():
            solution[2] = "digit"

         # if word is english, update pos to be ENGLISH
         elif re.match("^[a-zA-Z]*$", word):
            solution[2] = "ENGLISH"

         else:
            # search for a word (as is) in ALMA dictionary   
            result_word = lookup_lemma(word,lang, task)
            
            if len(re.sub(r'^[ﻝ]','',re.sub(r'^[ﺍ]','',word))) > 5 and result_word == []:
               # try with remove remove AL
               result_word = lookup_lemma(re.sub(r'^[ﻝ]','',re.sub(r'^[ﺍ]','',word)), lang, task)

            if result_word == []:
              # try with replace ﻩ with ﺓ
               result_word = lookup_lemma(re.sub(r'[ﻩ]$','ﺓ',word), lang, task)

            if result_word == []:
               # try with unify Alef
               word_with_unify_alef = arStrip(word , False , False , False , False , True , False) # Unify Alef
               result_word = lookup_lemma(word_with_unify_alef, lang, task)
            
            if result_word == []:
               # try with remove diac
               word_undiac = arStrip(word , True , False , True , True , False , False) # remove diacs, shaddah ,  digit
               result_word = lookup_lemma(word_undiac, lang, task)

            if result_word == []:
               # try with remove diac and unify alef
               word_undiac = arStrip(word , True , True , True , False, True , False) # diacs , smallDiacs , shaddah ,  alif
               result_word = lookup_lemma(word_undiac, lang, task)
         
         if result_word != []:
               # if solution found
               tmp_solution = [word,word+"_0","",0]               
               tmp_solution[1] = result_word[2] # lemma
               tmp_solution[2] = result_word[1] # pos_ar
               tmp_solution[3] = result_word[3] # lemma_freq
               output_list.append(tmp_solution)
         else:
            # if no solution is found
            output_list.append(solution)
   return output_list               
        
def tagger(sentence: str, task = 'full', lang = 'MSA') -> list:
    """
    This function performs morphological analysis and tagging on a given Arabic sentence.
    
    Args:
        sentence (str): The input Arabic sentence to be morphologically analyzed and tagged.
        task (str): The type of morphological analysis and tagging to be performed. Default is 'full'.
        lang (str): The language of the input sentence. Default is 'MSA' (Modern Standard Arabic).
        
    Returns:
        list: A list of lists, where each sublist contains information about a word in the input sentence, including 
              the original word, its lemma, its part of speech (POS) tag, and its lemma frequency.
    """
    
    # Check if the ALMA dictionary has been loaded
    # if settings.flag == True:
    #     settings.flag = False
    settings.div_dic = load_ALMA_dic(r'~\demo_sna\dic_data\ALMA_dic_first_500records_with_language_and_task.pickle')
   
    
    # Perform lemmatization on the input sentence
    output_list = lemmatize_sentence(sentence,lang, task)
    
    # Return the list of lemmatized words
    return output_list

# def x():
#     settings.div_dic= load_ALMA_dic(r'C:\Users\Alaa\Documents\demo\demo\demo\dic_data\ALMA_dic_first_500records_with_language_and_task.pickle')


# [[word, lemma, pos, lemma_freq]]

# def morph_tagger(sentence, task='full', lang='MSA'):
#    if settings.flag == True:
#       settings.flag = False
#       settings.div_dic = load_ALMA_dic()
#    output_list = []
#    output_list = lemmatize_sentence(sentence, task, lang)
#    return output_list

  
  
  
  
  
# print("Load ALMA dictionary")
# ALMA_dic = load_ALMA_dic()

# sentence = "ذهب الأولاد إلى المدارس." 
# task = "lemmatizer"
# language = "MSA"
# morph_tagger(sentence, task, language)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    
    
    
    
    
