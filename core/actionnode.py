from .node import Node

class ActionNode(Node):
    def __init__(self, name, tick_func = None):
        super().__init__(name)
        self.tick = tick_func

    def display(self, indent):
        print('\t'*indent + "Action: " + self.name)

    def process(self):
        #This would be the leaf (end node) of the behaviour tree
        #and represents a specific action. The tick function would contain
        #the details of the action and if it was successful or not
        if self.tick != None:
            return self.tick()
        
        return Node.STATE_FAILED