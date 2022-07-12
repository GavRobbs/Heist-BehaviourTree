
#A generic node class - this is only really used for the root node of the tree.
#All other nodes are usually one of the other subtypes
class Node:
    STATE_SUCCESS = 0
    STATE_FAILED = 1
    STATE_RUNNING = 2

    def __init__(self, name="Node"):
        self.status = Node.STATE_FAILED
        self.children = []
        self.currentChild = 0
        self.name = name

    def addChild(self, childNode):
        self.children.append(childNode)

    def display(self, indent):
        #Recursively print this node and its kids with proper indentation
        print('\t'*indent + self.name)
        
        for child in self.children:
            child.display(indent)

    def process(self):
        return self.children[self.currentChild].process()

    