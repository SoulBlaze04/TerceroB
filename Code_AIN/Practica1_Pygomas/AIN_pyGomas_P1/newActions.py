#Alumnos: Alberto Olcina Calabuig y Alma Salmerón Sena
import json
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

class NewSoldier(BDISoldier):
    def add_custom_actions(self, actions):
        super().add_custom_actions(actions)

        @actions.add_function(".getNearestCentralLimit", (tuple))
        def _getNearestCentralLimit(pos) :
            x, y, z = pos[0], pos[1], pos[2]
            first = [121,0,10]
            second = [121,0,244]
            third = [10,0,121]
            fourth = [244,0,121]
            listP = [first, second, third, fourth]
            minDist = 999999
            goTo = None
            for point in listP :
                distance = abs(point[0] - int(x)) + abs(point[2] - int(z))
                if (distance < minDist) :
                    minDist = distance
                    goTo = point
            goTo = tuple(goTo)
            return goTo

        @actions.add_function(".getInitialLookAt", (tuple))
        def _getInitialLookAt(pos) :
            x, y, z = pos[0], pos[1], pos[2]
            lookAt = []
            if ((x == 121) and (z == 10)):
                lookAt = [121,0,25]
            elif ((x == 121) and (z == 244)):
                lookAt = [121,0,230]
            elif ((x == 10) and (z == 121)):
                lookAt = [25,0,121]
            elif ((x == 244) and (z == 121)):
                lookAt = [230,0,121]
            
            lookAt = tuple(lookAt)
            return lookAt
        
        @actions.add_function(".lookSideOne", (tuple))
        def _lookSideOne(pos) :
            x, y, z = pos[0], pos[1], pos[2]
            lookAt = []
            if ((x == 121) and (z == 10)):
                lookAt = [90,0,25]
            elif ((x == 121) and (z == 244)):
                lookAt = [90,0,230]
            elif ((x == 10) and (z == 121)):
                lookAt = [25,0,90]
            elif ((x == 244) and (z == 121)):
                lookAt = [230,0,90]
            
            lookAt = tuple(lookAt)
            return lookAt
        
        @actions.add_function(".lookSideTwo", (tuple))
        def _lookSideTwo(pos) :
            x, y, z = pos[0], pos[1], pos[2]
            lookAt = []
            if ((x == 121) and (z == 10)):
                lookAt = [150,0,25]
            elif ((x == 121) and (z == 244)):
                lookAt = [150,0,230]
            elif ((x == 10) and (z == 121)):
                lookAt = [25,0,150]
            elif ((x == 244) and (z == 121)):
                lookAt = [230,0,150]
            
            lookAt = tuple(lookAt)
            return lookAt