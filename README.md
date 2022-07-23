# Behaviour Tree Demo

A simple demo I made to teach myself the basics of behaviour trees. This is a stripped down version of the Unity and C# course that can be found at https://www.udemy.com/course/behaviour-trees/, with some additions from my own personal research.

This example demonstrates:
- Action Nodes
- Condition Nodes
- Sequence Nodes
- Regular Selector Nodes
- Random Selector Nodes
- Inverters

## Usage and Expected Results

Run the sample application with `python btexample.py`. 

It starts by displaying a printout of the behaviour tree. The hierarchy is shown by indentation, just like in regular Python code, meaning that indented nodes on subsequent lines are children of the nodes on preceding lines, while nodes with the same indentation are at the same level of the tree.

After the tree structure has been displayed, press RETURN to run an execution of the behaviour tree. The behaviour tree runs until the character has made $5000000 or you terminate it with `Ctrl+C`.

## Graph Theory Crash Course

A graph G is mathematical object defined as G := {V, E}, where V is a set of vertices (also known as nodes), and E is a list of edges. Edges connect two vertices/nodes. An edge can be unidirectional or bidirectional. In a unidirectional edge, you can only travel from the start node to the end node, and not backwards (from end to start), while in a bidirectional edge, you can go both ways. A graph containing at least one unidirectional edge is known as a directed graph.

A cycle in a graph occurs when you can start at a specific node and follow a path along other nodes, specified by the edges to return to the starting node. Acyclic graphs don't contain any cycles.

A tree is a directed acyclic graph that starts at a single node called the root node that all the other edges branch off from.

Due to the directionality of edges in trees, a hierarchy of nodes can be established. If two nodes A and B are connected by an edge that points from node A to node B, node A is known as the parent node and node B is known as the child node. Due to the definition of a tree, each node can only have one parent node, but can have multiple child nodes.

Child nodes and children of child nodes are known as descendants of a specific node. For example, if we added a node C to the above example, nodes B and C would be considered to be descendants of node A. Similarly, node A is considered to be the ancestor of nodes B and C.

The root node by definition has no parent, and is the ancestor of all nodes in the tree.

