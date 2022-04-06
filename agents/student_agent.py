# Student agent: Add your own agent here
# AlphaCS
from tkinter import N
from agents.agent import Agent
from store import register_agent
import math;
import time;
import random;
import numpy as np;
from copy import deepcopy;

import sys
# from memory_profiler import profile;
import tracemalloc;

class BoardState:
        def __init__(self, chess_board, my_pos, adv_pos, max_step, myTurn):
            self.board = chess_board; #Deepcopy may not be needed? ***
            self.myPosition = my_pos;
            self.advPosition = adv_pos;
            self.maxStep = max_step;
            self.board_size = len(chess_board); # The 'M' value of the board.
            self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1));
            self.opposites = {0: 2, 1: 3, 2: 0, 3: 1}
            self.myTurn = myTurn; # true if it is this agent's turn, false otherwise

        def getBoard(self):
            return self.board;

        def getMyPos(self):
            return self.myPosition;

        def getAdvPos(self):
            return self.advPosition;

        def getSize(self):
            return self.board_size;

        def getMaxStep(self):
            return self.maxStep;

        def setBoardState(self, chess_board, my_pos, adv_pos, max_step):
            self.board = chess_board;
            self.myPosition = my_pos;
            self.advPosition = adv_pos;
            self.maxStep = max_step;

        def simulateRandomAction(self):
            if(self.myTurn):
                ori_pos = deepcopy(self.myPosition)
                steps = np.random.randint(0, self.maxStep + 1)

                # Random Walk
                for _ in range(steps):
                    r, c = self.myPosition;
                    dir = np.random.randint(0, 4)
                    m_r, m_c = self.moves[dir]
                    self.myPosition = (r + m_r, c + m_c)

                    # Special Case enclosed by Adversary
                    k = 0
                    while self.board[r, c, dir] or self.myPosition == self.advPosition:
                        k += 1
                        if k > 300:
                            break
                        dir = np.random.randint(0, 4)
                        m_r, m_c = self.moves[dir]
                        self.myPosition = (r + m_r, c + m_c)

                    if k > 300: #Is 300, but want to be fast. Tune this later 
                        #print(k);
                        self.myPosition = ori_pos
                        break

                # Put Barrier
                dir = np.random.randint(0, 4)
                r, c = self.myPosition
                #print("my");
                while self.board[r, c, dir]:
                    dir = np.random.randint(0, 4)
                    #print("Barrier repeat my")
                
                self.myTurn = False;
                self.board[r, c, dir] = True;
                move = self.moves[dir]
                self.board[r + move[0], c + move[1], self.opposites[dir]] = True
                return dir;
            else:
                steps = np.random.randint(0, self.maxStep + 1)
                ori_pos = deepcopy(self.advPosition)
                # Random Walk
                for _ in range(steps):
                    r, c = self.advPosition;
                    dir = np.random.randint(0, 4)
                    m_r, m_c = self.moves[dir]
                    self.advPosition = (r + m_r, c + m_c)

                    # Special Case enclosed by Adversary
                    k = 0
                    while self.board[r, c, dir] or self.myPosition == self.advPosition:
                        k += 1
                        if k > 300:
                            #print(k);
                            break
                        dir = np.random.randint(0, 4)
                        m_r, m_c = self.moves[dir]
                        self.advPosition = (r + m_r, c + m_c)

                    if k > 300: #Was 300, but want to be fast. Tune this later and see the effect ***
                        self.advPosition = ori_pos
                        break

                # Put Barrier
                dir = np.random.randint(0, 4)
                r, c = self.advPosition
                #print("adv");
                while self.board[r, c, dir]:
                    dir = np.random.randint(0, 4)
                    print("Barrier repeat adv") #*******************************************************
                self.myTurn = True;
                self.board[r, c, dir] = True;
                move = self.moves[dir]
                self.board[r + move[0], c + move[1], self.opposites[dir]] = True
                
            return None; # This function is used when computing random states - we don't need to save or return anything.

        # Similar to the 'check_endgame()' function from world.py. Returns the amt of points the player has won (0 for loss, 0.5 for tie, 1 for win) or a -1 if it is not the terminal state.
        def endCheck(self):
            #    Union-Find
            father = dict()
            for r in range(self.board_size):
                for c in range(self.board_size):
                    father[(r, c)] = (r, c)

            def find(pos):
                if father[pos] != pos:
                    father[pos] = find(father[pos])
                return father[pos]

            def union(pos1, pos2):
                father[pos1] = pos2

            for r in range(self.board_size):
                for c in range(self.board_size):
                    for dir, move in enumerate(
                        self.moves[1:3]
                    ):  # Only check down and right
                        if self.board[r, c, dir + 1]:
                            continue
                        pos_a = find((r, c))
                        pos_b = find((r + move[0], c + move[1]))
                        if pos_a != pos_b:
                            union(pos_a, pos_b)

            for r in range(self.board_size):
                for c in range(self.board_size):
                    find((r, c))
            my_r = find(tuple(self.myPosition)) # Was self.p0_pos in world.py. Replaced with myPos, check here if there's a bug later.
            adv_r = find(tuple(self.advPosition)) # Was self.p1_pos in world.py. Replaced with advPos, check here if there's a bug later.
            myScore = list(father.values()).count(my_r)
            advScore = list(father.values()).count(adv_r)
            if my_r == adv_r:
                return -1;
            if myScore > advScore:
                return 1;
            elif myScore < advScore:
                return 0;
            else:
                return 0.5;


