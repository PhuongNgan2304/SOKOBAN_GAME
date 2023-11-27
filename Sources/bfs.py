# import support_function as spf
# import time
# import psutil
# import os
# from copy import deepcopy

# TIME_OUT = 1800

# '''
# //========================//
# //           BFS          //
# //        ALGORITHM       //
# //     IMPLEMENTATION     //
# //========================//
# '''


# # DỮ LIỆU ĐỂ LƯU TRẠNG THÁI CHO MỖI BƯỚC

# class state:
#     def __init__(self, board, state_parent, list_check_point):
#         '''lưu trạng thái hiện tại và trạng thái cha của trạng thái này'''
#         self.board = board
#         self.state_parent = state_parent
#         self.cost = 1
#         self.heuristic = 0
#         self.check_points = deepcopy(list_check_point)
#     '''HÀM ĐỆ QUY ĐỂ TRUY VẾT ĐẾN TRẠNG THÁI ĐẦU TIÊN NẾU TRẠNG THÁI HIỆN TẠI LÀ MỤC TIÊU'''
#     def get_line(self):
#         '''sử dụng vòng lặp để tìm danh sách trạng thái từ đầu đến trạng thái hiện tại'''
#         if self.state_parent is None:
#             return [self.board]
#         return (self.state_parent).get_line() + [self.board]
#     '''TÍNH HÀM HEURISTIC ĐƯỢC SỬ DỤNG CHO GIẢI THUẬT A*'''
#     def compute_heuristic(self):
#         list_boxes = find_boxes_position(self.board)
#         if self.heuristic == 0:
#             self.heuristic = self.cost + abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0] - self.check_points[i][1] for i in range(len(list_boxes))))
           
#         return self.heuristic
#     '''NẠP TOÁN TỬ CHO PHÉP LƯU TRẠNG THÁI TRONG HÀNG ĐỢI ƯU TIÊN'''
#     def __gt__(self, other):
#         if self.compute_heuristic() > other.compute_heuristic():
#             return True
#         else:
#             return False
#     def __lt__(self, other):
#         if self.compute_heuristic() < other.compute_heuristic():
#             return True
#         else :
#             return False


# def BFS_search(board, list_check_point):
#     start_time = time.time()
    
#     ''' GIẢI PHÁP TÌM KIẾM BFS '''
    
#     ''' NẾU BẮT ĐẦU LÀ TRẠNG THÁI KẾT THÚC HOẶC KHÔNG CÓ ĐIỂM KIỂM TRA '''
#     if spf.check_win(board, list_check_point):
#         print("Found Win")
#         return [board]
    
#     ''' KHỞI TẠO TRẠNG THÁI BẮT ĐẦU '''
#     start_state = state(board, None, list_check_point)
    
#     ''' KHỞI TẠO 2 DANH SÁCH ĐƯỢC SỬ DỤNG CHO TÌM KIẾM BFS '''
#     list_state = [start_state]
#     list_visit = [start_state]
    
#     ''' LẶP QUA DANH SÁCH ĐÃ DUỢC DUYỆT '''
#     while len(list_visit) != 0:
        
#         ''' LẤY TRẠNG THÁI HIỆN TẠI ĐỂ TÌM KIẾM '''
#         now_state = list_visit.pop(0)
        
#         ''' LẤY VỊ TRÍ HIỆN TẠI CỦA NGƯỜI CHƠI '''
#         cur_pos = spf.find_position_player(now_state.board)
        
#         ''' LẤY DANH SÁCH VỊ TRÍ MÀ NGƯỜI CHƠI CÓ THỂ DI CHUYỂN ĐẾN '''
#         list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        
#         ''' TẠO TRẠNG THÁI MỚI TỪ DANH SÁCH CÓ THỂ DI CHUYỂN '''
#         for next_pos in list_can_move:
            
#             ''' TẠO BẢNG MỚI '''
#             new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            
#             ''' NẾU BẢNG NÀY CHƯA TỒN TẠI TRONG DANH SÁCH TRẠNG THÁI THÌ BỎ QUA TRẠNG THÁI NÀY '''
#             if spf.is_board_exist(new_board, list_state):
#                 continue
            
