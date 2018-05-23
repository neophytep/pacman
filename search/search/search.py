  # search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
#    print "Start:", problem.getStartState()
##    print problem.getStartState()[0], problem.getStartState()[1]
#    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
#    suc = problem.getSuccessors(problem.getStartState())
#    print "Start's successors:", problem.getSuccessors(problem.getStartState())
#    print problem.getSuccessors(suc[0][0])
#    util.raiseNotDefined()
#    print "Cost of actions:", problem.getCostOfActions(['South', s, w, s, w, w, s, w])
    return  ['South', s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
#    print "Start:", problem.getStartState()
#    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
#    print "Start's successors:", problem.getSuccessors(problem.getStartState())
       
    return genericSearch('dfs').search(problem)
    util.raiseNotDefined()
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    return genericSearch('bfs').search(problem)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return genericSearch('ucs').search(problem)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return genericSearch('astar', heuristic).search(problem)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

class genericSearch:
    def __init__(self, method, heuristic = None):
        self.method = method
        self.heuristic = heuristic
        if method == 'dfs':
            self.fringe = util.Stack()
        elif method == 'bfs':
            self.fringe = util.Queue()
        elif method == 'ucs' or method == 'astar':
            self.fringe = util.PriorityQueue()
            
    def push(self, state, priority = None):
        if self.method == 'dfs' or self.method == 'bfs':
            self.fringe.push(state)
        elif self.method == 'ucs' or self.method == 'astar':
            self.fringe.push(state, priority)
            
    def pop(self):
        return self.fringe.pop()
        
    def isEmpty(self):
        return self.fringe.isEmpty()
            
    def search(self, problem):
#        a search node contains: (state, lastaction, parentnode, accumulative cost)
        seen = set()
        self.push(  (problem.getStartState(), None, None, 0)  )
#        seen.add(problem.getStartState())        
        while not self.isEmpty():
            node = self.pop()
            state, action, parent, costs = node
#            seen.add(state)

            if state in seen:
                continue
            seen.add(state)
            
            if problem.isGoalState(state):
                actions = []
                n = node
                while n[0] != problem.getStartState():
                    actions.append(n[1])
                    n = n[2]
                actions.reverse()
                return actions

            for nextState, action, cost in problem.getSuccessors(state):
                if nextState in seen:
                    continue
                
                priority = 0
                if self.method == 'ucs': 
                    priority = costs + cost
                elif self.method == 'astar':
                    priority = costs + cost + self.heuristic(nextState, problem)

                self.push((nextState, action, node, costs + cost), priority)