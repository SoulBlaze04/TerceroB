#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys
from typing import List, Optional, TextIO

## Nombres: Alma Salmerón Sena, Alberto Olcina Calabuig

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################


def convert_to_lm_dict(d: dict):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]')
        self.r2 = re.compile('\W+')
        self.info = {}

    def get_n(self):
        return self.info.get('n', 0)

    def index_sentence(self, sentence:str):
        n = self.info['n']

        # COMPLETAR #

        # comprueba que la frase que se ha pasado no está vacía 
        if(sentence == ""):
            pass
        else:

            # pasa la frase a minúsculas y elimina los caracteres que no son alfanuméricos
            line = sentence.lower()
            words = self.r2.split(line.strip())

            # itera para cada longitud de n-gramas desde 2 hasta n
            for naux in range(2, n + 1):
                
                # creamos una variable auxiliar que copia words
                auxWords = words[:] 

                # añade naux-1 símbolos $
                for j in range(1, naux):
                    auxWords.insert(0, "$")
        
                # añade un $ al final
                auxWords.append("$")

                # define una variable start y una variable fin que indica qué palabras de words hay que coger para hacer una tupla 
                start = 0
                fin = naux - 1
                auxList = auxWords[start:fin]
                tupla = tuple(auxList)

                # itera para el número de palabras desde la última que hemos cogido en la tupla hasta la última en words
                for k in range(naux, len(auxWords) + 1):

                    # define una variable nextWord, que es la palabra que hay a continuación de las de la tupla
                    nextWord = auxWords[fin]

                    # si es la primera vez que esa tupla aparece, crea una entrada en el diccionario
                    if(self.info['lm'][naux].get(tupla) == None):
                        self.info['lm'][naux][tupla] = {nextWord: 0}

                    # aumenta en uno el contador de apariciones de esa palabra nextWord para la tupla
                    self.info['lm'][naux][tupla][nextWord] = self.info['lm'][naux][tupla].get(nextWord, 0) + 1

                    # incrementa el contador de start y fin y crea una nueva tupla con las palabras que quedan
                    start += 1
                    fin += 1
                    auxList = auxWords[start:fin]
                    tupla = tuple(auxList)

                # ejemplo del funcionamiento de este bucle
                # si words = [patata, tomate, huevo, zanahoria, bacon] y el tamaño de n-grama es 3 hace
                # tupla = (patata, tomate)
                # nextWord = huevo
                # actualiza la información en el diccionario
                # tupla = (tomate, huevo)
                # nextWords = zanahoria
                # ...    


    def compute_lm(self, filenames:List[str], lm_name:str, n:int):
        self.info = {'name': lm_name, 'filenames': filenames, 'n': n, 'lm': {}}
        for i in range(2, n+1):
            self.info['lm'][i] = {}
        for filename in filenames:
            with open(filename, encoding='utf-8') as fh:

                # creamos una variable pass_sentence que acumulará los trozos de frase en distintas líneas para formar la frase completa y pasarla a index_sentence
                pass_sentence = ""

                for line in fh:
                    # COMPLETAR #

                    # separa las frases para cada línea
                    words = self.r1.split(line.strip())
                    
                    # si hay varias entradas en words (es decir, en la misma línea hay más de una frase)
                    if (len(words) > 1):

                        # guardamos el primer elemento (ya que o será una frase entera por sí mismo o pertenecerá a la frase anterior)
                        init = words[0]

                        # guardamos el último elemento porque pertenecerá a la siguiente frase
                        fin = words[len(words)-1]

                        # nos quedamos con todo lo del medio en words
                        words = words[1:len(words)-1]

                        # añadimos el primer elemento a pass_sentence y llamamos a index_sentence para analizar las estadísticas de esa frase
                        pass_sentence += init.strip()
                        self.index_sentence(pass_sentence.strip())

                        # si quedan más elementos en words
                        if(len(words) != 0):

                            # llamamos a index_sentence para cada uno de ellos, ya que serán frases
                            for entry in words:
                                self.index_sentence(entry.strip())
                        
                        # antes de acabar, guardamos fin en pass_sentence
                        pass_sentence = fin
                    
                    # si no hay más de una frase
                    else:
                        # si no es vacío, lo añade a pass_sentence
                        if (words[0] != ''):
                            pass_sentence = pass_sentence + words[0].strip() + " "
                
                # hacemos una última llamada a index_sentence para pasar la última frase acumulada
                self.index_sentence(pass_sentence.strip())
                   
        for i in range(2, n+1):
            convert_to_lm_dict(self.info['lm'][i])

    def load_lm(self, filename:str):
        with open(filename, "rb") as fh:
            self.info = pickle.load(fh)

    def save_lm(self, filename:str):
        with open(filename, "wb") as fh:
            pickle.dump(self.info, fh)

    def save_info(self, filename:str):
        with open(filename, "w", encoding='utf-8', newline='\n') as fh:
            self.print_info(fh=fh)

    def show_info(self):
        self.print_info(fh=sys.stdout)

    def print_info(self, fh:TextIO):
        print("#" * 20, file=fh)
        print("#" + "INFO".center(18) + "#", file=fh)
        print("#" * 20, file=fh)
        print(f"language model name: {self.info['name']}", file=fh)
        print(f'filenames used to learn the language model: {self.info["filenames"]}', file=fh)
        print("#" * 20, file=fh)
        print(file=fh)
        for i in range(2, self.info['n']+1):
            print("#" * 20, file=fh)
            print("#" + f'{i}-GRAMS'.center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for prev in sorted(self.info['lm'][i].keys()):
                wl = self.info['lm'][i][prev]
                print(f"'{' '.join(prev)}'\t=>\t{wl[0]}\t=>\t{', '.join(['%s:%s' % (x[1], x[0]) for x in wl[1]])}" , file=fh)


    def generate_sentences(self, n:Optional[int], nsentences:int=10, prefix:Optional[str]=None):
        # COMPLETAR #

        # generamos tantas frases como nsentences indique
        for y in range(0, nsentences):

            res = ""
            tupla = ()

            # si hay prefijo
            if(prefix is not None):

                # guarda la longitud del prefijo
                words = prefix.split()
                prefLength = len(words)

                # si hay menos palabras en el prefijo que espacio en la tupla
                if (prefLength < n):

                    # añade $ a la tupla hasta que sólo queden los huecos para el prefijo
                    for x in range (0, n - prefLength - 1):
                        tupla = tupla + ("$",)
                
                    # añade el prefijo a la tupla
                    for word in words:
                        tupla = tupla + (word,)
                
                # si hay más o igual de palabras en el prefijo
                else:

                    # guardamos las primeras palabras en la respuesta directamente
                    for token in range(0, prefLength - n + 1):
                        res += words[token]
                        res += " "
    
                    # y guardamos el resto en la tupla
                    words = words[prefLength - n + 1:]

                    for word in words:
                        tupla += (word,)

            
            # si no hay prefijo simplemente hace una tupla llena de $
            else:
                for x in range (0, n - 1):
                    tupla = tupla + ("$",)

            # inicializa una variable limit
            limit = n

            # hace un bucle infinito
            while True:

                # mientras no se supere el límite
                if (limit <= 50):

                    # se inicializa una variable que contendrá la lista entre la que se elegirá
                    choiceList = []
                
                    try:
                        # coge todas las posibles palabras que podrían ser la siguiente
                        possibleNexts = self.info['lm'][n][tupla][1]

                        # para cada palabra
                        for option in possibleNexts:

                            # coge el número de veces que aparece
                            numReps = option[0] 

                            # añade la palabra a la lista el número de veces que aparece
                            for rep in range(0, numReps):
                                choiceList.append(option[1])

                        # elige aleatoriamente una palabra de la lista
                        nextWord = random.choice(choiceList)

                        # si es $, salimos del bucle
                        if nextWord == "$":
                            break
                        
                        # actualiza la tupla guardando en res la palabra descartada
                        else:
                            aux = list(tupla)

                            descarte = aux[0]

                            if descarte != "$":
                                res += descarte
                                res += " "

                            aux = aux[1:]
                            aux.append(nextWord)
                            tupla = tuple(aux)
                            limit += 1

                    # captura la excepción en la que el prefijo no se encuentra
                    except KeyError:
                        print("El prefijo no es válido")
                        break
                
                # si el límite es más de 50 rompe el bucle
                else:
                    break
            
            # cuando acaba construye una cadena con los elementos de la tupla y lo imprime
            for element in tupla:
                res += element
                res += " "

            print(res.strip())


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