#             ''' NẾU MỘT HOẶC NHIỀU HỘP BỊ KẸT TRONG GÓC THÌ BỎ QUA TRẠNG THÁI NÀY '''
#             if spf.is_board_can_not_win(new_board, list_check_point):
#                 continue
            
#             ''' NẾU TẤT CẢ HỘP BỊ KẸT THÌ BỎ QUA TRẠNG THÁI NÀY '''
#             if spf.is_all_boxes_stuck(new_board, list_check_point):
#                 continue
            
#             ''' TẠO TRẠNG THÁI MỚI '''
#             new_state = state(new_board, now_state, list_check_point)
            
#             ''' KIỂM TRA XEM TRẠNG THÁI MỚI CÓ PHẢI LÀ TRẠNG THÁI KẾT THÚC KHÔNG '''
#             if spf.check_win(new_board, list_check_point):
#                 print("\nBreadth First Search")
#                 print("Found Win")
#                 print("  Số trạng thái đã duyệt : {} ".format(len(list_state)))
#                 process = psutil.Process(os.getpid())
#                 memory_usage = process.memory_info().rss / (1024**2)
#                 print(f"  Bộ nhớ: {memory_usage} Mb")
#                 return (new_state.get_line(), len(list_state))
            
#             ''' THÊM TRẠNG THÁI MỚI VÀO DANH SÁCH ĐÃ DUYỆT VÀ DANH SÁCH TRẠNG THÁI CẦN DUYỆT '''
#             list_state.append(new_state)
#             list_visit.append(new_state)
#             process = psutil.Process(os.getpid())
#             memory_usage = process.memory_info().rss / (1024**2)
            
#             ''' TÍNH THỜI GIAN TIMEOUT '''
#             end_time = time.time()
#             if end_time - start_time > TIME_OUT:
#                 return []
        
#         end_time = time.time()
#         if end_time - start_time > TIME_OUT:
#             return []
    
#     ''' KHÔNG TÌM THẤY GIẢI PHÁP '''
#     print("Not Found")
#     return []

import numpy as np
from collections import deque

class State:
    def __init__(self, board, parent, checkpoints):
        self.board = board
        self.parent = parent
        self.checkpoints = checkpoints

def check_win(board, checkpoints):
    return np.all(board[tuple(zip(*checkpoints))] == '$')

def find_position_player(board):
    pos = np.where(board == '@')
    if len(pos[0]) > 0:
        return pos[0][0], pos[1][0]
    return -1, -1

def get_next_positions(current_state):
    player_pos = find_position_player(current_state.board)
    possible_moves = []

    for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_pos = (player_pos[0] + move[0], player_pos[1] + move[1])
        if 0 <= next_pos[0] < current_state.board.shape[0] and 0 <= next_pos[1] < current_state.board.shape[1]:
            possible_moves.append(next_pos)

    return possible_moves

def move(board, next_pos, player_pos, checkpoints):
    new_board = board.copy()
    new_player_pos = tuple(next_pos)
    box_pos = player_pos

    if board[next_pos] == '$':
        box_pos = (2 * next_pos[0] - player_pos[0], 2 * next_pos[1] - player_pos[1])

    new_board[player_pos] = ' '
    new_board[new_player_pos] = '@'

    if board[box_pos] == '$':
        new_board[box_pos] = ' '
        new_board[2 * next_pos[0] - player_pos[0], 2 * next_pos[1] - player_pos[1]] = '$'

    return new_board

def BFS_search(board, checkpoints):
    start_state = State(board, None, checkpoints)
    queue = deque([start_state])
    visited = set()

    while queue:
        current_state = queue.popleft()

        if check_win(current_state.board, current_state.checkpoints):
            return get_solution_path(current_state)

        visited.add(tuple(map(tuple, current_state.board)))

        for next_pos in get_next_positions(current_state):
            new_board = move(current_state.board, next_pos, find_position_player(current_state.board), current_state.checkpoints)
            new_state = State(new_board, current_state, current_state.checkpoints)

            if tuple(map(tuple, new_board)) not in visited:
                queue.append(new_state)
                visited.add(tuple(map(tuple, new_board)))

    return []

def get_solution_path(final_state):
    path = [final_state.board]
    while final_state.parent:
        final_state = final_state.parent
        path.insert(0, final_state.board)
    return path

