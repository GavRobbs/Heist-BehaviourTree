from core.behaviourtree import BehaviourTree
from core.node import Node
from core.actionnode import ActionNode
from core.sequencenode import SequenceNode
from core.selectornode import SelectorNode

import random
import time

theftDecided = False
planDevised = False
valuableStolen = False
vanEscaped = False

def tick_decideOnTheft():
    global theftDecided
    if not theftDecided:
        theftDecided = True
        print("Made up my mind to steal something")
    else:
        pass
        #print("Already made up my mind to steal something")
    return Node.STATE_SUCCESS

def tick_devisePlan():
    global planDevised
    if not planDevised:
        planDevised = True
        print("Devised a plan to steal")
    else:
        pass
        #print("I already devised a plan to steal a diamond")
    return Node.STATE_SUCCESS

def tick_stealDiamond():
    global valuableStolen
    if not valuableStolen:
        chance = random.randrange(0, 10, 1)

        if chance <= 3:
            valuableStolen = True
            print("Managed to steal the diamond!")
        else:
            return Node.STATE_FAILED
    else:
        pass
        #print("I already stole the diamond, I need to get away")
    return Node.STATE_SUCCESS

def tick_stealPainting():
    global valuableStolen
    if not valuableStolen:
        valuableStolen = True
        print("Managed to steal the painting!")
    else:
        pass
        #print("I already stole the diamond, I need to get away")
    return Node.STATE_SUCCESS

def tick_escapeVan():
    global vanEscaped
    if not vanEscaped:
        vanEscaped = True
        print("I got away in my van!")
    else:
        pass
        #print("I'm currently getting away in my van")
    return Node.STATE_SUCCESS

def tick_nextHeist():
    global theftDecided
    global planDevised
    global valuableStolen
    global vanEscaped

    print("Great heist guys, let's prepare for the next one")
    theftDecided = False
    planDevised = False
    valuableStolen = False
    vanEscaped = False
    return Node.STATE_SUCCESS

if __name__ == '__main__':

    random.seed()

    tree = BehaviourTree("Root")
    plottingPhase = SequenceNode("Plotting phase")
    decideToSteal = ActionNode("Decide to steal something", tick_decideOnTheft)
    startPlotting = ActionNode("Start the plotting", tick_devisePlan)
    executePlan = SequenceNode("Execute the plan")

    selectTarget = SelectorNode("Picking diamond or painting to steal")
    stealDiamondNode = ActionNode("Steal diamond", tick_stealDiamond)
    stealPaintingNode = ActionNode("Steal painting", tick_stealPainting)

    ending = SequenceNode("Make an exit")

    escapeToVan = ActionNode("Escape by van", tick_escapeVan)
    celebrate = ActionNode("Celebrate heist", tick_nextHeist)

    plottingPhase.addChild(decideToSteal)
    plottingPhase.addChild(startPlotting)
    plottingPhase.addChild(executePlan)
    tree.addChild(plottingPhase)

    executePlan.addChild(selectTarget)    
    selectTarget.addChild(stealDiamondNode)
    selectTarget.addChild(stealPaintingNode)
    executePlan.addChild(ending)

    ending.addChild(escapeToVan)
    ending.addChild(celebrate)

    tree.display(0)

    input()

    while(True):
        tree.process()
        time.sleep(1)