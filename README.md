# Behaviour Tree Demo

A simple demo I made to teach myself the basics of behaviour trees. This is a stripped down version of the Unity and C# course that can be found at https://www.udemy.com/course/behaviour-trees/.

This example demonstrates:
- Action Nodes
- Condition Nodes
- Sequence Nodes
- Selector Nodes
- Inverters

## Usage and Expected Results

Run the sample application with `python btexample.py`. 

It starts by displaying a printout of the behaviour tree. The hierarchy is shown by indentation, just like in regular Python code, meaning that indented nodes on subsequent lines are children of the nodes on preceding lines, while nodes with the same indentation are at the same level of the tree.

After the tree structure has been displayed, press RETURN to run an execution of the behaviour tree. The behaviour tree runs until the character has made $5000000 or you terminate it with `Ctrl+C`.