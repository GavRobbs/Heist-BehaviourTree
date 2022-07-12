from .node import Node

#An inverter node negates the result of its child
#It is considered a decorator, and should only have a single child by definition
class InverterNode(Node):
    def __init__(self, name):
        super().__init__(name)

    def display(self, indent):
        print('\t'*indent + "Inverter: " + self.name)

        indent += 1
        self.children[0].display(indent)

    def addChild(self, child):
        #We only want to use the child at index 0, since it shouldn't have multiple children
        if len(self.children) == 0:
            self.children.append(child)
        else:
            self.children[0] = child

    def process(self):        
        childstatus = self.children[0].process()

        if childstatus == Node.STATE_RUNNING:
            return Node.STATE_RUNNING
        elif childstatus == Node.STATE_FAILED:
            return Node.STATE_SUCCESS
        elif childstatus == Node.STATE_SUCCESS:
            self.currentChild = 0
            return Node.STATE_FAILED