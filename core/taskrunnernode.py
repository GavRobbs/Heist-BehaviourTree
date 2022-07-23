from tkinter import N
from .node import Node

#The TaskRunnerNode for continuous actions. Derive from this and reimplement onStart(), onRunTask() and onExit(),
#when you're creating your own long running actions
class TaskRunnerNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self._started = False

    def display(self, indent):
        print('\t'*indent + "Task Runner: " + self.name)

        indent += 1
        for child in self.children:
            child.display(indent)
    
    def onStart(self):
        pass

    def onRunTask(self):
        return Node.STATE_RUNNING

    def onExit(self):
        pass

    def process(self):
        if not self._started:
            self.onStart()
            self._started = True
        
        status = self.onRunTask()

        if status != Node.STATE_RUNNING:
            self._started = False
            self.onExit()
            return status
        
        return Node.STATE_RUNNING