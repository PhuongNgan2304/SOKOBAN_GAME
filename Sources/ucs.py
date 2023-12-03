import support_function as spf
import time
from copy import deepcopy
from queue import PriorityQueue
import psutil
import os

'''
//===========================//
//     GIẢI THUẬT UCS       //
//    IMPLEMENTATION       //
//========================//
'''

class state:
    def __init__(self, board, state_parent, list_check_point , cost):
        self.board = board
        self.state_parent = state_parent
        self.cost = cost
        self.check_points = deepcopy(list_check_point)

    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]
    
    def __gt__(self, other):
        return self.cost > other.cost
        
    def __lt__(self, other):
        return self.cost < other.cost
        

def UCS_Search(board, list_check_point):
    box_push_count = 0
    result = spf.Result()

    if spf.check_win(board, list_check_point):
        print("Found Win")
        return [board]

    start_state = state(board, None, list_check_point, 0)
    list_state = set()
    cost_queue = PriorityQueue()

    list_state.add(tuple(map(tuple, board)))
    cost_queue.put((0, start_state))

    while not cost_queue.empty():
        current_cost, now_state = cost_queue.get()

        cur_pos = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        for next_pos in list_can_move:
            new_board, move_cost = spf.move_with_cost(now_state.board, next_pos, cur_pos, list_check_point)
            new_cost = current_cost + move_cost

            if move_cost > 1:
                box_push_count += 1
                
            if tuple(map(tuple, new_board)) in list_state:
                continue

            if spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = state(new_board, now_state, list_check_point, new_cost)

            if spf.check_win(new_board, list_check_point):
                print("\nUniform Cost Search")
                print("Found Win")
                print("  Số trạng thái đã duyệt : {} ".format(len(list_state)))
                print("  Số lần đẩy hộp : {} ".format(box_push_count))
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024 ** 2)

                result.approved_states = len(list_state)
                result.memory = memory_usage
                result.time = time.time()
                result.list_board = (new_state.get_line(), len(list_state))
                result.algorithmName = "Uniform Cost Search"

                return result

            list_state.add(tuple(map(tuple, new_board)))
            cost_queue.put((new_cost, new_state))

    print("Not Found")
    return result