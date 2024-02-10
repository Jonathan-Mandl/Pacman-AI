import search
import math
import utils

id = "211399175"

""" Rules """
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50
PACMAN = 77


def tuple_to_list(state_tuple):
    return [list(row) for row in state_tuple]


def list_to_tuple(state_list):
    return tuple(tuple(row) for row in state_list)


def search_ghost(ghost_code, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == ghost_code * 10:
                return i, j
            if matrix[i][j] == ghost_code * 10 + 1:
                return i, j
    return None


def search_element(symbol, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == symbol:
                return i, j
    return None


def move_pacman(matrix, locations, action):
    """This function moves pacman. returns True if pacman moved. returns False if pacman was not able to move or was
    caught by a ghost"""

    rows = len(matrix) - 1
    columns = len(matrix[0]) - 1

    y, x = locations[7]  # pacman location

    # map actions to coordinate changes
    action_mapping = {"R": (0, 1), "L": (0, -1), "D": (1, 0), "U": (-1, 0)}

    # change in x and y coordinates
    dy, dx = action_mapping.get(action, (0, 0))

    # check is pacman will hit a wall or exits the board
    if not (0 <= y + dy <= rows) or not (0 <= x + dx <= columns) or matrix[y + dy][x + dx] == 99:
        return False

    matrix[y][x] = 10  # update previous location to empty cell

    if matrix[y + dy][x + dx] in [10, 11]:  # if new location does not contain ghost
        matrix[y + dy][x + dx] = 77  # update new location
    else:  # ghost caught pacman
        matrix[y + dy][x + dx] = 88
        return False

    locations[7] = (y + dy, x + dx)  # update pacman location

    return True


def move_ghost_direction(matrix, ghost_code, locations, direction):
    y1, x1 = locations[ghost_code]  # ghost location

    action_mapping = {"R": (0, 1), "L": (0, -1), "D": (1, 0), "U": (-1, 0)}

    dy, dx = action_mapping.get(direction, (0, 0))  # coordinate difference

    # new location
    y2, x2 = y1 + dy, x1 + dx

    # update new location
    if matrix[y2][x2] == 11:  # if contain coin
        matrix[y2][x2] = ghost_code * 10 + 1
    elif matrix[y2][x2] == 77:  # if contains pacman
        matrix[y2][x2] = 88  # ghost caught pacman
    else:  # if empty cell
        matrix[y2][x2] = ghost_code * 10

    # check if previous location contains coin based on ghost symbol and update it
    if matrix[y1][x1] == ghost_code * 10 + 1:
        matrix[y1][x1] = 11  # previous location still contains coin
    else:
        matrix[y1][x1] = 10  # previous location becomes  an empty cell

    locations[ghost_code] = (y2, x2)  # update locations dictionary


def move_ghost(matrix, ghost_code, locations):
    rows = len(matrix) - 1
    columns = len(matrix[0]) - 1

    yp, xp = locations[7]  ## pacman location
    yg, xg = locations[ghost_code]  # ghost location

    # calculate Manhattan distance for moving in each possible direction
    left_distance = abs(xg - 1 - xp) + abs(yg - yp)
    right_distance = abs(xg + 1 - xp) + abs(yg - yp)
    up_distance = abs(xg - xp) + abs(yg - 1 - yp)
    down_distance = abs(xg - xp) + abs(yg + 1 - yp)

    # list of directions and their manhattan distance
    move_directions = [("L", left_distance), ("R", right_distance), ("U", up_distance), ("D", down_distance)]

    # Sort the possible directions list based Manhattan distance first and then based priority: right, down, left, up
    move_directions = sorted(move_directions, key=lambda x: (x[1], "RDLU".index(x[0])))

    action_mapping = {"R": (0, 1), "L": (0, -1), "D": (1, 0), "U": (-1, 0)}

    # try moving in every possible direction based on sorted order
    for direction in move_directions:

        direction = direction[0]

        dy, dx = action_mapping.get(direction, (0, 0))

        # check ghost wont hit a wall or another ghost
        if 0 <= yg + dy <= rows and 0 <= xg + dx <= columns and matrix[yg + dy][xg + dx] in [10, 11, 77]:
            move_ghost_direction(matrix, ghost_code, locations, direction)
            break


class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""

    def __init__(self, initial):
        """ Magic numbers for ghosts and Packman:
        2 - blue, 3 - yellow, 4 - green, 5 - red and 7 - Packman."""

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def successor(self, state):
        """ Generates the successor state """
        # if state contains 88 do not return successors
        if search_element(88, state) is not None:
            return None

        successors = []

        for action in ["R", "D", "L", "U"]:

            new_state = self.result(state, action)

            if new_state is None:
                continue

            successors.append((action, new_state))

        return successors

    def result(self, state, move):
        """given state and an action and return a new state"""
        matrix = tuple_to_list(state)  # convert state to 2d array temporarily

        # search pacman location
        self.locations[7] = search_element(77, matrix)

        # search for ghost location
        self.locations[2] = search_ghost(2, matrix)
        self.locations[3] = search_ghost(3, matrix)
        self.locations[4] = search_ghost(4, matrix)
        self.locations[5] = search_ghost(5, matrix)

        # if pacman could not move  or was caught by ghost do not return state
        if not move_pacman(matrix, self.locations, move):
            return None

        # move ghosts in the specified order
        if self.locations[2] is not None:
            move_ghost(matrix, 2, self.locations)
        if self.locations[3] is not None:
            move_ghost(matrix, 3, self.locations)
        if self.locations[4] is not None:
            move_ghost(matrix, 4, self.locations)
        if self.locations[5] is not None:
            move_ghost(matrix, 5, self.locations)

        # if ghost caught pacman do no return state
        if search_element(88, matrix) is not None:
            return None

        new_state = list_to_tuple(matrix)

        return new_state

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""

        coin_count = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] % 10 == 1:  # check if cell contains coin
                    coin_count += 1

        if coin_count == 0:  # if there are no coins return true - goal state
            return True
        else:
            return False

    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        state = node.state
        y, x = search_element(77, state)
        min_distance = 0
        coin_count = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                # check if cell contains coin
                if state[i][j] % 10 == 1:
                    coin_count += 1
                    distance = abs(y - i) + abs(x - j)
                    if distance < min_distance:
                        min_distance = distance

        # coin count is the heuristic function
        return coin_count + min_distance


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()
create_pacman_problem(game)
