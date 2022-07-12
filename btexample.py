from argparse import Action
from core.behaviourtree import BehaviourTree
from core.node import Node
from core.actionnode import ActionNode
from core.sequencenode import SequenceNode
from core.selectornode import SelectorNode
from core.conditionnode import ConditionNode

from enum import Enum
import random
import time
import sys


class ValuableTheftStatus(Enum):
    NONE = 0
    DIAMOND_STOLEN = 1
    PAINTING_STOLEN = 2
    ALREADY_SOLD = 3

walletChecked = False
theftDecided = False
planDevised = False
valuableStolen = ValuableTheftStatus.NONE
vanEscaped = False
balance = 0

def evaluate_checkWallet():
    global walletChecked
    if not walletChecked:
        walletChecked = True

        print("Checking my wallet to see if it's crime time")
        if balance < 5000000:
            print(f"Current balance {balance}")
            print("I'm broke, time to pull off another heist.")
            return Node.STATE_SUCCESS
        else:
            print("Let me lay low for now.")
            print("=====================")
            print("\n\nExecution complete")
            sys.exit(0)
            walletChecked = False
            return Node.STATE_FAILED
    else:
        return Node.STATE_SUCCESS

def evaluate_successfulEscape():
    escapeChance = random.randrange(0, 10)
    if escapeChance <= 2:
        print("NOOOO! Got caught by the cops!")
        print("Got sentenced and now I'm languishing in prison for my crimes")
        return Node.STATE_FAILED
    else:
        print("I evaded the museum security!")
        return Node.STATE_SUCCESS

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
    if valuableStolen == ValuableTheftStatus.NONE:
        chance = random.randrange(0, 10, 1)

        if chance <= 3:
            valuableStolen = ValuableTheftStatus.DIAMOND_STOLEN
            print("Managed to steal the diamond!")
        else:
            return Node.STATE_FAILED
    else:
        pass
        #print("I already stole the diamond, I need to get away")
    return Node.STATE_SUCCESS

def tick_stealPainting():
    global valuableStolen
    if valuableStolen == ValuableTheftStatus.NONE:
        valuableStolen = ValuableTheftStatus.PAINTING_STOLEN
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

def tick_pawnItem():
    global valuableStolen
    global balance

    if valuableStolen == ValuableTheftStatus.DIAMOND_STOLEN:
        print("Pawned the stolen diamond and made a tidy sum!")
        balance += 1000000
    elif valuableStolen == ValuableTheftStatus.PAINTING_STOLEN:
        print("Sold the stolen painting for a pretty penny!")
        balance += 500000
    else:
        #Set it to a third state to prevent errors when the tree is being re_evaluated
        valuableStolen = ValuableTheftStatus.ALREADY_SOLD

    return Node.STATE_SUCCESS

def tick_payLawyer():
    global balance
    print("Paid my lawyer to get me out of prison - he didn't come cheap")
    balance = round(balance * 0.5)
    return Node.STATE_SUCCESS

def tick_leavePrison():
    global theftDecided
    global planDevised
    global vanEscaped
    global walletChecked
    global valuableStolen

    print("Well that sucked! I'm happy to be a free man again.")
    theftDecided = False
    planDevised = False
    vanEscaped = False
    walletChecked = False
    valuableStolen = ValuableTheftStatus.NONE
    return Node.STATE_SUCCESS


def tick_nextHeist():
    global theftDecided
    global planDevised
    global vanEscaped
    global walletChecked
    global valuableStolen

    print("Great heist guys, let's prepare for the next one")
    theftDecided = False
    planDevised = False
    vanEscaped = False
    walletChecked = False
    valuableStolen = ValuableTheftStatus.NONE
    return Node.STATE_SUCCESS

if __name__ == '__main__':

    random.seed()

    tree = BehaviourTree("Root")
    plottingPhase = SequenceNode("Plotting phase")
    checkFinancialStatus = ConditionNode("Am I broke?", evaluate_checkWallet)
    decideToSteal = ActionNode("Decide to steal something", tick_decideOnTheft)
    startPlotting = ActionNode("Start the plotting", tick_devisePlan)
    executePlan = SequenceNode("Execute the plan")

    selectTarget = SelectorNode("Picking diamond or painting to steal")
    stealDiamondNode = ActionNode("Steal diamond", tick_stealDiamond)
    stealPaintingNode = ActionNode("Steal painting", tick_stealPainting)

    ending = SequenceNode("Make an exit")

    escapeSuccessful = ConditionNode("Managed to escape?", evaluate_successfulEscape)
    escapeToVan = ActionNode("Escape by van", tick_escapeVan)
    sellValuable = ActionNode("Sell stolen valuable", tick_pawnItem)
    celebrate = ActionNode("Celebrate heist", tick_nextHeist)

    goToPrison = SequenceNode("Go To Prison")
    payLawyer = ActionNode("Pay my lawyer", tick_payLawyer)
    getOutOfPrison = ActionNode("Leave prison", tick_leavePrison)
    goToPrison.addChild(payLawyer)
    goToPrison.addChild(getOutOfPrison)

    plottingPhase.addChild(checkFinancialStatus)
    plottingPhase.addChild(decideToSteal)
    plottingPhase.addChild(startPlotting)
    plottingPhase.addChild(executePlan)
    tree.addChild(plottingPhase)

    executePlan.addChild(selectTarget)    
    selectTarget.addChild(stealDiamondNode)
    selectTarget.addChild(stealPaintingNode)
    executePlan.addChild(ending)
    executePlan.addChild(goToPrison)

    ending.addChild(escapeSuccessful)
    ending.addChild(escapeToVan)
    ending.addChild(sellValuable)
    ending.addChild(celebrate)

    print("\n\nTree Structure")
    print("========================\n")
    tree.display(0)

    input()
    print("Tree execution")
    print("========================\n")

    while(True):
        tree.process()
        time.sleep(0.5)