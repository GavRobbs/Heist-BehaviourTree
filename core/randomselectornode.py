from .node import Node
import random
import math

#A random selector child picks a random child to evaluate until it returns SUCCESS
#We use -1 as a signal that the child is uninitialized so we need to generate a new
#random currentChild - otherwise we continue execution of the currently running child
#The scale variable exists to provide a greater range of randomness
class RandomSelectorNode(Node):
    def __init__(self, name, scale = 1):
        super().__init__(name)
        self.currentChild = -1
        self.scale = scale

    def display(self, indent):
        print('\t'*indent + "Random Selector: " + self.name)

        indent += 1
        for child in self.children:
            child.display(indent)

    def process(self):

        if self.currentChild == -1:
            #Using randrange instead of randint because I don't want to
            #include the endpoint
            self.currentChild = random.randrange(0, len(self.children) * self.scale)

        childstatus = self.children[math.floor(self.currentChild / self.scale)].process()

        if childstatus == Node.STATE_RUNNING:
            return Node.STATE_RUNNING
        else:
            self.currentChild = -1
            return childstatus         