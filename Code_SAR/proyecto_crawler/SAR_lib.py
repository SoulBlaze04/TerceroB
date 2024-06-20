import json
from nltk.stem.snowball import SnowballStemmer
import os
import re
import sys
from pathlib import Path
from typing import Optional, List, Dict
import pickle

class SAR_Indexer:
    """
    Prototipo de la clase para realizar la indexacion y la recuperacion de artículos de Wikipedia
        
        Preparada para todas las ampliaciones:
          parentesis + multiples indices + posicionales + stemming + permuterm

    Se deben completar los metodos que se indica.
    Se pueden añadir nuevas variables y nuevos metodos
    Los metodos que se añadan se deberan documentar en el codigo y explicar en la memoria
    """

    # lista de campos, el booleano indica si se debe tokenizar el campo
    # NECESARIO PARA LA AMPLIACION MULTIFIELD
    fields = [
        ("all", True), ("title", True), ("summary", True), ("section-name", True), ('url', False),
    ]
    def_field = 'all'
    PAR_MARK = '%'
    # numero maximo de documento a mostrar cuando self.show_all es False
    SHOW_MAX = 10

    all_atribs = ['urls', 'index', 'sindex', 'ptindex', 'docs', 'weight', 'articles',
                  'tokenizer', 'stemmer', 'show_all', 'use_stemming']

    def __init__(self):
        """
        Constructor de la clase SAR_Indexer.
        NECESARIO PARA LA VERSION MINIMA

        Incluye todas las variables necesaria para todas las ampliaciones.
        Puedes añadir más variables si las necesitas 

        """
        self.urls = set() # hash para las urls procesadas,
        self.index = {"all": {}, "url": {}, "title": {}, "summary": {}, "section-name": {}} # hash para el indice invertido de terminos --> clave: termino, valor: posting list
        self.sindex = {"all": {}, "url": {}, "title": {}, "summary": {}, "section-name": {}} # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {} # hash para el indice permuterm.
        self.docs = {} # diccionario de documentos --> clave: entero(docid),  valor: ruta del fichero.
        self.weight = {} # hash de terminos para el pesado, ranking de resultados.
        self.articles = {} # hash de articulos --> clave entero (artid), valor: la info necesaria para diferencia los artículos dentro de su fichero
        self.tokenizer = re.compile(r"\W+") # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish') # stemmer en castellano
        self.show_all = False # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()
        self.query_parser = re.compile(r'\)|\(|[^ ()]+')


    ###############################
    ###                         ###
    ###      CONFIGURACION      ###
    ###                         ###
    ###############################


    def set_showall(self, v:bool):
        """

        Cambia el modo de mostrar los resultados.
        
        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_all es True se mostraran todos los resultados el lugar de un maximo de self.SHOW_MAX, no aplicable a la opcion -C

        """
        self.show_all = v


    def set_snippet(self, v:bool):
        """

        Cambia el modo de mostrar snippet.
        
        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_snippet es True se mostrara un snippet de cada noticia, no aplicable a la opcion -C

        """
        self.show_snippet = v


    def set_stemming(self, v:bool):
        """

        Cambia el modo de stemming por defecto.
        
        input: "v" booleano.

        UTIL PARA LA VERSION CON STEMMING

        si self.use_stemming es True las consultas se resolveran aplicando stemming por defecto.

        """
        self.use_stemming = v



    #############################################
    ###                                       ###
    ###      CARGA Y GUARDADO DEL INDICE      ###
    ###                                       ###
    #############################################


    def save_info(self, filename:str):
        """
        Guarda la información del índice en un fichero en formato binario
        
        """
        info = [self.all_atribs] + [getattr(self, atr) for atr in self.all_atribs]
        with open(filename, 'wb') as fh:
            pickle.dump(info, fh)

    def load_info(self, filename:str):
        """
        Carga la información del índice desde un fichero en formato binario
        
        """
        #info = [self.all_atribs] + [getattr(self, atr) for atr in self.all_atribs]
        with open(filename, 'rb') as fh:
            info = pickle.load(fh)
        atrs = info[0]
        for name, val in zip(atrs, info[1:]):
            setattr(self, name, val)


    ###############################
    ###                         ###
    ###   PARTE 1: INDEXACION   ###
    ###                         ###
    ###############################

    def already_in_index(self, article:Dict) -> bool:
        """

        Args:
            article (Dict): diccionario con la información de un artículo

        Returns:
            bool: True si el artículo ya está indexado, False en caso contrario
        """
        return article['url'] in self.urls


    def index_dir(self, root:str, **args):
        """
        
        Recorre recursivamente el directorio o fichero "root" 
        NECESARIO PARA TODAS LAS VERSIONES
        
        Recorre recursivamente el directorio "root"  y indexa su contenido
        los argumentos adicionales "**args" solo son necesarios para las funcionalidades ampliadas

        """
        self.multifield = args['multifield']
        self.positional = args['positional']
        self.use_stemming = args['stem']
        self.permuterm = args['permuterm']

        file_or_dir = Path(root)
        
        if file_or_dir.is_file():
            # is a file
            self.index_file(root)
        elif file_or_dir.is_dir():
            # is a directory
            for d, _, files in os.walk(root):
                for filename in files:
                    if filename.endswith('.json'):
                        fullname = os.path.join(d, filename)
                        self.index_file(fullname)
        else:
            print(f"ERROR:{root} is not a file nor directory!", file=sys.stderr)
            sys.exit(-1)
        ##########################################
        ## COMPLETAR PARA FUNCIONALIDADES EXTRA ##
        ##########################################
        
        
    def parse_article(self, raw_line:str) -> Dict[str, str]:
        """
        Crea un diccionario a partir de una linea que representa un artículo del crawler

        Args:
            raw_line: una linea del fichero generado por el crawler

        Returns:
            Dict[str, str]: claves: 'url', 'title', 'summary', 'all', 'section-name'
        """
        
        article = json.loads(raw_line)
        sec_names = []
        txt_secs = ''
        for sec in article['sections']:
            txt_secs += sec['name'] + '\n' + sec['text'] + '\n'
            txt_secs += '\n'.join(subsec['name'] + '\n' + subsec['text'] + '\n' for subsec in sec['subsections']) + '\n\n'
            sec_names.append(sec['name'])
            sec_names.extend(subsec['name'] for subsec in sec['subsections'])
        article.pop('sections') # no la necesitamos 
        article['all'] = article['title'] + '\n\n' + article['summary'] + '\n\n' + txt_secs
        article['section-name'] = '\n'.join(sec_names)

        return article

    
    def index_file(self, filename:str):
        """

        Indexa el contenido de un fichero.
        
        input: 

        NECESARIO PARA TODAS LAS VERSIONES

        dependiendo del valor de self.multifield y self.positional se debe ampliar el indexado


        """
        """ Indexa el contenido de un fichero.

        Args:
            self: Una referencia a sí mismo
            filename: es el nombre de un fichero generado por el Crawler cada línea es un objeto json
            con la información de un artículo de la Wikipedia

        Returns:
            None, tan solo puebla el self.index, y si stemming == True, llama a self.make_stemming
        """
        # añade un documento con el docid generado en orden
        docid = len(self.docs)
        self.docs[docid] = filename
        for line_number, line in enumerate(open(filename)):
            article_dict = self.parse_article(line)
            if not self.already_in_index(article_dict):
                self.urls.add(article_dict["url"])
                # añade un artículo con el artid generado en orden
                # e introduce como valor en self.articles el doic
                # y la linea dentro del docid de donde viene el artículo
                artid = len(self.articles)
                self.articles[artid] = (docid, line_number)
                if not self.multifield:
                    for w in self.tokenize(article_dict["all"]):
                        if w in self.index["all"]:
                            # no añadir un artid dos veces a una posting list
                            if self.index["all"][w][-1] != artid:
                                self.index["all"][w].append(artid)
                        else:
                            self.index["all"][w] = [artid]
                else:
                    for field, should_be_tokenized in self.fields:
                        if should_be_tokenized:
                            for w in self.tokenize(article_dict[field]):
                                if w in self.index[field]:
                                    # no añadir un artid dos veces a una posting list
                                    if self.index[field][w][-1] != artid:
                                        self.index[field][w].append(artid)
                                else:
                                    self.index[field][w] = [artid]
                        else:
                            self.index[field][article_dict[field]] = [artid]
        if self.use_stemming:
            self.make_stemming()
        #
        # 
        # En la version basica solo se debe indexar el contenido "article"
        #
        #
        #
        #################
        ### COMPLETAR ###
        #################


    def tokenize(self, text:str):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Tokeniza la cadena "texto" eliminando simbolos no alfanumericos y dividiendola por espacios.
        Puedes utilizar la expresion regular 'self.tokenizer'.

        params: 'text': texto a tokenizar

        return: lista de tokens

        """
        return self.tokenizer.sub(' ', text.lower()).split()


    def make_stemming(self):
        """ Crea el indice de stemming (self.sindex) para los terminos de todos los indices.

        Args:
            self: Una referencia a sí mismo

        Returns:
            None, tan solo inicializa el diccionario de stems self.sindex
        """
        if not self.multifield:
            for term in self.index["all"].keys():
                stem = self.stemmer.stem(term)
                if stem in self.sindex["all"]:
                    self.sindex["all"][stem].append(term)
                else:
                    self.sindex["all"][stem] = [term]
        else:
            for field, should_be_tokenized in self.fields:
                for term in self.index[field].keys():
                    stem = self.stemmer.stem(term)
                    if stem in self.sindex[field]:
                        self.sindex[field][stem].append(term)
                    else:
                        self.sindex[field][stem] = [term]
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################

    
    def make_permuterm(self):
        """

        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.

        NECESARIO PARA LA AMPLIACION DE PERMUTERM


        """
        pass
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################


    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        
        Muestra estadisticas de los indices
        
        """
        
        print(f"========================================")
        print(f"Number of indexed files: {len(self.docs)}")
        print(f"----------------------------------------")
        print(f"Number of indexed articles: {len(self.articles)}")
        print(f"----------------------------------------")
        print(f"TOKENS:")

        if self.multifield:
            for field, _ in self.fields:
                print(f"\t# of tokens in '{field}': {len(self.index[field])}")
        else:
            print(f"\t# of tokens in 'all': {len(self.index['all'])}")

        if self.use_stemming:
            print(f"----------------------------------------")
            print(f"STEMS:")
            if self.multifield:
                for field, _ in self.fields:
                    print(f"\t# of tokens in '{field}': {len(self.sindex[field])}")
            else:
                print(f"\t# of tokens in 'all': {len(self.sindex['all'])}")
        print(f"----------------------------------------")
        print(f"Positional queries are NOT allowed.")
        print(f"=======================================")


    #################################
    ###                           ###
    ###   PARTE 2: RECUPERACION   ###
    ###                           ###
    #################################

    ###################################
    ###                             ###
    ###   PARTE 2.1: RECUPERACION   ###
    ###                             ###
    ###################################


    def solve_query(self, query:str, prev:Dict={}) -> List[int]:
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una query.
        Debe realizar el parsing de consulta que sera mas o menos complicado en funcion de la ampliacion que se implementen

        param:  "query": cadena con la query
                "prev": incluido por si se quiere hacer una version recursiva. No es necesario utilizarlo.


        return: posting list con el resultado de la query

        """

        if query is None or len(query) == 0:
            return []

        if '*' in query or '?' in query:
            raise NotImplementedError('La extensión de permuterm no está implementada')
        if '"' in query:
            raise NotImplementedError('La extensión de búsquedas posicionales no está implementada')
        
        query_parsed = self.query_parser.findall(query)

        #Transformación de cada item en su respectiva posting list
        for i, item in enumerate(query_parsed):
            if item not in ['(', ')', 'AND', 'OR', 'NOT']:
                word = item.lower().split(':', maxsplit=1)
                if len(word) == 1:
                    query_parsed[i] = self.get_posting(word[0])
                else:
                    query_parsed[i] = self.get_posting(word[1], word[0])

        #Implementación del algoritmo del stack para operaciones con prioridad (variación del algoritmo "shunting yard"), el resultado de la query se almacena en
        #la última y única instacia almacenada en el stack
        stack = []
        for token in query_parsed:
            if token in ['(', 'AND', 'OR', 'NOT']:
                stack.append(token)
            else: 
                if token == ')':
                    #He llegado a un cierre de paréntesis
                    value = stack.pop()
                    #Elimino el paréntesis inicial
                    stack.pop()
                    # Resultado parcial al que se aplicarán los operadores
                    partial_result = value
                else:
                    #He llegado a un término (respresentado por su posting list)
                    partial_result = token
                while len(stack) > 0 and stack[-1] != '(':
                    operator = stack.pop()
                    if operator == 'NOT':
                        partial_result = self.reverse_posting(partial_result)
                    else: 
                        left_operand = stack.pop()
                        if operator == 'AND':
                            partial_result = self.and_posting(left_operand, partial_result)
                        else: # operator == 'OR'
                            partial_result = self.or_posting(left_operand, partial_result)
                stack.append(partial_result)
        return stack[-1]
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################


    def get_posting(self, term:str, field:Optional[str]=None):
        """

        Devuelve la posting list asociada a un termino. 
        Dependiendo de las ampliaciones implementadas "get_posting" puede llamar a:
            - self.get_positionals: para la ampliacion de posicionales
            - self.get_permuterm: para la ampliacion de permuterms
            - self.get_stemming: para la amplaicion de stemming


        param:  "term": termino del que se debe recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario si se hace la ampliacion de multiples indices

        return: posting list
        
        NECESARIO PARA TODAS LAS VERSIONES

        """
        if self.use_stemming:
            if field == None:
                aux_field = 'all'
            else : 
                aux_field = field
            # queremos un OR de todas las posting lists de cada término que comparta stem con term
            result = []
            for other_term in self.get_stemming(term, aux_field):
                result = self.or_posting(result, self.index[aux_field].get(other_term, []))
            return result
        else:
            if field == None:
                return self.index['all'].get(term, [])
            else:
                return self.index[field].get(term, [])        
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################


    def get_positionals(self, terms:str, index):
        """

        Devuelve la posting list asociada a una secuencia de terminos consecutivos.
        NECESARIO PARA LA AMPLIACION DE POSICIONALES

        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        raise NotImplementedError('Amplicación de posicionales no implementada')
        ########################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE POSICIONALES ##
        ########################################################


    def get_stemming(self, term:str, field: Optional[str]=None):
        """

        Devuelve la posting list asociada al stem de un termino.
        NECESARIO PARA LA AMPLIACION DE STEMMING

        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        
        if field != 'url':
            stem = self.stemmer.stem(term)
        else:
            stem = term
        if field != None:
            res = self.sindex[field].get(stem, [])
        else:
            res = self.sindex['all'].get(stem, [])
        return res
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################


    def get_permuterm(self, term:str, field:Optional[str]=None):
        """

        Devuelve la posting list asociada a un termino utilizando el indice permuterm.
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        param:  "term": termino para recuperar la posting list, "term" incluye un comodin (* o ?).
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        ##################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA PERMUTERM ##
        ##################################################
        raise NotImplementedError('Ampliación de permuterm no implementada')


    def reverse_posting(self, p:list):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.


        param:  "p": posting list


        return: posting list con todos los artid exceptos los contenidos en p

        """
        
        return self.minus_posting(list(sorted(self.articles)), p)
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################


    def and_posting(self, p1:list, p2:list):
        """ Calcula el AND de dos posting list de forma EFICIENTE

        Args:
             "p1", "p2" (lists): posting lists sobre las que calcular

        Returns:
            Una lista, el resultado de hacer la intersección de ambas posting lists
        """
        result = []
        i, j = 0, 0
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                result.append(p1[i])
                i += 1; j += 1
            elif p1[i] < p2[j]:
                i += 1
            else:
                j += 1
        
        return result
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################


    def or_posting(self, p1:list, p2:list):
        """ Calcula el OR de dos posting list de forma EFICIENTE

        Args:
             "p1", "p2" (lists): posting lists sobre las que calcular

        Returns:
            Una lista, el resultado de hacer la unión de ambas posting lists
        """
        result = []
        i, j = 0, 0
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                result.append(p1[i])
                i += 1; j += 1
            elif p1[i] < p2[j]:
                result.append(p1[i])
                i += 1
            else:
                result.append(p2[j])
                j += 1
        
        while i < len(p1):
            result.append(p1[i])
            i += 1
        while j < len(p2):
            result.append(p2[j])
            j += 1

        return result
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################


    def minus_posting(self, p1, p2):
        """

        OPCIONAL PARA TODAS LAS VERSIONES

        Calcula el except de dos posting list de forma EFICIENTE.
        Esta funcion se incluye por si es util, no es necesario utilizarla.

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los artid incluidos de p1 y no en p2

        """

        result = []
        i, j = 0, 0
        while i < len(p1) and j < len(p2):
            if p1[i] < p2[j]:
                result.append(p1[i])
                i += 1
            elif p2[j] < p1[i]:
                j += 1
            else:
                i += 1
                j += 1
        while i < len(p1):
            result.append(p1[i])
            i += 1
        return result
        ########################################################
        ## COMPLETAR PARA TODAS LAS VERSIONES SI ES NECESARIO ##
        ########################################################


    #####################################
    ###                               ###
    ### PARTE 2.2: MOSTRAR RESULTADOS ###
    ###                               ###
    #####################################

    def solve_and_count(self, ql:List[str], verbose:bool=True) -> List:
        results = []
        for query in ql:
            if len(query) > 0 and query[0] != '#':
                r = self.solve_query(query)
                results.append(len(r))
                if verbose:
                    print(f'{query}\t{len(r)}')
            else:
                results.append(0)
                if verbose:
                    print(query)
        return results


    def solve_and_test(self, ql:List[str]) -> bool:
        errors = False
        for line in ql:
            if len(line) > 0 and line[0] != '#':
                query, ref = line.split('\t')
                reference = int(ref)
                result = len(self.solve_query(query))
                if reference == result:
                    print(f'{query}\t{result}')
                else:
                    print(f'>>>>{query}\t{reference} != {result}<<<<')
                    errors = True                    
            else:
                print(line)
        return not errors


    def solve_and_show(self, query:str):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra junto al numero de resultados 

        param:  "query": query que se debe resolver.

        return: el numero de artículo recuperadas, para la opcion -T

        """

        solved_query = self.solve_query(query)

        print('========================================')
        for i, artid in enumerate(solved_query):
            # solo se deben mostrar los 10 primeros artículos si no se especifica -A
            if not self.show_all and i >= 10:
                break
            docid, line_number = self.articles[artid]
            with open(self.docs[docid], 'r') as file:
                article = self.parse_article(list(file.readlines())[line_number])
                if not self.show_snippet:
                    # ponemos el título antes ya que así aparece en la referencia del pdf
                    print(f'# {i+1:02} ({line_number:3}) {article["title"]}:\t{article["url"]}')
                else:
                    print(f'# {i+1:02} ({line_number:3}) {article["url"]}\n\t{article["title"]}')
                    query_parsed = self.query_parser.findall(query)
                    # representamos la query de forma canónica como suma de minterms (OR de ANDs)
                    # implementada como una lista de listas en la que cada sublista representa un minterm,
                    # es decir, un AND de términos, y la lista en si es un OR de minterms
                    # Por ejemplo, la query t1 AND t2 OR t3 se transforma en la minterm_list [[t1, t2], [t3]], 
                    # la query t1 OR t2 AND t3 se transforma en la minterm_list [[t1, t3], [t2, t3]] 
                    # ya que la consulta es ((t1 AND t3) OR (t2 AND t3)) en forma canónica de suma de minterms
                    minterm_list = []
                    found_and = False
                    found_or = False
                    # este bucle se encarga de formar la minterm_list
                    for item in query_parsed:
                        if item == 'AND':
                            found_and = True
                            found_or = False
                        elif item == 'OR':
                            found_or = True
                            found_and = False
                        else:
                            token = item.lower()
                            if found_or:
                                minterm_list.append([token])
                            elif found_and:
                                for minterm in minterm_list:
                                    minterm.append(token)
                            else:
                                minterm_list.append([token])
                            found_and = False
                            found_or = False
                    all_words = self.tokenize(article['all'])
                    # ahora iteramos sobre todas las palabras hasta encontrar un snippet en el
                    # que se cumpla una de las condiciones AND definidas en la condition_list
                    found_snippet = False
                    for w, word in enumerate(all_words):
                        for minterm in minterm_list:
                            if word == minterm[0]:
                                found_snippet = True
                                snippet_words = all_words[w-20 : w+21]
                                for i in range(1, len(minterm)):
                                    if minterm[i] not in snippet_words:
                                        found_snippet = False
                                        break
                                if found_snippet:
                                    print(' '.join(snippet_words))
                                    break
                        if found_snippet:
                            break
                    if not found_snippet:
                        print('No se ha podido encontrar un snippet')
        print('========================================')
        print(f'Number of results: {len(solved_query)}')
        ################
        ## COMPLETAR  ##
        ################
