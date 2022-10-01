from .node import Node

#This is one of the leaf/end nodes of the behaviour tree and represents a specific action. 
#The tick function runs the action and returns if it was successful or not
class ActionNode(Node):
    def __init__(self, name, tick_func = None):
        super().__init__(name)
        self.tick = tick_func

    def display(self, indent):
        print('\t'*indent + "Action: " + self.name)

    def process(self):
        if self.tick != None:
            return self.tick(self.blackboard)
        
        return Node.STATE_FAILED