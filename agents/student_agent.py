# Student agent: Add your own agent here
# AlphaCS
from agents.agent import Agent
from store import register_agent

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
        # dummy return
        return my_pos, self.dir_map["u"]




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
