#Alumnos: Alberto Olcina Calabuig y Alma Salmerón Sena
import json
import math
import random
from loguru import logger
from spade.behaviour import OneShotBehaviour
from spade.template import Template
from spade.message import Message
from pygomas.agents.bditroop import BDITroop
from pygomas.agents.bdimedic import BDIMedic
from pygomas.agents.bdisoldier import BDISoldier
from pygomas.agents.bdifieldop import BDIFieldOp
from pygomas.ontology import Belief
from agentspeak import Actions
from agentspeak import grounded
from agentspeak.stdlib import actions as asp_action

class NewSoldier(BDISoldier):
    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)

        @actions.add_function(".getFinalPosition", (tuple, tuple, tuple))
        def _getFinalPosition(posSoldier, posBase, posFlag):
            xSoldier, ySoldier, zSoldier = posSoldier[0], posSoldier[1], posSoldier[2]
            xBase, yBase, zBase = posBase[0], posBase[1], posBase[2]
            xFlag, yFlag, zFlag = posFlag[0], posFlag[1], posFlag[2]

            if(xFlag - xBase == 0):
                if(zBase < zFlag):
                    ejeY = zSoldier + zFlag - zBase - 25
                else:
                    ejeY = zSoldier - zFlag + zBase + 25
                endPos = [xSoldier, ySoldier, (zSoldier + ejeY)]

            elif(zFlag - zBase == 0):
                if(xBase < xFlag):
                    ejeX = xSoldier + xFlag - xBase - 25
                else:
                    ejeX = xSoldier - xFlag + xBase + 25
                endPos = [(xSoldier + ejeX), ySoldier, zSoldier]

            else:

                ejeX = xFlag - xBase
                
                if(xBase < xFlag):
                    ejeX = ejeX - 25
                else:
                    ejeX = ejeX + 25

                m = (zFlag - zBase) / (xFlag - xBase)
                ejeY = math.floor(m*ejeX)

                endPos = [(xSoldier + ejeX), ySoldier, (zSoldier + ejeY)]

            tryX = int(endPos[0])
            tryZ = int(endPos[2])
            
            newTuple = None

            if (not(self.map.can_walk(tryX, tryZ))) or tryX >= 245 or tryX <= 10 or tryZ >= 245 or tryZ <= 10 :
                return tuple([xFlag, 0, zFlag])
                
        

            retPos = tuple(endPos)
            return retPos

    
        @actions.add_function(".mas_cercano", (tuple))
        def _mas_cercano(tupla) :
            ofertas = tupla[0]
            agentes = tupla[1]
            if (len(ofertas) == 0 or len(agentes) == 0) :
                return tuple()
            set_agentes = set(agentes)
            set_auxiliar = set()
            posicion = tupla[2]
            x, z = posicion[0], posicion[2]
            distancia_minima = 100000000
            mejor_oferta = ofertas[0]
            mejor_agente = agentes[0]
            indice_agente = 0
            
            for indice, oferta in enumerate(ofertas) :
                if len(set_auxiliar) != len(set_agentes) :
                    set_auxiliar.add(agentes[indice])
                    x_medico = oferta[0]
                    z_medico = oferta[2]
                    distancia = abs(int(x) - int(x_medico)) + abs(int(z) - int(z_medico))
                    if (distancia < distancia_minima) :
                        distancia_minima = distancia
                        mejor_oferta = oferta
                        mejor_agente = agentes[indice]
                        indice_agente = indice
                else : break
            
            posicion_intermedia =  tuple([math.ceil((int(x) + int(mejor_oferta[0])) / 2), 0, math.ceil((int(z) + int(mejor_oferta[2])) / 2)])

            if not (self.map.can_walk(posicion_intermedia[0], posicion_intermedia[2])) :
                posicion_intermedia = mejor_oferta

            return tuple([posicion_intermedia, mejor_agente, indice_agente])