#! -*- encoding: utf8 -*-

## Nombres: 

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import os
import re
from typing import Optional

def sort_dic_by_values(d:dict) -> list:
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')

    def write_stats(self, filename:str, stats:dict, use_stopwords:bool, bigrams: bool, full:bool):
        """
        Este método escribe en fichero las estadísticas de un texto
            
        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas
        """

        with open(filename, 'w', encoding='utf-8', newline='\n') as ofile:
            ## completar
            
            ofile.write("Lines: " + str(stats['nlines']) + '\n')
            ofile.write("Number words (including stopwords): " + str(stats['nwords']) + '\n')
            
            if(use_stopwords):
                ofile.write("Number words (without stopwords): " + str((stats['nwords'] - stats['nwordsstop'])) + '\n')
            
            ofile.write("Vocabulary size: " + str(len(stats['word'])) + '\n')
            ofile.write("Number of symbols: " + str(stats['nsymbol']) + '\n')
            ofile.write("Number of different symbols: " + str(len(stats['symbol'])) + '\n')

            # Print words
            ofile.write("Words (alphabetical order):" + '\n')

            if(full):
                for word in stats['word']:
                    ofile.write('\t' + word + ": " + str(stats['word'].get(word, 0)) + '\n')

            else:
                i = 0

                for word in stats['word']:
                    if(i == 20):
                        break
                
                    ofile.write('\t' + word + ": " + str(stats['word'].get(word, 0)) + '\n')
                    i += 1
            
            ofile.write("Words (by frequency):" + '\n')
            stats['word'] = dict(sort_dic_by_values(stats['word']))

            if(full):
                for word in stats['word']:
                    ofile.write('\t' + word + ": " + str(stats['word'].get(word, 0)) + '\n')

            else:
                i = 0

                for word in stats['word']:
                    if(i == 20):
                        break
                
                    ofile.write('\t' + word + ": " + str(stats['word'].get(word, 0)) + '\n')
                    i += 1
        
            # Print symbols
            ofile.write("Symbols (alphabetical order):" + '\n')

            if(full):
                for token in stats['symbol']:
                    ofile.write('\t' + token + ": " + str(stats['symbol'].get(token, 0)) + '\n')

            else:
                i = 0

                for token in stats['symbol']:
                    if(i == 20):
                        break
                
                    ofile.write('\t' + token + ": " + str(stats['symbol'].get(token, 0)) + '\n')
                    i += 1
            
            ofile.write("Symbols (by frequency):" + '\n')
            stats['symbol'] = dict(sort_dic_by_values(stats['symbol']))

            if(full):
                for token in stats['symbol']:
                    ofile.write('\t' + token + ": " + str(stats['symbol'].get(token, 0)) + '\n')

            else:
                i = 0

                for token in stats['symbol']:
                    if(i == 20):
                        break

                    ofile.write('\t' + token + ": " + str(stats['symbol'].get(token, 0)) + '\n')
                    i += 1
            
            # Print bigrams
            if(bigrams):

                # Print biwords
                ofile.write("Word pairs (alphabetical order):" + '\n')

                if(full):
                    for pair in stats['biword']:
                        aux = str(pair[0] + " " + pair[1])
                        ofile.write('\t' + aux + ": " + str(stats['biword'].get(pair, 0)) + '\n')

                else:
                    i = 0

                    for pair in stats['biword']:
                        if(i == 20):
                            break

                        aux = str(pair[0] + " " + pair[1])  
                        ofile.write('\t' + aux + ": " + str(stats['biword'].get(pair, 0)) + '\n')
                        i += 1

                ofile.write("Word pairs (by frequency):" + '\n')
                stats['biword'] = dict(sort_dic_by_values(stats['biword']))

                if(full):
                    for pair in stats['biword']:
                        aux = str(pair[0] + " " + pair[1])
                        ofile.write('\t' + aux + ": " + str(stats['biword'].get(pair, 0)) + '\n')

                else:
                    i = 0

                    for pair in stats['biword']:
                        if(i == 20):
                            break
                        
                        aux = str(pair[0] + " " + pair[1])
                        ofile.write('\t' + aux + ": " + str(stats['biword'].get(pair, 0)) + '\n')
                        i += 1

                #Print bisymbols
                ofile.write("Symbol pairs (alphabetical order):" + '\n')

                if(full):
                    for pair in stats['bisymbol']:
                        ofile.write('\t' + pair + ": " + str(stats['bisymbol'].get(pair, 0)) + '\n')

                else:
                    i = 0

                    for pair in stats['bisymbol']:
                        if(i == 20):
                            break
                            
                        ofile.write('\t' + pair + ": " + str(stats['bisymbol'].get(pair, 0)) + '\n')
                        i += 1

                ofile.write("Symbol pairs (by frequency):" + '\n')
                stats['bisymbol'] = dict(sort_dic_by_values(stats['bisymbol']))

                if(full):
                    for pair in stats['bisymbol']:
                        ofile.write('\t' + pair + ": " + str(stats['bisymbol'].get(pair, 0)) + '\n')

                else:
                    i = 0

                    for pair in stats['bisymbol']:
                        if(i == 20):
                            break
                            
                        ofile.write('\t' + pair + ": " + str(stats['bisymbol'].get(pair, 0)) + '\n')
                        i += 1


            # Print prefixes
            ofile.write("Prefixes (by frequency):" + '\n')
            stats['prefix'] = dict(sort_dic_by_values(stats['prefix']))

            if(full):
                for pref in stats['prefix']:
                    ofile.write('\t' + pref + ": " + str(stats['prefix'].get(pref, 0)) + '\n')

            else:
                i = 0

                for pref in stats['prefix']:
                    if(i == 20):
                        break

                    ofile.write('\t' + pref + ": " + str(stats['prefix'].get(pref, 0)) + '\n')
                    i += 1

            # Print suffixes
            ofile.write("Suffixes (by frequency):" + '\n')
            stats['suffix'] = dict(sort_dic_by_values(stats['suffix']))

            if(full):
                for pref in stats['suffix']:
                    ofile.write('\t' + pref + ": " + str(stats['suffix'].get(pref, 0)) + '\n')

            else:
                i = 0

                for pref in stats['suffix']:
                    if(i == 20):
                        break

                    ofile.write('\t' + pref + ": " + str(stats['suffix'].get(pref, 0)) + '\n')
                    i += 1        


    def file_stats(self, fullfilename:str, lower:bool, stopwordsfile:Optional[str], bigrams:bool, full:bool):
        """
        Este método calcula las estadísticas de un fichero de texto

        :param 
            fullfilename: el nombre del fichero, puede incluir ruta.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?
        """

        stopwords = set() if stopwordsfile is None else set(open(stopwordsfile, encoding='utf-8').read().split())

        # variables for results

        sts = {
                'nlines': 0,
                'nwords': 0,
                'nwordsstop': 0,
                'nsymbol': 0,
                'word': {},
                'symbol': {},
                'prefix': {},
                'suffix': {}
                }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        # COMPLETAR
        # AYUDA: line = self.clean_re.sub(' ', line)
    
        with open(fullfilename, 'r', encoding='utf-8') as ifile:

            for line in ifile:
                sts['nlines'] += 1
                line = self.clean_re.sub(' ', line)
            
                if lower:
                    line = line.lower()
                
                if bigrams:
                    words = line.split(" ")
                    words = words[0:len(words) - 1]
                    words.append("$")

                    current = "$"

                    for token in words:
                        next = token

                        if(stopwordsfile):
                            if (next not in stopwords):
                                pair = (current, next)
                                sts['biword'][pair] = sts['biword'].get(pair, 0) + 1
                            else:
                                sts['nwordsstop'] += 1
                        else:
                            pair = (current, next)
                            sts['biword'][pair] = sts['biword'].get(pair, 0) + 1
                        
                        if(next != "$"):
                            if(next != ''):
                                sts['nwords'] += 1

                                if(stopwordsfile):
                                    if (next not in stopwords):
                                        sts['word'][next] = sts['word'].get(next, 0) + 1    
                                        self.word_analysis(next, sts, bigrams)
                                else:
                                    sts['word'][token] = sts['word'].get(token, 0) + 1
                                    self.word_analysis(next, sts, bigrams)
                        
                        current = next
                
                else:
                    words = line.split(" ")
                    words = words[0:len(words) - 1]
                    
                    for token in words:
                        if(token != ''):
                            sts['nwords'] += 1

                            if(stopwordsfile):
                                if (token not in stopwords):
                                    sts['word'][token] = sts['word'].get(token, 0) + 1
                                    self.word_analysis(token, sts, bigrams)
                                else:
                                    sts['nwordsstop'] += 1
                            else:
                                sts['word'][token] = sts['word'].get(token, 0) + 1
                                self.word_analysis(token, sts, bigrams)

                

        filename, ext0 = os.path.splitext(fullfilename)

        extraString = ""
        if(lower): extraString += "l"
        if(stopwordsfile): extraString += "s"
        if(bigrams): extraString += "b"
        if(full): extraString += "f"


        new_filename = filename + "_" + extraString + "_stats" + ext0
        sts['word'] = dict(sorted(sts['word'].items()))
        sts['symbol'] = dict(sorted(sts['symbol'].items()))
        sts['prefix'] = dict(sorted(sts['prefix'].items()))
        sts['suffix'] = dict(sorted(sts['suffix'].items()))
        
        if(bigrams):
            sts['biword'] = dict(sorted(sts['biword'].items()))
            sts['bisymbol'] = dict(sorted(sts['bisymbol'].items()))

        self.write_stats(new_filename, sts, stopwordsfile is not None, bigrams, full)

    def word_analysis(self, word, stats, bigrams:bool):
        
        if(len(word) > 2):
            pref2 = word[0 : 2] + "-"
            suf2 = "-" + word[len(word) - 2 : len(word)]

            stats['prefix'][pref2] = stats['prefix'].get(pref2, 0) + 1
            stats['suffix'][suf2] = stats['suffix'].get(suf2, 0) + 1
        
        if(len(word) > 3):
            pref3 = word[0 : 3] + "-"
            suf3 = "-" + word[len(word) - 3 : len(word)]

            stats['prefix'][pref3] = stats['prefix'].get(pref3, 0) + 1
            stats['suffix'][suf3] = stats['suffix'].get(suf3, 0) + 1
        
        if(len(word) > 4):
            pref4 = word[0 : 4] + "-"
            suf4 = "-" + word[len(word) - 4 : len(word)]

            stats['prefix'][pref4] = stats['prefix'].get(pref4, 0) + 1
            stats['suffix'][suf4] = stats['suffix'].get(suf4, 0) + 1
        
        stats['nsymbol'] += len(word)

        current = word[0]
        stats['symbol'][current] = stats['symbol'].get(current, 0) + 1
        new_word = word[1 : len(word)]

        for symbol in new_word:
            next = symbol

            if(bigrams):
                key = current + next
                stats['bisymbol'][key] = stats['bisymbol'].get(key, 0) + 1
            
            stats['symbol'][next] = stats['symbol'].get(next, 0) + 1
            current = next

    def compute_files(self, filenames:str, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower',
                        action='store_true', default=False, 
                        help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                        help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram',
                        action='store_true', default=False, 
                        help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full',
                        action='store_true', default=False, 
                        help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file,
                     lower=args.lower,
                     stopwordsfile=args.stopwords,
                     bigrams=args.bigram,
                     full=args.full)