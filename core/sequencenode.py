from .node import Node

#A sequence node processes all of its children until it reaches one that returns false (logical AND)  
class SequenceNode(Node):
    def __init__(self, name):
        super().__init__(name)

    def display(self, indent):
        print('\t'*indent + "Sequence: " + self.name)

        indent += 1
        for child in self.children:
            child.display(indent)

    def process(self):
        childstatus = self.children[self.currentChild].process()

        if childstatus == Node.STATE_RUNNING:
            return Node.STATE_RUNNING

        if childstatus == Node.STATE_FAILED:
            self.currentChild = 0
            return Node.STATE_FAILED
        
        if childstatus == Node.STATE_SUCCESS:
            self.currentChild += 1
            if self.currentChild == len(self.children):
                self.currentChild = 0
                return Node.STATE_SUCCESS

        return Node.STATE_RUNNING