An internal node (also called a branch node) is a node that has children, while an external node (also called terminal node or leaf) has no children. Using the analogy of a biological tree, a branch can have multiple sub-branches or leaves, but nothing branches off a leaf in a tree (not a plant biologist, please don't kill me).

Trees have a wide variety of applications in computer science, both as storage and information retrieval structures eg. binary search trees and tries. 

## What Is A Behaviour Tree?

A behaviour tree is a tree that structures switching between different tasks in an autonomous (self-controlling) agent. They were initially developed to control non-player characters (NPCs) in video game AI, but have since found use in controlling other autonomous agents, such as robots. 

Each node in a behaviour tree performs a specific logical operation and can return one of three states: SUCCESS, RUNNING or FAILED. This state is passed to the parent node, which in turn determines what is done with this state by its own logical rules. This can back-propagate up to the root node of the tree, which generates the driving signal for each evaluation of the state of the tree (known as a tick). 

All nodes in a behaviour tree can be classified into one of three types:
- Leaf nodes
- Decorator nodes
- Composite nodes

Leaf nodes have no children, and are used to perform an action or check a condition. Decorator nodes have one child, and are often used to modify the result of that child. Composite nodes consist of one or more children nodes.

In essence a behaviour tree acts as a higher level programming language on top of your actual language, giving the sequence of instructions you want your autonomous agents to follow, with the addition of features such as conditionality.

### Leaf Nodes

Leaf nodes are generally considered to be the interface between your application logic and the tree logic. The two major types of leaf nodes are action nodes and conditional nodes. 

The execution of a conditional node checks if a condition is true, and returns SUCCESS or FAILED. The execution of an action node tries to complete an action and returns SUCCESS if it worked, FAILED if it didn't, and RUNNING if the action is still being performed. In a game, these will generally specify the actions that the NPC will take or the conditions that they will check.

### Decorator Nodes

These always have one child node, whose result they modify. The commonest example is the inverter node, which corresponds to a NOT gate. For example, if we have a conditional node that asks "Is the area safe?", we expect it to return SUCCESS if the area is safe, or FAILED if the area is not. If we attach it to an inverter node, the question becomes "Is the area unsafe?".

### Composite Nodes

Composite nodes have one or more children. You can create your own type of composite nodes (technically, you can create your own variant of any type of node), but the commonest ones are:
- Sequence
- Selector/Fallback
- Parallel

#### Sequence Nodes

A sequence node operates somewhat like an AND logical gate. It generally has multiple children, and keeps track of the current child that is being executed.

The rules are as follows:
- It will iterate over and execute all of its children, as long as the child preceding the current one returns SUCCESS. 
- If all the children return SUCCESS, the sequence node itself will return SUCCESS after the last child has been executed. 
- If any child returns FAILED, the sequence node will terminate the iteration and return FAILED. 
- If all the children so far have returned SUCCESS, but the sequence node has not iterated over all its children, it will return RUNNING.
- If either SUCCESS or FAILED is returned, the current child is reset to the first one.

#### Selector/Fallback Nodes

A selector node, also known as a fallback node operates like an OR logical gate. Just like the sequence node, it generally has multiple children and keeps track of the current child that is being executed.

The rules are as follows:
- It will iterate over its children until one of them returns SUCCESS.
- Until it has found that child, it returns RUNNING.
- If all the children have been iterated over, and none of them have returned SUCCESS, then the selector returns FAILED

#### Parallel Nodes

A parallel node is probably one of the more complex composite nodes to understand. A parallel node has N children (where N >= 1) and a success threshold M, which is the number of children that need to return SUCCESS for the parallel node itself to return SUCCESS.

The rules are as follows:
- All of the children of the parallel node are executed and the results are stored. 
- If the number of SUCCESS results is greater than or equal to M, then the node returns SUCCESS.
- Otherwise, if the number of failures is greater than N - M + 1, then it returns FAILED.
- The fall through case here is to return RUNNING.

The parallel node is so named because it runs in parallel, ie. it evaluates multiple nodes simultaneously to determine the result. As an example, given a parallel node with 5 children (N = 5) and M = 3:
- If 3 or more nodes return SUCCESS, then the parallel node returns SUCCESS
- If 3 or more nodes return FAILURE, then the parallel node returns failure (5 - 3 + 1)
- Otherwise, the node returns RUNNING

## Practical Considerations

### Statefulness and Long-Running Actions

It is generally advisable keep statefulness in the nodes of a behaviour tree to a minimum. Minimum is relative (since nodes contain information about their children, and sometimes a priority ranking), and this isn't a hard and fast rule, but this guidance should help to reduce the chances of undefined behaviour due to some variable having an expected value. The rule was broken in this example for the sake of simplicity, but its stated here for the sake of completeness.

The execution style of a leaf or decorator node can be said to be instant or continuous. A leaf node with an instant execution style evaluates and returns a result immediately. One with a continuous execution style evaluates until some condition is met then returns SUCCESS or FAILED. Nodes with a continuous execution style are important for long running tasks that don't instantly succeed or fail (eg. pathfinding towards a target in a game).

Many times, nodes with a continuous execution style need to maintain some state in order to carry out their actions and properly evaluate if they have succeeded or failed. This can easily turn into a kludge, with lots of variables cluttering the body of the agent class in question to help maintain state.

One way around this is creating a custom TaskRunnerNode, and deriving classes from it for actions that you expect to be continuously executed. I didn't use it in this example, but I've included a sample of how it could be structured in taskrunnernode.py.The task runner node defines functions for onStart, onRunTask and onExit, corresponding to the node lifecycle. These should be overriden in the derived node. The simplified operation of the TaskRunnerNode is as follows:
- When the node is first switched to, onStart() is executed
- For as long as the task is incomplete, the specifics of the logic take place in OnRunTask(), and it returns RUNNING
- When the task is either SUCCESS or FAILED, onExit() is called, and this carries out cleanup logic and resets the node for future usage.

Nodes with a continuous execution style aren't only limited to being actions, they can also be conditions ie. monitoring nodes. These nodes continuously evaluate a condition and allow processing to continue to the child nodes or fail out depending on the outcome.

### Inventing New Nodes

Custom node types can be created to meet specific nodes. Some examples are:
- Random selectors - pick a random child to execute until one returns SUCCESS
- Priority selectors - which evaluate children in order of an explicitly specified priorities, which can be dynamically reprioritized


