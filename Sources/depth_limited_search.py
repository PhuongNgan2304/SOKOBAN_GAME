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

class state:
    def __init__(self, board, state_parent, list_check_point):
        '''lưu trạng thái hiện tại và trạng thái cha của trạng thái này'''
        self.board = board
        self.state_parent = state_parent
        self.check_points = deepcopy(list_check_point)

    def get_line(self):
        '''sử dụng vòng lặp để tìm danh sách trạng thái từ đầu đến trạng thái hiện tại'''
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]

def DLS_Search(board, list_check_point, max_depth):
    start_time = time.time()
    result = spf.Result()
    
    if spf.check_win(board, list_check_point):
        print("Found Win")
        return [board]

    ''' KHỞI TẠO TRẠNG THÁI BẮT ĐẦU '''
    start_state = state(board, None, list_check_point)

    ''' KHỞI TẠO STACK VÀ SET ĐỂ THEO DÕI TRẠNG THÁI ĐÃ DUYỆT '''
    stack = [(start_state, 0)]
    visited = set()
    visited.add(tuple(map(tuple, board)))

    ''' THỰC HIỆN DLS '''
    while stack:
        current_state, depth = stack.pop()
        cur_pos = spf.find_position_player(current_state.board)
        list_can_move = spf.get_next_pos(current_state.board, cur_pos)

        ''' TẠO TRẠNG THÁI MỚI TỪ DANH SÁCH CÓ THỂ DI CHUYỂN '''
        for next_pos in list_can_move:
            new_board = spf.move(current_state.board, next_pos, cur_pos, list_check_point)
            board_tuple = tuple(map(tuple, new_board))

            if board_tuple in visited or depth >= max_depth:
                continue

            if spf.is_board_can_not_win(new_board, list_check_point):
                continue

            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = state(new_board, current_state, list_check_point)

            if spf.check_win(new_board, list_check_point):
                print("\nDepth-Limited Search")
                print("Found Win")
                print("  Số trạng thái đã duyệt : {} ".format(len(visited)))
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024 ** 2)

                result.approved_states = len(visited)
                result.memory = memory_usage
                result.time = time.time()
                result.list_board = (new_state.get_line(), len(visited))
                result.algorithmName = "Depth Limited Search"

                return result

            visited.add(board_tuple)
            stack.append((new_state, depth + 1))

            ''' TÍNH THỜI GIAN TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > TIME_OUT:
                return result

    ''' KHÔNG TÌM THẤY GIẢI PHÁP '''
    print("Not Found")
    return result
