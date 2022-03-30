# Student agent: Add your own agent here
# AlphaCS
from agents.agent import Agent
from store import register_agent
import math;

import sys


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

    def step(self, chess_board, my_pos, adv_pos, max_step):
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

        # dummy return
        return my_pos, self.dir_map["u"]

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
            # Get a random child from the list ***
            return None;

        def getMaxScoreChild(self):
            # Get the child with the highest 'visitCount' (I think. Review and get max number according to tree policy) ***
            return None;

    class MCTSTree:
        def __init__(self):
            self.root = None;
    
        def setRoot(self, node):
            self.root = node;

        def getRoot(self):
            return self.root;

        def addChild(self, parentNode: MCTSNode, childNode: MCTSNode):
            parentNode.addChildNode(childNode);
    
    class State:
        
        def __init__(self, boardState):
            self.boardState = boardState
            self.visitCount = 0;
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
            # Get all possible moves, and return them in a list of States ***
            return None;

        def randomMove(self):
            # Uses BoardState to figure out a random move.
            return None;

    class UCT:
        def findBestUCTNode(node):
            parentVisitCount = node.getState().visitCount();
            # Foreach child in node.getChildArray, get the one with the highest UCTValue(parentVisitCount, childNode.getState().getWinScore(), childNode.getState().getVisitCount()) ***
            return None;

        def UCTValue(totalVisits, winScore, visitCountNode): #Double check in general ***
            if(visitCountNode == 0):
                return 9999; #Maybe double check if we can use INTEGER_MAXVAL or something instead.
            return (winScore / visitCountNode) + 1.41 * math.sqrt(math.log(totalVisits) /  visitCountNode) #Check that this isnt integer division - would cause unpredictable behavior. ***

        

        


           

        




# ==== GENERAL ====
# - Has a time limit - can't run for too long, so "pure" Minimax is likely unusable.
# - Should first figure out what the branching factor (b), max tree depth (m) , etc... are.

# From slide 67, L8:
# - Design compact state representation.
# - Search using iterative deepening for real-time play.
# - Decide where to spend the computation effort.
# - Consider suboptimal opponents.

# ==== ALGORITHM OPTIONS ====
# Two main algorithms seen in class which seem applicable here: Alpha-Beta pruning Minimax, and MCTS. 

# - For AB-Minimax, could couple it with one of the 'tricks' described in class. Use cutoff tests depending on depth limits along with an evaluation function for nodes where we cut the search ('learning' AI?)
#   (Though this may not be that effective, since AB-pruning is an attempt at a solution to this. Make up a combo?)
#   Would also need to come up with the best 'ordering' of the AB-pruning-Minimax-tree to get the most out of it.
#   Look also into 'forward pruning' which was barely covered in class.

# - For MCTS, apparently helps if there is nondeterminism (does not apply) or if we don't know the game well enough to design eval functions. Uses random simulations to help determine what move to select.
#   MCTS is made better if we have a way to look at more promising nodes like AB-Minimax, but these eval functionas can depend on observed outcomes of simulations. In the infinite limit, converges to minimax.
#   The search develops in a selective, best-first manner ; expanding promising regions deeply. Policy given to do this most effectively, but can be tuned (UCT). Can also try our hand at "RAVE" where we share
#   knowledge among related nodes, but this was barely covered and seems quite complex.


# ==== OTHER ====
# - Game is deterministic, and fully observable.
# - It is a Zero-sum game
# - Most students will probably do Minimax, which means they will be optimal against ours if ours is also optimal (winner would be decided by who starts). Include some degree of random or suboptimal moves to trip them up?

# - If a player has 3 barriers around them and is within range, the move to 'box them in' should always be taken.
# - Amount of possible movements is from 0 to 1 + (sum of 1 to K(4i)) Then we potentially have 4 directions to place a barrier each, so branching factor is up to 4 * (1 + sum-of-1-to-K(4i)). M is limited between 4 and 10,
#   and K = floor((M + 1) / 2)! This does not take into account the K * 2 random barriers, or cases where a player is in a space within range of another player.
# - Players are on a random area of the board, but symmetrically. There may be special strategies/moves when players are within range of each other.
# - Disatvantage with starting first (according to the project description)
# - Be careful of random walks!
# - They give us 30 seconds to load data from files. Seems to imply either we should keep a collection of good start-of-game moves (MCTS learning, I think?) or spend a lot of time in calculations at the start.

# - "HumanAgent" and "RandomAgent" have useful validity-checking features (like the check_valid_input functions)

# - Eval: Try to go as close to adversary as possible, then put barrier towards them. If a barrier towards them exists, put it opposite instead. -> Works some of the time, flawed in the case where an agent is in
#   a smaller 'chunk', in which case they box themselves in. May need a way to detect that we're in such a 'chunk' (eg. a group of blocks where there are only 3 or less exits). May also want case where there is only
#   one thing left to block to end the game.
# - If in some kind of 'danger area', should prioritize escaping it over attempting to place a barrier right beside the adversary.
# - So, maybe first only consider moves bringing you closer to the opponent, if out of reach of the opponent?
# - Need a verification that a player doesn't block the other player into a "chunk" of greater value than the one they're in!


"""

Both:

- Figure out potential moves
- Figure out how to respect time/memory constraints

AB-Minimax:
- AB part and main algorithm loop pseudocode already exists
- DFS can be used to reduce space complexity (apparently)
- Make an eval function

MCTS:
- Need a way to do several random simulations
- Need a tree policy and a leaf/default policy (Look-Ahead Tree)
  Q*(s,a,h) = E[R(s,a) + βV*(T(s,a),h-1)]

"""
