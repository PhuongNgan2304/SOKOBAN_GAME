from cmath import sqrt
import numpy as np
import math
POS_PLAYER_MOVE = {"UP": [-1, 0], "DOWN": [1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}

def load_maze(path):
    a = np.loadtxt("./problem/"+path, dtype=str)
    return tuple(map(tuple, a))

def load_goal_state(path):
    a = np.loadtxt("./goal_state/"+path, dtype=str)
    if any(isinstance(t, np.ndarray) for t in a):
        return list(a)
    return [list(a)]

def get_box_position(state):
    list_position=list([])
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '*':
                list_position.append([str(i),str(j)])
    return list_position
def get_goal_nearest_box_dis(box_pos, goal_poses):
    min = 99999.0
    for (i, j) in goal_poses:
        dis = math.sqrt((int(box_pos[1]) - int(j))**2 + (int(box_pos[0]) - int(i)) ** 2)
        if dis < min:
            min = dis
    return min
def get_player_position(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 'x':
                return [str(i),str(j)]
    return None

def is_over_bound_maze(maze, pos):
    if pos[0] >= len(maze) or pos[0] < 0 or pos[1] >= len(maze[1]) or pos[1] < 0:
            return True
    return False
def is_more_box_collision(maze, pos, action):
    next_pos = (pos[0] + POS_PLAYER_MOVE[action][0], pos[1] + POS_PLAYER_MOVE[action][1])
    if is_over_bound_maze(maze, next_pos):
        return True
    if maze[next_pos[0]][next_pos[1]] == '*' and maze[pos[0]][pos[1]] == '*':
        return True
    return False

def is_wall_collision(maze, pos):
    if maze[pos[0]][pos[1]] == '1':
        return True
    return False

def is_box_wall_collision(maze, pos, action):
    next_pos = (pos[0] + POS_PLAYER_MOVE[action][0], pos[1] + POS_PLAYER_MOVE[action][1])
    if is_over_bound_maze(maze, next_pos):
        return True
    if maze[next_pos[0]][next_pos[1]] == '1' and maze[pos[0]][pos[1]] == '*':
        return True
    return False

def can_move(maze, pos, action):
    return not (is_over_bound_maze(maze, pos) or is_more_box_collision(maze, pos, action) or is_wall_collision(maze, pos) or is_box_wall_collision(maze, pos, action))

def get_value_contain_in_PrioQueue(node, frontier):
    for item in frontier.queue:
        if node.state == item.state:
            return item
    return False
class SokobanProblem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        player_pos = get_player_position(state)
        player_pos = [int(player_pos[0]), int(player_pos[1])]
        for act, pos in POS_PLAYER_MOVE.items():
            if not can_move(state, (player_pos[0] + pos[0], player_pos[1] + pos[1]), act):
                possible_actions.remove(act)
        return possible_actions

    def result(self, state, action):
        player_pos = get_player_position(state)
        player_pos = [int(player_pos[0]), int(player_pos[1])]
        new_state = list(map(list,state))
        next_player_pos = (player_pos[0] + POS_PLAYER_MOVE[action][0], player_pos[1] + POS_PLAYER_MOVE[action][1])
        if new_state[next_player_pos[0]][next_player_pos[1]] == '*':
            next_box_pos = (next_player_pos[0] + POS_PLAYER_MOVE[action][0], next_player_pos[1] + POS_PLAYER_MOVE[action][1])
            new_state[next_player_pos[0]][next_player_pos[1]], new_state[next_box_pos[0]][next_box_pos[1]] = new_state[next_box_pos[0]][next_box_pos[1]], new_state[next_player_pos[0]][next_player_pos[1]]
        
        new_state[next_player_pos[0]][next_player_pos[1]], new_state[player_pos[0]][player_pos[1]] = new_state[player_pos[0]][player_pos[1]], new_state[next_player_pos[0]][next_player_pos[1]]

        if new_state[player_pos[0]][player_pos[1]] == 'g':
            new_state[player_pos[0]][player_pos[1]] = '0'

        for g in self.goal:
            if new_state[int(g[0])][int(g[1])] == '0':
                new_state[int(g[0])][int(g[1])] = 'g'

        return tuple(map(tuple,new_state))

    def goal_test(self, state):
        count = 0
        index = 0
        list_position = get_box_position(state)
        for i in list_position:
            if i[0] == self.goal[index][0] and i[1] == self.goal[index][1]:
                count +=1
            index += 1
        if count == len(self.goal):
            return True
        return False

    def path_cost(self, c, state1, action, state2):
        return c + 1     



