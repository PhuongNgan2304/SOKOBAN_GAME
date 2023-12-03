#import heapq
import support_function as spf
from copy import deepcopy
import time
from queue import PriorityQueue
import psutil
import os
import math

'''
//=========================================//
//     GIẢI THUẬT BEST FIRST SEARCH*      //
//            IMPLEMENTATION             //
//======================================//
'''

class state:
    def __init__(self, board, state_parent, list_check_point):
        self.board = board
        self.state_parent = state_parent
        self.heuristic = 0 #h(n), không cộng g(n)
        self.check_points = deepcopy(list_check_point)
    
    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]

    def compute_euclidean_heuristic_for_best_first_search(self):
        list_boxes = spf.find_boxes_position(self.board)
        if self.heuristic == 0:
            total_distance = 0
            for i in range(len(list_boxes)):
                box = list_boxes[i]
                checkpoint = self.check_points[i]
                distance = math.sqrt((box[0] - checkpoint[0])**2 + (box[1] - checkpoint[1])**2)
                total_distance += distance
            self.heuristic = total_distance
        return self.heuristic

    def __gt__(self, other):
        if self.compute_euclidean_heuristic_for_best_first_search() > other.compute_euclidean_heuristic_for_best_first_search():
            return True
        else:
            return False

    def __lt__(self, other):
        if self.compute_euclidean_heuristic_for_best_first_search() < other.compute_euclidean_heuristic_for_best_first_search():
            return True
        else:
            return False

def Best_First_Search(board, list_check_point):
    start_time = time.time()
    result = spf.Result()

    if spf.check_win(board, list_check_point):
        print("Found Win")
        return [board]

    start_state = state(board, None, list_check_point)
    list_state = {tuple(map(tuple, board))}

    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)

    while not heuristic_queue.empty():
        now_state = heuristic_queue.get()
        cur_pos = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)

            if tuple(map(tuple, new_board)) in list_state:
                continue

            if spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = state(new_board, now_state, list_check_point)

            if spf.check_win(new_board, list_check_point):
                print("\nGreedy Best First Search")
                print("Found Win")
                print("  Số trạng thái đã duyệt : {} ".format(len(list_state)))
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024**2)

                result = spf.Result()
                result.approved_states = len(list_state)
                result.memory = memory_usage
                result.time = time.time()
                result.list_board = (new_state.get_line(), len(list_state))
                result.algorithmName = "Greedy Best First Search"

                return result

            list_state.add(tuple(map(tuple, new_board)))
            heuristic_queue.put(new_state)

            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / (1024**2)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return result

        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return result

    print("Not Found")
    return result

# ''' KHỞI TẠO TRẠNG THÁI BẮT ĐẦU '''
# start_state = state(board, None, list_check_point)
# open_list = []
# heapq.heappush(open_list, start_state)

# ''' LẶP QUA HÀNG ĐỢI ƯU TIÊN '''
# while open_list:
    
#     '''LẤY TRẠNG THÁI HIỆN TẠI ĐỂ TÌM KIẾM'''
#     now_state = heapq.heappop(open_list)
    
#     '''LẤY VỊ TRÍ HIỆN TẠI CỦA NGƯỜI CHƠI'''
#     cur_pos = spf.find_position_player(now_state.board)
    
#     '''LẤY DANH SÁCH VỊ TRÍ MÀ NGƯỜI CHƠI CÓ THỂ DI CHUYỂN'''
