# -*- coding: utf-8 -*-
# Created by Mohammad A'bed - 24/3/2021
# Trello task: https://trello.com/c/QDkwNQsQ/27-arstrip-function
import re


# This function can be used to clean Arabic word by removing unnecessary diacritics, digits, hamzes, and dashes
# If input is None or any exception happen then the function will return the input
# Example:
# arStrip( "هذَّا " ,False ,True ,False ,False ,False , False ) >> To remove only diacs 

# we need to replace some of the small Quranic annotation signs by range: (06D6 - 06ED).
# See all the Arabic Unicode range from the article (https://www.unicode.org/charts/PDF/U0600.pdf)

def arStrip(input_str , diacs , smallDiacs , shaddah ,  digit , alif , specialChars ):
    """
    Remove Arabic diacritics, Quranic annotation signs, digits, and special characters from a given input string.
    The function also unifies the different forms of alif (أ, إ, آ, ٱ) with hamzah.

    Args:
    input_str (str): The input string to be stripped from diacritics, Quranic annotation signs, digits, and special characters.
    diacs (bool): If True, remove Arabic diacritics [ ًٌٍَُِْ] and SUKUN.
    smallDiacs (bool): If True, remove all small Quranic annotation signs.
    shaddah (bool): If True, remove shaddah.
    digit (bool): If True, remove English and Arabic digits.
    alif (bool): If True, unify alif with hamzah (أ, إ, آ, ٱ) with alif (ا).
    specialChars (bool): If True, remove some special characters.

    Returns:
    str: The input string stripped from diacritics, Quranic annotation signs, digits, and special characters.
    """
    try:
        if input_str: # if the input string is not empty do the following
            #print("in if")
            if diacs == True :
                input_str = re.sub(r'[\u064B-\u0650]+', '',input_str) # Remove all Arabic diacretics [ ًٌٍَُِْ]
                input_str = re.sub(r'[\u0652]+', '',input_str) # Remove SUKUN
            if shaddah == True:
                input_str = re.sub(r'[\u0651]+', '',input_str) # Remove shddah
            if smallDiacs == True:
                input_str = re.sub(r'[\u06D6-\u06ED]+', '',input_str) # Remove all small Quranic annotation signs
            if digit == True:
                input_str = re.sub('[0-9]+', ' ',input_str) # Remove English digits
                input_str = re.sub('[٠-٩]+', ' ',input_str)# Remove Arabic digits
            
            if alif == True:                             # Unify alif with hamzah: 
                input_str = re.sub('ٱ', 'ا',input_str);
                input_str = re.sub('أ', 'ا',input_str);
                input_str = re.sub('إ', 'ا',input_str);
                input_str = re.sub('آ', 'ا',input_str);
            if specialChars == True:
                input_str = re.sub('[?؟!@#$%-]+' , '' , input_str) # Remove some of special chars 

            input_str = re.sub('[\\s]+'," ",input_str) # Remove all spaces
            input_str = input_str.replace("_" , '') #Remove underscore
            input_str = input_str.replace("ـ" , '') # Remove Arabic tatwelah
            input_str = input_str.strip() # Trim input string
    except:
        return input_str
    return input_str
    
    
def removePunctuation( inputString ):
    """
    Removes punctuation marks from the input string.
    
    Args:
    inputString (str): The input string containing punctuation marks.
    
    Returns:
    str: The output string with all punctuation marks removed.
    
    Raises:
    None
    """
    outputString = inputString
    try:
        if inputString:
            # English Punctuation
            outputString = re.sub(r'[\u0021-\u002F]+', '',inputString) # ! " # $ % & ' ( ) * + ,  - . /
            outputString = re.sub(r'[U+060C]+', '',outputString) # ! " # $ % & ' ( ) * + ,  - . /
            outputString = re.sub(r'[\u003A-\u0040]+', '',outputString) # : ; < = > ? @ 
            outputString = re.sub(r'[\u005B-\u0060]+', '',outputString) # [ \ ] ^ _ `
            outputString = re.sub(r'[\u007B-\u007E]+', '',outputString) # { | } ~
            # Arabic Punctuation
            outputString = re.sub(r'[\u060C]+', '',outputString) # ،
            outputString = re.sub(r'[\u061B]+', '',outputString) # ؛
            outputString = re.sub(r'[\u061E]+', '',outputString) # ؞
            outputString = re.sub(r'[\u061F]+', '',outputString) # ؟
            outputString = re.sub(r'[\u0640]+', '',outputString) # ـ
            outputString = re.sub(r'[\u0653]+', '',outputString) # ٓ
            outputString = re.sub(r'[\u065C]+', '',outputString) #  ٬
            outputString = re.sub(r'[\u066C]+', '',outputString) #  ٜ 
            outputString = re.sub(r'[\u066A]+', '',outputString) # ٪
            outputString = re.sub(r'["}"]+', '',outputString) 
            outputString = re.sub(r'["{"]+', '',outputString) 
            # outputString = re.sub(r'[\u066B]+', '',outputString) # ٫ 
            # outputString = re.sub(r'[\u066D ]+','',outputString) # ٭
            # outputString = re.sub(r'[\u06D4 ]+','',outputString) # ۔
    except:
        return inputString
    # print(outputString)
    return outputString

def removeEnglish( inputString ):
    """
    Removes all English characters from the input string.

    Args:
    - inputString (str): The string to remove English characters from.

    Returns:
    - outputString (str): The input string with all English characters removed.
    If an error occurs during processing, the original input string is returned.
    """
    try:
        if inputString:
            inputString = re.sub('[a-zA-Z]+', ' ',inputString)
    except:
        return inputString
    return inputString
# print(removeEnglish("miojkdujhvaj1546545spkdpoqfoiehwv nWEQFGWERHERTJETAWIKUYFC"))
# print(removePunctuation("te!@#،$%%؟st") )
# Example
# print(arStrip( " مَحًمٌٍُِ" ,True ,True ,True ,True ,False , True ))

