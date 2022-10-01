from argparse import Action
from glob import glob
from core.behaviourtree import BehaviourTree
from core.node import Node
from core.actionnode import ActionNode
from core.sequencenode import SequenceNode
from core.selectornode import SelectorNode
from core.conditionnode import ConditionNode
from core.inverternode import InverterNode
from core.randomselectornode import RandomSelectorNode

from enum import Enum
import random
import time
import sys



class HeistBlackboard:

    class ValuableTheftStatus(Enum):
        NONE = 0
        DIAMOND_STOLEN = 1
        PAINTING_STOLEN = 2
        ALREADY_SOLD = 3

    def __init__(self):
        self.walletChecked = False
        self.theftDecided = False
        self.planDevised = False
        self.valuableStolen = HeistBlackboard.ValuableTheftStatus.NONE
        self.vanEscaped = False
        self.evadedSecurity = False
        self.notInPrison = True
        self.balance = 0

def evaluate_checkWallet(bb):
    if not bb.walletChecked:
        bb.walletChecked = True

        print("Checking my wallet to see if it's crime time")
        if bb.balance < 5000000:
            print(f"Current balance {bb.balance}")
            print("I'm broke, time to pull off another heist.")
            return Node.STATE_SUCCESS
        else:
            print("Let me lay low for now.")
            print("=====================")
            print("\n\nExecution complete")
            sys.exit(0)
    else:
        return Node.STATE_SUCCESS

def evaluate_successfulEscape(bb):
    if not bb.notInPrison:
        return Node.STATE_FAILED

    escapeChance = random.randrange(0, 15)
    if escapeChance <= 2:
        print("NOOOO! Got caught by the cops!")
        print("Got sentenced and now I'm languishing in prison for my crimes")
        bb.evadedSecurity = False
        bb.notInPrison = False
        return Node.STATE_FAILED
    else:
        print("I evaded the museum security!")
        bb.evadedSecurity = True
        bb.notInPrison = True
        return Node.STATE_SUCCESS

def evaluate_evadedSecurity(bb):
    if bb.notInPrison:
        return Node.STATE_SUCCESS
    else:
        return Node.STATE_FAILED

def tick_decideOnTheft(bb):
    if not bb.theftDecided:
        bb.theftDecided = True
        print("Made up my mind to steal something")
    else:
        pass
    return Node.STATE_SUCCESS

def tick_devisePlan(bb):
    if not bb.planDevised:
        bb.planDevised = True
        print("Devised a plan to steal")
    else:
        pass
        #print("I already devised a plan to steal a diamond")
    return Node.STATE_SUCCESS

def tick_stealDiamond(bb):
    if bb.valuableStolen == HeistBlackboard.ValuableTheftStatus.NONE:
        bb.valuableStolen = HeistBlackboard.ValuableTheftStatus.DIAMOND_STOLEN
        print("Managed to steal the diamond!")
    else:
        pass
    return Node.STATE_SUCCESS

def tick_stealPainting(bb):
    if bb.valuableStolen == HeistBlackboard.ValuableTheftStatus.NONE:
        bb.valuableStolen = HeistBlackboard.ValuableTheftStatus.PAINTING_STOLEN
        print("Managed to steal the painting!")
    else:
        pass
        #print("I already stole the diamond, I need to get away")
    return Node.STATE_SUCCESS

def tick_escapeVan(bb):
    if not bb.vanEscaped:
        bb.vanEscaped = True
        print("I got away in my van!")
    else:
        pass
        #print("I'm currently getting away in my van")
    return Node.STATE_SUCCESS

def tick_pawnItem(bb):

    if bb.valuableStolen == HeistBlackboard.ValuableTheftStatus.DIAMOND_STOLEN:
        print("Pawned the stolen diamond and made a tidy sum!")
        bb.balance += 1000000
    elif bb.valuableStolen == HeistBlackboard.ValuableTheftStatus.PAINTING_STOLEN:
        print("Sold the stolen painting for a pretty penny!")
        bb.balance += 500000
    else:
        #Set it to a third state to prevent errors when the tree is being re_evaluated
        bb.valuableStolen = HeistBlackboard.ValuableTheftStatus.ALREADY_SOLD

    return Node.STATE_SUCCESS

