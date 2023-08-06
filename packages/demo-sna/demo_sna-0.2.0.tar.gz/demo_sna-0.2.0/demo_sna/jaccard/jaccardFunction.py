# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 14:22:26 2021

@author: Tymaa
"""

import re
from demo_sna.parser import arStrip
from demo_sna.salma.implication import Implication


def normalizeWord(word, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic):
    if ignoreAllDiacriticsButNotShadda:
        word = arStrip(word, True, True, False, False, False, False) # Remove diacs and smallDiacs 
        
    if ignoreShaddaDiacritic:
        word = arStrip(word, False, False, True, False, False, False) # Remove shaddah
    return word
    
def getPreferredWord(word1, word2):
    implication = Implication(word1, word2);
    
    direction = implication.getDirection()
    
    if(direction == 0 or direction == 2 ):         
        return word1
       
    elif direction == 1:
        return word2
       
    elif direction == 3:             
        if (not word1.endswith("َ") and not word1.endswith("ُ")):
            return word2
        return word1
           
    
def getNonPreferredWord(word1, word2):
    # Find non preferred word, if the Distance between the two words input less than 15
    implication = Implication(word1, word2)
    if (implication.getDistance() < 15):
       direction = implication.getDirection()
       if direction == 0 or direction == 1:
          return word1
                    
       elif direction == 2:
          return word2
      
       elif direction == 3:
          if (not word1.endswith("َ") and not word1.endswith("ُ")):
             return word1
          return word2
    return "#"         


def getIntersection(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic):
    # Remove all None and empty values from first list
    list1 = [str(i) for i in list1 if i not in(None,' ','')]
    list1 = [str(i.strip()) for i in list1]
    
    # Remove all None and empty values from second list
    list2 = [str(i) for i in list2 if i not in(None,' ','')]
    list2 = [str(i.strip()) for i in list2]
    
    interectionList = []
    
    # Add all Common words between the two list1 and list2 to interectionList
    for list1_word in list1:
        for list2_word in list2:
            word1 = normalizeWord(list1_word, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            word2 = normalizeWord(list2_word, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
            
            
            implication = Implication(word1, word2)
            if (implication.getDirection() >= 0 and implication.getDistance() < 15):
                interectionList.append(getPreferredWord(word1, word2))
    
    
    i = 0
    while i < len(interectionList):
        j = i + 1
        while j < len(interectionList):
            nonPreferredWord = getNonPreferredWord(interectionList[i], interectionList[j])
            if (nonPreferredWord != "#"):
                interectionList.remove(nonPreferredWord)
            j = j + 1
        i = i + 1
            
    return interectionList              


def getUnion(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic):
    # Remove all None and empty values from first set
    list1 = [str(i) for i in list1 if i not in(None,' ','')]
    
    # Remove all None and empty values from second set
    list2 = [str(i) for i in list2 if i not in(None,' ','')]
    
    unionList = []
    
    # Add all words found in set#1 to union_list
    for list1_word in list1:
        word1 = normalizeWord(list1_word, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
        unionList.append(word1)  
 
    # Add all words found in set#2 to union_list       
    for list2_word in list2:
        word2 = normalizeWord(list2_word, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
        unionList.append(word2)  
    
    # Remove redundant words, by using getNonPreferredWord function 
    i = 0
    while i < len(unionList):
        j = i + 1
        while j < len(unionList):
            nonPreferredWord = getNonPreferredWord(unionList[i], unionList[j]) 
            if (nonPreferredWord != "#"):
                unionList.remove(nonPreferredWord)
            j = j + 1
        i = i + 1     
    return unionList        


def jaccardSimilarity(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic):
    # Find the intersection between two sets
    intersectionList = getIntersection(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
    
    # Find the union between two sets
    unionList = getUnion(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
    
    # calculate the jaccard similarity by divide length of intersectionList on length of union list 
    return float(len(intersectionList)) / float(len(unionList))    


def jaccardFunction(delimiter,str1,str2, selection,ignoreAllDiacriticsButNotShadda,ignoreShaddaDiacritic):
  try: 

   
   # delimiter = d['delimiter']
   
   # str1 = d['string1']
   list1 = str1.split(delimiter)
   
   # # str2 = d['string2']
   list2 = str2.split(delimiter)

   # ignoreAllDiacriticsButNotShadda = d['ignoreAllDiacriticsButNotShadda']
   # ignoreShaddaDiacritic = d['ignoreShaddaDiacritic']

   # selection = d['selection']
   
   try:
      # If the selection is intersection, the intersection of two sets are return
      if selection == "intersection":
         intersection = getIntersection(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
         return  intersection
         

      # If the selection is union, the union of two sets are return
      elif selection == "union":
         union = getUnion(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
         return union
         # content = {"resp": union, "statusText":"OK","statusCode":0}
         # return JsonResponse(content, safe=False, json_dumps_params={'ensure_ascii': False})   

      # If the selection is jaccardSimilarity, the similarity of two sets are return
      elif selection == "jaccardSimilarity":      
         similarity = jaccardSimilarity(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
         return similarity
         # content = {"resp": similarity, "statusText":"OK","statusCode":0}
         # return JsonResponse(content, safe=False, json_dumps_params={'ensure_ascii': False})   

      # If the selection is jaccardAll, then the similarity, Union, and intersection are return 
      elif selection == "jaccardAll":    
         intersection = getIntersection(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
         union = getUnion(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
         similarity = jaccardSimilarity(list1, list2, ignoreAllDiacriticsButNotShadda, ignoreShaddaDiacritic)
         output_list = ["intersection:", intersection, "union:", union, "similarity:", similarity]
         return output_list
         # content = {"resp": output_list , "statusText":"OK","statusCode":0}
         # return JsonResponse(content, safe=False, json_dumps_params={'ensure_ascii': False})   
      
   except:
      return{"statusText":"Error !!","statusCode":"-6"}    
  except:
      return {"statusText":"Incorrect API parameter value","statusCode":"-4"}     
