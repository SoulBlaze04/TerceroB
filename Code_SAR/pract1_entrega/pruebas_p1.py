import re
import sys
from typing import Optional, Text
from os.path import isfile

def translate_word(word:Text) -> Text:
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """

        # new_word = word SUSTITUIR ESTA PARTE
        mayuscula = word.isupper()
        primeraMayuscula = word[0].isupper()
        primeraSimbolo = not(word[0].isalpha())

        if(primeraSimbolo):
            new_word = word
        else:
            word = word.lower()
            if(word[0] == "a" or word[0] == "e" or word[0] == "i" or word[0] == "o" or word[0] == "u" or word[0] == "y"):
                new_word = word + "yay"
            else:
                aux_string = ""
                while not(word[0] == "a" or word[0] == "e" or word[0] == "i" or word[0] == "o" or word[0] == "u"):
                    aux_string += word[0]
                    word = word[1:]
                
                new_word = word + aux_string + "ay"
            
            if mayuscula: new_word = new_word.upper()
            elif primeraMayuscula: new_word = new_word.capitalize()
            
        
        return new_word

print(translate_word("Spam"))
print(translate_word("SPAM"))
print(translate_word("Egg"))
print(translate_word("EGG"))
print(translate_word("egg"))
print(translate_word("spam"))
print(translate_word("4G"))
print(translate_word(input("Introduce una palabra: ")))