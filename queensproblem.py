
import random as rand
import GUI as g
class Algorithm:
    
    @property
    def state(self):
        return self._state

    @property
    def cost(self):
        return len(attacking_queens(self.state))

    @property
    def step(self):
        return self._step

    @state.setter
    def state(self, state):
        self._state = state

    def __init__(self):
        self._state = []
        self._step = 0

    def initial_state(self, n=8):
        self._state = [-1] * n
        self._step = 0

        for column in range(0, n):
            self._state[column] = rand.randint(0, n - 1)

    def next_states_cost(self):
        return next_states_cost(self.state)

    def move_next(self):
        self._step += 1
        
def next_states(state=[]):
    successors = []
    n = len(state)

    for column in range(0, n):
        for row in range(0, n):
            if state[column] != row:
                successor = state.copy()
                successor[column] = row
                successors.append(successor)

    return successors


def attacking_queens(state=[]):
    pairs = set()

    for index_1, value_1 in enumerate(state):
        for index_2, value_2 in enumerate(state):
            if index_1 == index_2 or index_1 > index_2:
                continue
            elif value_1 == value_2:  # check rows
                pairs.add(((index_1, value_1), (index_2, value_2)))
            elif abs(index_1 - index_2) == abs(value_1 - value_2):  # check diagonal
                pairs.add(((index_1, value_1), (index_2, value_2)))

    return pairs


def next_states_cost(state=[]):
    n = len(state)
    result = [[-1 for c in range(0, n)] for r in range(0, n)]

    for column in range(0, n):
        for row in range(0, n):
            if state[column] != row:
                successor = state.copy()
                successor[column] = row
                result[row][column] = len(attacking_queens(successor))

    return result

#######If no next state cost less than the current state cost make it select randomly any state to take:#######
            
class HillClimbing(Algorithm):
    def move_next(self):
        super().move_next()
        state_cost = self.cost

        next_states_list = next_states(self.state)
        better_states = []

        for next_state in next_states_list:
            next_state_cost = len(attacking_queens(next_state))
            
            if next_state_cost < state_cost:
                self.state = next_state
                better_states.append(next_state)
                break     

        if len(better_states) > 0:
            self.state = rand.choice(better_states)
        else:
            self.state = rand.choice(next_states_list)
              

class StochasticHillClimbing(Algorithm):
    def move_next(self):
        super().move_next()
        state_cost = self.cost
        next_state_candidates = []

        next_states_list = next_states(self.state)

        for next_state in next_states_list:
            next_state_cost = len(attacking_queens(next_state))

            if next_state_cost < state_cost:
                next_state_candidates.append(next_state)

        if len(next_state_candidates) > 0:
            self.state = rand.choice(next_state_candidates)
        else:
            self.state = rand.choice(next_states_list)
            

class BestFirstSearch(Algorithm):
    def move_next(self):
        super().move_next()

        next_states_list = next_states(self.state)

        evaluated_states = [(state, len(attacking_queens(state))) for state in next_states_list]

        sorted_states = sorted(evaluated_states, key=lambda x: x[1])

        best_state, _ = sorted_states[0]

        if len(sorted_states) > 1:
            best_cost = sorted_states[0][1]
            best_states = [state for state, cost in sorted_states if cost == best_cost]
            best_state = rand.choice(best_states)

        self.state = best_state


            
class BeamSearch(Algorithm):

    def __init__(self, k=1):
        super().__init__()
        self._k_states = []
        self._k = k

    @staticmethod
    def select_best_states(states, k=1):
        candidates = []

        for state in states:
            state_cost = len(attacking_queens(state))
            candidates.append([state, state_cost])

        return [x[0] for x in sorted(candidates, key=lambda x: x[1])[:k]]

    @staticmethod
    def get_random_following_states(state, k=1):
        next_states_list = next_states(state)
        return [rand.choice(next_states_list) for _ in range(k)]

    def move_next(self):
        super().move_next()

        if not self._k_states:
            self._k_states = BeamSearch.get_random_following_states(self.state, self._k)

        next_state_candidates = []
        for state in self._k_states:
            next_state_candidates += next_states(state)

        if len(next_state_candidates) == 0:
            return

        self._k_states = BeamSearch.select_best_states(next_state_candidates, self._k)

        if len(self._k_states) == 0:
            self.state = rand.choice(next_state_candidates)
        else:
            self.state = BeamSearch.select_best_states(self._k_states)[0]
   
class Monitor:
    def __init__(self, gui):
        self._gui = gui
        self._gui.restart_action = self.init_board
        self._gui.move_action = self.next_board
        self._gui.selection_action= self.change_selection
        self.change_selection("Hill-Climbing")

    def start(self):
        self._gui.show()

    def change_selection(self, selection):
        if selection == "Hill-Climbing":
            self._algorithm = HillClimbing()
        elif selection == "Stochastic Hill-Climbing":
            self._algorithm = StochasticHillClimbing()  
        elif selection == "Greedy Best First Search":
            self._algorithm = BestFirstSearch() 
        elif selection == "Beam Search (beam width=4)":
            self._algorithm = BeamSearch(4)

        self._algorithm.initial_state()
        self.draw()

    def next_board(self):
        self._algorithm.move_next()
        self.draw()

    def init_board(self):
        self._algorithm.initial_state()
        self.draw()

    def draw(self):
        self._gui.draw_board()
        self._gui.cost = self._algorithm.cost
        self._gui.step = self._algorithm.step

        for column, row in enumerate(self._algorithm.state):
            self._gui.draw_position(column, row)

        for row_index, row in enumerate(self._algorithm.next_states_cost()):
            for column_index, value in enumerate(row):
                if value >= 0:
                    self._gui.draw_value(column_index, row_index, value)
   
gui = g.GUI()
monitor = Monitor(gui)

monitor.start()

