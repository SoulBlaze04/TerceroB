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
from pygomas.ontology import Belief
from agentspeak import Actions
from agentspeak import grounded
from agentspeak.stdlib import actions as asp_action

class NewGeneral(BDISoldier):
    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)

        @actions.add_function(".startingPositions", (tuple, tuple))
        def _startingPositions(posBase, posFlag) :
            xBase, yBase, zBase = posBase[0], posBase[1], posBase[2]
            xFlag, yFlag, zFlag = posFlag[0], posFlag[1], posFlag[2]

            pointList = []

            if(xFlag - xBase == 0):
                if(zBase < zFlag):
                    fieldop_pos = [xBase, 0, zBase + 20]
                    pointList.append(tuple(fieldop_pos))
                    
                    comandante = tuple([(fieldop_pos[0]), 0, (fieldop_pos[2] + 10)])
                    pointList.append(comandante)
                    soldado3 = tuple([(fieldop_pos[0]), 0, (fieldop_pos[2] + 20)])

                else:
                    fieldop_pos = [xBase, 0, zBase - 20]
                    pointList.append(tuple(fieldop_pos))
                    
                    comandante = tuple([(fieldop_pos[0]), 0, (fieldop_pos[2] + 10)])
                    pointList.append(comandante)
                    soldado3 = tuple([(fieldop_pos[0]), 0, (fieldop_pos[2] + 20)])

                medic1 = [fieldop_pos[0] + 10, 0, fieldop_pos[2]]
                pointList.append(tuple(medic1))
                medic2 = [fieldop_pos[0] - 10, 0, fieldop_pos[2]]
                pointList.append(tuple(medic2))
                soldado1 = [(fieldop_pos[0] + 20), 0, fieldop_pos[2]]
                pointList.append(tuple(soldado1))
                soldado2 = [(fieldop_pos[0] - 20), 0, fieldop_pos[2]]
                pointList.append(tuple(soldado2))

                pointList.append(tuple(soldado3))

                if(xBase <= xFlag):
                    soldado4 = [fieldop_pos[0] + 10, 0, fieldop_pos[2] + 10]
                    pointList.append(tuple(soldado4))
                    soldado5 = [fieldop_pos[0] - 10, 0, fieldop_pos[2] + 10]
                    pointList.append(tuple(soldado5))
                
                else:
                    soldado4 = [fieldop_pos[0] + 10, 0, fieldop_pos[2] - 10]
                    pointList.append(tuple(soldado4))
                    soldado5 = [fieldop_pos[0] - 10, 0, fieldop_pos[2] - 10]
                    pointList.append(tuple(soldado5))

            elif (zFlag - zBase == 0):
                if (xBase < xFlag):
                    fieldop_pos = [xBase + 20, 0, zBase]
                    pointList.append(tuple(fieldop_pos))
                    
                    comandante = tuple([(fieldop_pos[0] + 10), 0, fieldop_pos[2]])
                    pointList.append(comandante)
                    soldado3 = tuple([(fieldop_pos[0] + 20), 0, fieldop_pos[2]])

                else:
                    fieldop_pos = [xBase - 20, 0, zBase]
                    pointList.append(tuple(fieldop_pos))
                    
                    comandante = tuple([(fieldop_pos[0] + 10), 0, fieldop_pos[2]])
                    pointList.append(comandante)
                    soldado3 = tuple([(fieldop_pos[0] + 20), 0, fieldop_pos[2]])
                    
                    comandante = tuple([(fieldop_pos[0] - 10), 0, fieldop_pos[2]])
                    pointList.append(comandante)
                    soldado3 = tuple([(fieldop_pos[0] - 20), 0, fieldop_pos[2]])

                medic1 = [fieldop_pos[0], 0, fieldop_pos[2] + 10]
                pointList.append(tuple(medic1))
                medic2 = [fieldop_pos[0], 0, fieldop_pos[2] - 10]
                pointList.append(tuple(medic2))
                soldado1 = [fieldop_pos[0], 0, (fieldop_pos[2] + 20)]
                pointList.append(tuple(soldado1))
                soldado2 = [fieldop_pos[0], 0, (fieldop_pos[2] - 20)]
                pointList.append(tuple(soldado2))

                pointList.append(tuple(soldado3))
                
                if (zBase <= zFlag):
                    soldado4 = [fieldop_pos[0] + 10, 0, fieldop_pos[2] + 10]
                    pointList.append(tuple(soldado4))
                    soldado5 = [fieldop_pos[0] + 10, 0, fieldop_pos[2] - 10]
                    pointList.append(tuple(soldado5))
                
                else:
                    soldado4 = [fieldop_pos[0] - 10, 0, fieldop_pos[2] + 10]
                    pointList.append(tuple(soldado4))
                    soldado5 = [fieldop_pos[0] - 10, 0, fieldop_pos[2] - 10]
                    pointList.append(tuple(soldado5))

            else:
                m = math.ceil((zFlag - zBase) / (xFlag - xBase))
                mT = (-1) / m if m != 0 else -1
                
                if(xBase < xFlag):
                    if(zBase < zFlag):
                        fieldop_pos = [xBase + 20, 0, zBase + 20]
                        pointList.append(tuple(fieldop_pos))
                    else:
                        fieldop_pos = [xBase + 20, 0, zBase - 20]
                        pointList.append(tuple(fieldop_pos))
                    
                    comandante = tuple([(fieldop_pos[0] + 10), 0, (fieldop_pos[2] + (10*m))])
                    pointList.append(comandante)
                    soldado3 = tuple([(fieldop_pos[0] + 20), 0, (fieldop_pos[2] + (20*m))])

                else:
                    if(zBase < zFlag):
                        fieldop_pos = [xBase - 20, 0, zBase + 20]
                        pointList.append(tuple(fieldop_pos))
                    else:
                        fieldop_pos = [xBase - 20, 0, zBase - 20]
                        pointList.append(tuple(fieldop_pos))
                    
                    comandante = [(fieldop_pos[0] - 10), 0, (fieldop_pos[2] - (10*m))]
                    pointList.append(tuple(comandante))
                    soldado3 = [(fieldop_pos[0] - 20), 0, (fieldop_pos[2] - (20*m))]

                medic1 = [fieldop_pos[0] + 10, 0, fieldop_pos[2] + 10*mT]
                pointList.append(tuple(medic1))
                medic2 = [fieldop_pos[0] - 10, 0, (fieldop_pos[2] - (10*mT))]
                pointList.append(tuple(medic2))
                soldado1 = [(fieldop_pos[0] + 20), 0, (fieldop_pos[2] + (20*mT))]
                pointList.append(tuple(soldado1))
                soldado2 = [(fieldop_pos[0] - 20), 0, (fieldop_pos[2] - (20*mT))]
                pointList.append(tuple(soldado2))

                pointList.append(tuple(soldado3))
                
                soldado4 = [((soldado1[0] + soldado3[0]) / 2), 0, ((soldado1[2] + soldado3[2]) / 2)]
                pointList.append(tuple(soldado4))
                soldado5 = [((soldado2[0] + soldado3[0]) / 2), 0, ((soldado2[2] + soldado3[2]) / 2)]
                pointList.append(tuple(soldado5))
    
            for i, tryPosition in enumerate(pointList):
                tryX = int(tryPosition[0])
                tryZ = int(tryPosition[2])
                newTuple = None

                while (self.map.can_walk(tryX, tryZ) == False) and (tryX > 10) and (tryZ > 10):
                    tryX = tryX - 1
                    tryZ = tryZ - 1
                    newTuple = tuple([tryX, 0, tryZ])

                while (self.map.can_walk(tryX, tryZ) == False) and (tryX < 245) and (tryZ < 245):
                    tryX = tryX + 1
                    tryZ = tryZ + 1
                    newTuple = tuple([tryX, 0, tryZ])
                
                while (self.map.can_walk(tryX, tryZ) == False):
                    tryX = random.randint(10,245)
                    tryZ = random.randint(10,245)
                    newTuple = tuple([tryX, 0, tryZ])
                
                if newTuple is not None:
                    pointList[i] = newTuple
            
                     
            res = tuple(pointList)

            return res

        @actions.add_function(".unifiedList", (tuple, tuple, tuple, tuple))
        def _unifiedList(comandanteList, medicList, fieldopsList, soldierList) :
            unified = []
            mySet = set()
            mySet.add("aaa")
            comandante = comandanteList[0] 


            for itemR in fieldopsList:
                if (itemR not in mySet) and (itemR != comandante):
                    unified.append(itemR)
                    mySet.add(itemR)

            for itemC in comandanteList:
                if itemC not in mySet:
                    unified.append(itemC)
                    mySet.add(itemC)

            for itemM in medicList:
                if itemM not in mySet:
                    unified.append(itemM)
                    mySet.add(itemM)

            for itemS in soldierList:
                if itemS not in mySet:
                    unified.append(itemS)
                    mySet.add(itemS)
            
            return tuple(unified)