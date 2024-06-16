#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin - Alma Salmerón Sena

import re
import sys
from typing import Optional, Text
from os.path import isfile

class Translator():

    def __init__(self, punt:Optional[Text]=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            punt = ".,;?!"
        self.re = re.compile(r"(\w+)([" + punt + r"]*)")

    def translate_word(self, word:Text) -> Text:
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """

        # new_word = word SUSTITUIR ESTA PARTE

        # Comprueba si toda la palabra está en mayúsculas
        mayuscula = word.isupper()

        # Comprueba si sólo la primera letra está en mayúsuclas
        primeraMayuscula = word[0].isupper()

        # Pasa toda la palabra a minúsculas
        word = word.lower()

        # Si empieza por vocal ó y añade yay
        if(word[0] == "a" or word[0] == "e" or word[0] == "i" or word[0] == "o" or word[0] == "u" or word[0] == "y"):
            new_word = word + "yay"
        
        # Si no empieza por vocal
        else:
            aux_string = ""

            # Mientras no se encuente una vocal va almacenando las letras en un string auxiliar
            while not(word[0] == "a" or word[0] == "e" or word[0] == "i" or word[0] == "o" or word[0] == "u"):
                aux_string += word[0]
                word = word[1:]
            
            # Cuando encuentra una vocal reconstruye la palabra con las letras al final y añade ay
            new_word = word + aux_string + "ay"
        
        # Si la palabra original estaba toda en mayúsculas pone la nueva palabra en mayúsculas
        if mayuscula: new_word = new_word.upper()

        # Si la palabra original empezaba en mayúscula pone la primera letra de la nueva palabra en mayúscula
        elif primeraMayuscula: new_word = new_word.capitalize()
        
        return new_word

    def translate_sentence(self, sentence:Text) -> Text:
        """
        Recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        # new_sentence = sentence SUSTITUIR ESTA PARTE

        # Crea una lista de las palabras que conforman la frase usando el split redefinido en __init__
        words = self.re.split(sentence)

        # Para cada palabra en words
        for i in range(0, len(words)):

            # Crea una nueva palabra en la que guarda la palabra para una posición dada
            palabra = words[i]

            # Elimina espacios innecesarios
            palabra = palabra.replace(" ", "")

            if (palabra == ""):
                palabra = " "
            
            # Comprueba si el primer caracter es una letra y, si no lo es, deja la palabra sin cambiarla
            # De esta forma también se respetan los signos de puntuación
            elif (not(palabra[0].isalpha())):
                palabra = words[i]
            
            # Siendo una palabra que comienza por una letra, llama al método para traducir la palabra
            else:
                palabra = self.translate_word(palabra)
            
            # Vuelve a guardar la palabra en la lista
            words[i] = palabra
       
       # Construye una nueva frase con las palabras traducidas y la devuelve
        new_sentence = "".join(words).strip()
        return new_sentence

    def translate_file(self, filename:Text):
        """
        Recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: None
        """
        # Busca el último punto en el texto del fichero para sacar la extensión (variable ext)
        n = filename.rfind(".")
        ext = filename[n:]

        # Guarda en la variable new_filename el nombre del fichero en el que se guardará la traducción
        new_filename = filename[0:n] + "_latin" + ext

        if not isfile(filename):
            print(f'{filename} no existe o no es un nombre de fichero', file=sys.stderr)

        # COMPLETAR
        # Abre el archivo de entrada (ifile) y de salida (ofile)
        with (open(filename, 'r', encoding = 'utf-8') as ifile, open(new_filename, 'w', encoding = 'utf-8') as ofile):

            # Para cada línea en el fichero de entrada
            for line in ifile:

                # Elimina espacios y \n innecesarios
                line = line.strip()
                
                # Llama al método que permite traducir la frase y guarda el resultado en new_line
                new_line = self.translate_sentence(line)

                #Escribe new_line en el fichero de salida
                ofile.write(new_line)
                ofile.write("\n")
            
            ifile.close()
            ofile.close()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f'Syntax: python {sys.argv[0]} [filename]')
        exit()
    
    t = Translator()
    if len(sys.argv) == 2:
        t.translate_file(sys.argv[1])
    else:
        sentence = input("ENGLISH: ")
        while len(sentence) > 1:
            print("PIG LATIN:", t.translate_sentence(sentence))
            sentence = input("ENGLISH: ")
