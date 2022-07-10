from .node import Node

class BehaviourTree(Node):
    def __init__(self, name):
        super().__init__(name)

    def process(self):
        self.children[self.currentChild].process()