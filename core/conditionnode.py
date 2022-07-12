from .node import Node

#This is one of the leaf/end nodes of the behaviour tree and represents the evaluation of a condition.
#The function to do this evaluation is passed as evaluator_func.
#The difference between this and the ActionNode is mostly semantic, in that the ActionNode
#expects an action to be performed in its tick function, while the ConditionNode only really
#expects a condition to be evaluated in its evaluator.
#Also note that the default state for a ConditionNode is success, as opposed to an ActionNode
#which is failure
class ConditionNode(Node):
    def __init__(self, name, evaluator_func = None):
        super().__init__(name)
        self.evaluator = evaluator_func

    def display(self, indent):
        print('\t'*indent + "Condition: " + self.name)

    def process(self):
        if self.evaluator != None:
            return self.evaluator()
        
        return Node.STATE_SUCCESS