class MCTSNode:
    def __init__(self):
        self.boardState = None;
        self.parent = None;
        self.visitCount = 0; 
        self.winCount = 0;
        self.childList = [];
        self.direction = None;

    def setParent(self, parent):
        self.parent = parent;

    def getParent(self):
        return self.parent;

    def hasParent(self):
        return self.parent != None;
    
    def setDirection(self, inputDirection):
        self.direction = inputDirection;

    def getDirection(self):
        return self.direction;

    def setState(self, inputState: BoardState):
        self.boardState = inputState;

    def getState(self):
        return self.boardState;
    
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

    def getVisitCount(self):
        return self.visitCount;

    def setVisitCount(self, newCount):
        self.visitCount = newCount;

    def incrementVisit(self):
        self.visitCount = self.visitCount + 1;

    def getWinCount(self):
        return self.winCount;

    def setWinCount(self, newScore):
        self.winCount = newScore;

    def addwinCount(self, scoreToAdd):
        self.winCount = self.winCount + scoreToAdd;

    #Returns true if this node is a leaf (i.e. it has an empty child list)
    def isLeaf(self):
        return (len(self.childList) == 0);

    def update(self, result):
        # Maybe revisit this later, but I think it's fine.
        self.visitCount += 1;
        self.winCount += result;

    def expandNode(self):
        # Get all possible states, and add them to this node's childList. *** This will likely be too expensive. Edit to be a subset of states (proportional to max_step).
        max_step = self.getState().getMaxStep();
        copy = deepcopy(self.getState());
        
        # Make an array with max_step slots which contain MCTSNode objects.
        # for max_step, make another boardstate copy, simulate a random move (twice) on it, and use it to create an MCTSNode which is then added to the array
        # Then, simply return the array.

        for i in range(max_step):
            # May be getting stuck because it's trying to do a random action when the game has already ended.
            direction = copy.simulateRandomAction();
            copy.simulateRandomAction(); #here.
            node = MCTSNode();
            node.setState(copy);
            node.setDirection(direction);
            self.addChildNode(node);
            copy = deepcopy(self.getState());
        
        return None;
        

