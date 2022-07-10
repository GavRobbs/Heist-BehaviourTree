from .node import Node

class SequenceNode(Node):
    def __init__(self, name):
        super().__init__(name)

    def display(self, indent):
        print('\t'*indent + "Sequence: " + self.name)

        indent += 1
        for child in self.children:
            child.display(indent)

    def process(self):
        #A sequence node progresses along all of its children
        #as long as each child returns success, basically a logical AND   
        childstatus = self.children[self.currentChild].process()

        if childstatus == Node.STATE_RUNNING:
            return Node.STATE_RUNNING
        elif childstatus == Node.STATE_FAILED:
            self.currentChild = 0
            return Node.STATE_FAILED
        elif childstatus == Node.STATE_SUCCESS:
            self.currentChild = (self.currentChild + 1) % len(self.children)
            return Node.STATE_SUCCESS