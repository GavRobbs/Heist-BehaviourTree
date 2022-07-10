from .node import Node

class ActionNode(Node):
    def __init__(self, name, tick_func = None):
        super().__init__(name)
        self.tick = tick_func

    def display(self, indent):
        print('\t'*indent + "Action: " + self.name)

    def process(self):
        if self.tick != None:
            return self.tick()
        
        return Node.STATE_FAILED