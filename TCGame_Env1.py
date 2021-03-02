from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product
import copy


class TicTacToe():

    def __init__(self):
        """initialise the board"""        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        out = False
        for count in range(3):
            row_list = [value for index,value in enumerate(curr_state) if index>=count*3 and index<3+count*3]
            out = out|True if sum(row_list)>=15 else out|False
        for count in range(3):
            col_list = [value for index,value in enumerate(curr_state) if index%3==count]
            out = out|True if sum(col_list)>=15 else out|False

        diagonal1_list = [value for index,value in enumerate(curr_state) if (index)%4==0]
        out = out|True if sum(diagonal1_list)>=15 else out|False

        diagonal2_list = [value for index,value in enumerate(curr_state) if index in [2,4,6]]
        out = out|True if sum(diagonal2_list)>=15 else out|False

    #     print(diagonal2_list)    
        return out
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'
        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'
        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)


    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        new_state = copy.deepcopy(curr_state)
        new_state[curr_action[0]] = curr_action[1]
        return new_state 


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""

        newState = self.state_transition(curr_state, curr_action)
        terminal = self.is_terminal(newState)
        if terminal[0]:
            if terminal[1] == 'Win':
                reward = 10
            else:
                reward = 0
            return (newState, reward, terminal[0])
        else:
            env_actions =  random.choice([i for i in self.action_space(newState)[1]])
            envnewState = self.state_transition(newState, env_actions)
            envterminal = self.is_terminal(envnewState)
            if envterminal[0]:
                if envterminal[1] == 'Win':
                    reward = -10
                else:
                    reward = 0
            else:
                reward = -1
            return (envnewState, reward, envterminal[0])

    
    def reset(self):
        return self.state
