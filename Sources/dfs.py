import support_function as spf
import time
import psutil
import os
from copy import deepcopy

TIME_OUT = 1800

'''
//========================//
//           DFS          //
//        ALGORITHM       //
//     IMPLEMENTATION     //
//========================//
'''


# DỮ LIỆU ĐỂ LƯU TRẠNG THÁI CHO MỖI BƯỚC

class state:
    def __init__(self, board, state_parent, list_check_point):
        '''lưu trạng thái hiện tại và trạng thái cha của trạng thái này'''
        self.board = board
        self.state_parent = state_parent
        self.check_points = deepcopy(list_check_point)
    '''HÀM ĐỆ QUY ĐỂ TRUY VẾT ĐẾN TRẠNG THÁI ĐẦU TIÊN NẾU TRẠNG THÁI HIỆN TẠI LÀ MỤC TIÊU'''
    def get_line(self):
        '''sử dụng vòng lặp để tìm danh sách trạng thái từ đầu đến trạng thái hiện tại'''
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]



def DFS_search(board, list_check_point):
   start_time = time.time()
   
   if spf.check_win(board, list_check_point):
       print("Found Win")
       return [board]
   
   start_state = state(board, None, list_check_point)
   
   list_state = [start_state]
   list_visit = [start_state]
   while len(list_visit) != 0:
       now_state = list_visit.pop()
       cur_pos = spf.find_position_player(now_state.board)
       list_can_move = spf.get_next_pos(now_state.board, cur_pos)
       for next_pos in list_can_move:
           new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
           if spf.is_board_exist(new_board, list_state):
               continue
           
           if spf.is_board_can_not_win(new_board, list_check_point):
               continue
           
           if spf.is_all_boxes_stuck(new_board, list_check_point):
               continue
           
           new_state = state(new_board, now_state, list_check_point)
           
           if spf.check_win(new_board, list_check_point):
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024**2)
                result = spf.Result()
                result.approved_states = len(list_state)
                result.memory = memory_usage
                result.time = time.time()
                result.list_board = (new_state.get_line(), len(list_state))
                result.algorithmName = "Depth First Search"
                return result
           
           
           list_state.append(new_state)
           list_visit.append(new_state)
           process = psutil.Process(os.getpid())
           memory_usage = process.memory_info().rss / (1024**2)
           
           end_time = time.time()
           if end_time - start_time > TIME_OUT:
               return []
       
       end_time = time.time()
       if end_time - start_time > TIME_OUT:
           return []
   
   print("Not Found")
   return []


# import numpy as np

# class State:
#     def __init__(self, board, parent, checkpoints):
#         self.board = board
#         self.parent = parent
#         self.checkpoints = checkpoints

# def check_win(board, checkpoints):
#     return np.all(board[tuple(zip(*checkpoints))] == '$')

# def find_position_player(board):
#     pos = np.where(board == '@')
#     if len(pos[0]) > 0:
#         return pos[0][0], pos[1][0]
#     return -1, -1

# def get_next_positions(current_state):
#     player_pos = find_position_player(current_state.board)
#     possible_moves = []

#     for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#         next_pos = (player_pos[0] + move[0], player_pos[1] + move[1])
#         if 0 <= next_pos[0] < current_state.board.shape[0] and 0 <= next_pos[1] < current_state.board.shape[1]:
#             possible_moves.append(next_pos)

#     return possible_moves

# def move(board, next_pos, player_pos, checkpoints):
#     new_board = board.copy()
#     new_player_pos = tuple(next_pos)
#     box_pos = player_pos

#     if board[next_pos] == '$':
#         box_pos = (2 * next_pos[0] - player_pos[0], 2 * next_pos[1] - player_pos[1])

#     new_board[player_pos] = ' '
#     new_board[new_player_pos] = '@'

#     if board[box_pos] == '$':
#         new_board[box_pos] = ' '
#         new_board[2 * next_pos[0] - player_pos[0], 2 * next_pos[1] - player_pos[1]] = '$'

#     return new_board

# def DFS_search(board, checkpoints):
#     start_state = State(board, None, checkpoints)
#     stack = [start_state]
#     visited = set()

#     count = 0 
#     while stack:
#         count = count +1 
#         print(count)
#         current_state = stack.pop()

#         if check_win(current_state.board, current_state.checkpoints):
#             return get_solution_path(current_state)

#         visited.add(tuple(map(tuple, current_state.board)))

#         for next_pos in get_next_positions(current_state):
#             new_board = move(current_state.board, next_pos, find_position_player(current_state.board), current_state.checkpoints)
#             new_state = State(new_board, current_state, current_state.checkpoints)

#             if tuple(map(tuple, new_board)) not in visited:
#                 stack.append(new_state)
#                 visited.add(tuple(map(tuple, new_board)))

#     return []

# def get_solution_path(final_state):
#     path = [final_state.board]
#     while final_state.parent:
#         final_state = final_state.parent
#         path.insert(0, final_state.board)
#     return path