def tick_payLawyer(bb):
    print("Paid my lawyer to get me out of prison - he didn't come cheap")

    if bb.balance > 0:
        bb.balance = round(bb.balance * 0.65)
    else:
        bb.balance -= 300000
    return Node.STATE_SUCCESS

def tick_leavePrison(bb):
    print("Well that sucked! I'm happy to be a free man again.")
    bb.theftDecided = False
    bb.planDevised = False
    bb.vanEscaped = False
    bb.walletChecked = False
    bb.evadedSecurity = False
    bb.notInPrison = True
    bb.valuableStolen = HeistBlackboard.ValuableTheftStatus.NONE
    return Node.STATE_SUCCESS


def tick_nextHeist(bb):
    print("Great heist guys, let's prepare for the next one")
    bb.theftDecided = False
    bb.planDevised = False
    bb.vanEscaped = False
    bb.walletChecked = False
    bb.evadedSecurity = False
    bb.notInPrison = True
    bb.valuableStolen = HeistBlackboard.ValuableTheftStatus.NONE
    return Node.STATE_SUCCESS

if __name__ == '__main__':

    random.seed()

    tree = BehaviourTree("Root")
    phaseSelector = SelectorNode("Pick phase")
    plottingPhase = SequenceNode("Plotting phase")
    checkFinancialStatus = ConditionNode("Am I broke?", evaluate_checkWallet)
    decideToSteal = ActionNode("Decide to steal something", tick_decideOnTheft)
    startPlotting = ActionNode("Start the plotting", tick_devisePlan)
    executePlan = SequenceNode("Execute the plan")

    selectTarget = RandomSelectorNode("Picking diamond or painting to steal", 5)
    stealDiamondNode = ActionNode("Steal diamond", tick_stealDiamond)
    stealPaintingNode = ActionNode("Steal painting", tick_stealPainting)

    ending = SequenceNode("Make an exit")

    escapeSuccessful = ConditionNode("Managed to escape?", evaluate_successfulEscape)
    escapeToVan = ActionNode("Escape by van", tick_escapeVan)
    sellValuable = ActionNode("Sell stolen valuable", tick_pawnItem)
    celebrate = ActionNode("Celebrate heist", tick_nextHeist)

    checkFreedom = ConditionNode("Am I free?", evaluate_evadedSecurity)
    checkImprisonment = InverterNode("")
    checkImprisonment.addChild(checkFreedom)
    goToPrison = SequenceNode("Prison Phase")
    payLawyer = ActionNode("Pay my lawyer", tick_payLawyer)
    getOutOfPrison = ActionNode("Leave prison", tick_leavePrison)
    goToPrison.addChild(checkImprisonment)
    goToPrison.addChild(payLawyer)
    goToPrison.addChild(getOutOfPrison)

    plottingPhase.addChild(checkFinancialStatus)
    plottingPhase.addChild(decideToSteal)
    plottingPhase.addChild(startPlotting)
    plottingPhase.addChild(executePlan)
    
    phaseSelector.addChild(plottingPhase)
    phaseSelector.addChild(goToPrison)
    tree.addChild(phaseSelector)

    executePlan.addChild(selectTarget)    
    selectTarget.addChild(stealDiamondNode)
    selectTarget.addChild(stealPaintingNode)
    executePlan.addChild(escapeSuccessful)
    executePlan.addChild(ending)

    ending.addChild(escapeToVan)
    ending.addChild(sellValuable)
    ending.addChild(celebrate)

    tree.bind(HeistBlackboard())

    print("\n\nTree Structure")
    print("========================\n")
    tree.display(0)

    input("\n\nPress RETURN to proceed to tree execution")

    print("\nTree execution")
    print("========================\n")

    while(True):
        tree.process()
        time.sleep(0.5)