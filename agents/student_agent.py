# Student agent: Add your own agent here
# AlphaCS
from agents.agent import Agent
from store import register_agent
import math;
import time;
import random;

import sys
# from memory_profiler import profile;
import tracemalloc;

class BoardState:
        def __init__(self, chess_board, my_pos, adv_pos, max_step):
            self.board = chess_board;
            self.myPosition = my_pos;
            self.advPosition = adv_pos;
            self.maxStep = max_step;

        def getBoard(self):
            return self.board;

        def getMyPos(self):
            return self.myPosition;

        def getAdvPos(self):
            return self.advPosition;

        def getMaxStep(self):
            return self.maxStep;

        def setBoardState(self, chess_board, my_pos, adv_pos, max_step):
            self.board = chess_board;
            self.myPosition = my_pos;
            self.advPosition = adv_pos;
            self.maxStep = max_step;

class MCTSNode:
    def __init__(self):
        self.nodeState = None;
        self.parent = None;
        self.childList = [];

    def setParent(self, parent):
        self.parent = parent;

    def getParent(self):
        return self.parent;
    
    def setState(self, state):
        self.state = state;

    def getState(self):
        return self.state;
    
    def addChildNode(self, child):
        self.childList.append(child);

    def getChildren(self):
        return self.childList;

    def getRandomChild(self):
        # Get a random child from the list 
        if(self.childList == []): #Double check that this is sufficient for verifying empty list.
            return None;
        return random.choice(self.childList);

    def getMaxScoreChild(self):
        # Get the child with the highest 'visitCount' (I think. Review and get max number according to tree policy) ***
        return None;

class MCTSTree:
    def __init__(self, node: MCTSNode):
        self.root = node;

    def setRoot(self, node: MCTSNode):
        self.root = node;

    def getRoot(self):
        return self.root;

    def addChild(self, parentNode: MCTSNode, childNode: MCTSNode):
        parentNode.addChildNode(childNode);

class State:
    
    def __init__(self, boardState):
        self.boardState = boardState
        self.visitCount = 0; #Could put these two in 'Node' Instead, and have just a 'board state'
        self.winScore = 0;

    def getVisitCount(self):
        return self.visitCount;

    def setVisitCount(self, newCount):
        self.visitCount = newCount;

    def incrementVisit(self):
        self.visitCount = self.visitCount + 1;

    def getWinScore(self):
        return self.winScore;

    def setWinScore(self, newScore):
        self.winScore = newScore;

    def addWinScore(self, scoreToAdd):
        self.winScore = self.winScore + scoreToAdd;

    def getAllStates(self):
        # Get all possible moves, and return them in a list of States. *** This might end up being very expensive. Edit to be a subset of states if need be.
        return None;

    def randomMove(self):
        # Uses BoardState to figure out a random move. Can likely snag random agent code to do this!
        return None;

# Probably doesn't need to be its own class.
class UCT:
    def findBestUCTNode(node):
        parentVisitCount = node.getState().visitCount();
        # Foreach child in node.getChildArray, get the one with the highest UCTValue(parentVisitCount, childNode.getState().getWinScore(), childNode.getState().getVisitCount()) ***
        return None;

    def UCTValue(totalVisits, winScore, visitCountNode): 
        if(visitCountNode == 0):
            return 9999; #Maybe double check if we can use INTEGER_MAXVAL or something instead.
        return (winScore / visitCountNode) + 1.41 * math.sqrt(math.log(totalVisits) /  visitCountNode) #Check that this isnt integer division - would cause unpredictable behavior. Also the 'c' value (1.41) can be tuned. ***

@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    def valid_move(cur_pos, x, y, dir, max_x, max_y):
        #Check for Board Dimension & Blockage
        return (0 <= x < max_x and 0 <= y < max_y and not dir.barrier)

    #@profile
    def step(self, chess_board, my_pos, adv_pos, max_step):
        tracemalloc.start();
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """
        init_pos = my_pos
        timelimit = 1750; # Tried 2000ms (2s) but results came out 2.3s so this seems to be about as high as we can safely go.
        startTime = time.time() * 1000;
        stateList = [];

        targetLevel = 2;

        # *** Create a node based on the passed in state, make it the root of the tree

        while((time.time() * 1000) < startTime + timelimit):
            #These two lines only here for speed/memory testings
            copiedState = BoardState(chess_board, my_pos, adv_pos, 2);
            stateList.append(copiedState);

            #node = root_node;
            # Step 1: Select a promising node (should be a root at the start)
            # while node is not a leaf
            #   n = select_UCB_node(n)
            # Step 2: Expand the node   
            # n.expand_node()
            # n = select_UCB_node(n)
            # Step 3: Simulate random game
            # while not terminal(n.state)
            #   n.state.simulate() # or just call a function to do it all in one shot
            # result = n.state.evaluate()
            # Step 4: Backpropagation 
            # while n.has_parent()
            #   n.update(result)
            #   n = n.parent()

        print(tracemalloc.get_traced_memory());
        tracemalloc.stop();
        print((time.time() * 1000) - startTime);
        # dummy return
        #return tree.best_move()
        return my_pos, self.dir_map["u"]


"""
CHECKLIST:
- Need a function to check that a state is terminal (can likely steal from world.py)
- Need function to get possible moves (node expansion)
- Need a function to simulate random moves until the end
- Need a function to properly select a UCT node
- Need to setup initial tree structure in step(), and should also reorganize helper classes
- Need a function to check that a given state in the tree is a leaf
- Need a function to evaluate a node's value given a state.
- Need a function to update a node's value (backpropagation)

MCTS:
- Need a way to do several random simulations
- Need a tree policy and a leaf/default policy (Look-Ahead Tree)
  Q*(s,a,h) = E[R(s,a) + βV*(T(s,a),h-1)]
"""
