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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    initial_state = (problem.getStartState(), None, None)
    open_stack = util.Stack()
    open_stack.push(initial_state)
    closed_list = []
    solution_list = {}
    solution_list[initial_state[0]] = None

    while not open_stack.isEmpty():
        curr_node = open_stack.pop()

        if curr_node in closed_list:
            continue

        closed_list.append(curr_node[0])

        if problem.isGoalState(curr_node[0]):
            result = []
            while curr_node != None:
                result.append(curr_node[1])
                curr_node = solution_list[curr_node[0]]
            return list(reversed(result[:-1]))
        else:
            for successor in problem.getSuccessors(curr_node[0]):
                if (successor[0] not in closed_list) and (successor not in open_stack.list):
                    open_stack.push(successor)
                    solution_list[successor[0]] = curr_node

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    initial_state = (problem.getStartState(), None, -1)
    open_queue = util.Queue()
    open_queue.push(initial_state)
    closed_list = []
    solution_list = {}
    solution_list[initial_state[0]] = []

    while not open_queue.isEmpty():
        curr_node = open_queue.pop()

        if curr_node[0] in closed_list:
            continue

        closed_list.append(curr_node[0])

        if problem.isGoalState(curr_node[0]):
            result = []
            while curr_node != None:
                result.append(curr_node[1])
                if solution_list[curr_node[0]]:
                    curr_node = min(solution_list[curr_node[0]], key = lambda node: node[2])
                else:
                    curr_node = None
            return list(reversed(result[:-1]))
        else:
            for successor in problem.getSuccessors(curr_node[0]):
                if (successor[0] not in closed_list):
                    open_queue.push(successor)
                    if successor[0] not in solution_list:
                        solution_list[successor[0]] = []
                    solution_list[successor[0]].append(curr_node)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    initial_state = (problem.getStartState(), None, 0)
    open_queue = util.PriorityQueue()
    open_queue.push(initial_state, float('inf'))
    closed_list = []
    solution_list = {}
    solution_list[initial_state[0]] = util.PriorityQueue()

    while not open_queue.isEmpty():
        curr_node = open_queue.pop()

        if curr_node[0] in closed_list:
            continue

        closed_list.append(curr_node[0])

        if problem.isGoalState(curr_node[0]):
            result = []
            while curr_node != None:
                result.append(curr_node[1])
                if not solution_list[curr_node[0]].isEmpty():
                    curr_node = solution_list[curr_node[0]].pop()
                else:
                    curr_node = None
            return list(reversed(result[:-1]))
        else:
            for successor in problem.getSuccessors(curr_node[0]):
                if (successor[0] not in closed_list):
                    combined_cost = curr_node[2] + successor[2]
                    open_queue.update((successor[0], successor[1], combined_cost), combined_cost)
                    if successor[0] not in solution_list:
                        solution_list[successor[0]] = util.PriorityQueue()
                    solution_list[successor[0]].update(curr_node, combined_cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    initial_state = (problem.getStartState(), None, 0)
    open_queue = util.PriorityQueue()
    open_queue.push(initial_state, float('inf'))
    closed_list = []
    solution_list = {}
    solution_list[initial_state[0]] = util.PriorityQueue()

    while not open_queue.isEmpty():
        curr_node = open_queue.pop()

        if curr_node[0] in closed_list:
            continue

        closed_list.append(curr_node[0])

        if problem.isGoalState(curr_node[0]):
            result = []
            while curr_node != None:
                result.append(curr_node[1])
                if not solution_list[curr_node[0]].isEmpty():
                    curr_node = solution_list[curr_node[0]].pop()
                else:
                    curr_node = None
            return list(reversed(result[:-1]))
        else:
            for successor in problem.getSuccessors(curr_node[0]):
                if (successor[0] not in closed_list):
                    combined_cost = curr_node[2] + successor[2]
                    combined_cost_with_heuristic = combined_cost + heuristic(successor[0], problem)
                    open_queue.update((successor[0], successor[1], combined_cost), combined_cost_with_heuristic)
                    if successor[0] not in solution_list:
                        solution_list[successor[0]] = util.PriorityQueue()
                    solution_list[successor[0]].update(curr_node, combined_cost_with_heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
