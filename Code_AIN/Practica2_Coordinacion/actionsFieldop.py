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
from pygomas.agents.bdifieldop import BDIFieldOp
from pygomas.agents.bdisoldier import BDISoldier
from pygomas.ontology import Belief
from agentspeak import Actions
from agentspeak import grounded
from agentspeak.stdlib import actions as asp_action

class NewFieldop(BDIFieldOp):
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

        @actions.add_function(".mustHelp", (tuple, tuple))
        def _mustHelp(possibleBackups, posSoldier):
            xSoldier, ySoldier, zSoldier = posSoldier[0], posSoldier[1], posSoldier[2]

            min1 = 999
            ag1 = None
            min2 = 999
            ag2 = None
            subs1 = True

            for backup in possibleBackups:
                xBackup, yBackup, zBackup = backup[0], backup[1], backup[2]
                distance = math.sqrt(((xSoldier - xBackup) * (xSoldier - xBackup)) + ((zSoldier - zBackup) * (zSoldier - zBackup)))

                if subs1:
                    if min1 < distance:
                        min1 = distance
                        ag1 = backup
                else:
                    if min2 < distance:
                        min2 = distance
                        ag2 = backup

                if min1 > min2:
                    subs1 = True
                else:
                    subs1 = False
            
            return (ag1, ag2)