class UCT:

    def findBestUCTNode(node: MCTSNode, totalRootVisits: int):
        # Foreach child in node.getChildArray, get the one with the highest UCTValue(parentVisitCount, childNode.getState().getwinCount(), childNode.getState().getVisitCount()) ***
        highest = None;
        highestVal = -1;
        for child in node.getChildren():
            if(highest == None):
                highest = child;
                highestVal = 9999;
            
            childVal = UCT.UCTValue(child.getVisitCount(), child.getWinCount(), totalRootVisits)
            if(childVal >= highestVal):
                highest = child;
                highestVal = childVal;

        return highest;

    # Should be (winScore / numberOfVisits) + C * sqrt(log(total root node visits) / numberOfVisits)
    def UCTValue(totalVisits, winCount, rootTotalVisits): 
        if(totalVisits == 0):
            return 9999; #Maybe double check if we can use INTEGER_MAXVAL or something instead, but this should work.
        return (winCount / totalVisits) + 1.41 * math.sqrt(math.log(rootTotalVisits) /  totalVisits) #The 'c' value (1.41) can and should be tuned later. ***

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
        timelimit = 1750; # Tried 2000ms (2s) but results came out 2.3s so this seems to be about as high as we can safely go.
        startTime = time.time() * 1000;
        #stateList = [];
        # *** Create a node based on the passed in state, make it the root of the tree
        rootNode = MCTSNode();
        initialState = BoardState(chess_board, tuple(my_pos), tuple(adv_pos), max_step, True);
        rootNode.setState(deepcopy(initialState));
        totalRootVisits = 0; #Maybe change to 1?
        curNode = rootNode;
        #result = self.randomSimulation(curNode.getState()); 
        #print(result);
    
        counter = 0
        #while((time.time() * 1000) < startTime + timelimit):
        while(counter < 100):
            #These two lines only here for speed/memory tests
            # copiedState = BoardState(chess_board, my_pos, adv_pos, max_step);
            # stateList.append(copiedState);

            ## Step 1: Select a promising node (should be the root at the start)
            while (not curNode.isLeaf()): # ***
                curNode = UCT.findBestUCTNode(curNode, totalRootVisits); # What if this returns 'None'? (not the problem)
            
            ## Step 2: Expand the node   
            curNode.expandNode();
            curNode = UCT.findBestUCTNode(curNode, totalRootVisits);

            ##Step 3: Simulate random game
            result = self.randomSimulation(deepcopy(curNode.getState())); #Will probably infinitely loop for now.
            ##Step 4: Backpropagation 
            while(curNode.hasParent()): # ***
              curNode.update(result)
              curNode = curNode.getParent()
              if(not curNode.hasParent()):
                  totalRootVisits += 1;
            counter += 1;

        
        print(tracemalloc.get_traced_memory());
        tracemalloc.stop();
        print((time.time() * 1000) - startTime);
        final_move_node = UCT.findBestUCTNode(rootNode, totalRootVisits); #Maybe just pick by visit count.
        # dummy return
        # return my_pos, self.dir_map["u"]
        return final_move_node.getState().getMyPos(), final_move_node.getDirection();
    
    def randomSimulation(self, state:BoardState):
        counter = 0;
        while(True):
            result = state.endCheck();
            #print("Result of endCheck is " + str(result));
            counter = counter + 1;
            #print(counter);
            if(result == -1):
                # print("simulating a move...");
                # This is not the end, need to do another random move.
                state.simulateRandomAction();
                continue;
            else:
                return result;


"""
CHECKLIST:
- Need function to get possible moves (node expansion) 

- Need a function to properly select a UCT node - DONE! (almost certainly needs testing though)
- Need a function to update a node's value (backpropagation) - DONE!
- Need a function to select a random move and play it on a state (as fast as possible!) - DONE!
- Need a function that will continually do random moves until the end (a random rollout/simulation) - DONE!
- Need a function to check that a state is terminal (can likely steal from world.py) - DONE!
- Need a function to evaluate a node's value given a state. - DONE! (review it tho)
- Need a function to check that a given state in the tree is a leaf - DONE!

MCTS:
- Need a way to do several random simulations
- Need a tree policy (UCT) and a leaf/default policy (Look-Ahead Tree, will likely be random)
  Q*(s,a,h) = E[R(s,a) + βV*(T(s,a),h-1)]
"""
