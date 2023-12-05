import support_function as spf
import time
from queue import PriorityQueue
import psutil
import os
from copy import deepcopy


'''
//========================//
//     GIẢI THUẬT A*      //
//    IMPLEMENTATION     //
//========================//
'''

class State:
    def __init__(self, board, state_parent, list_check_point):
        self.board = board
        self.state_parent = state_parent
        self.cost = 1
        self.heuristic = 0
        self.check_points = deepcopy(list_check_point)

    def compute_heuristic(self):
        if self.heuristic == 0:
            list_boxes = spf.find_boxes_position(self.board)
            self.heuristic = self.cost + abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0] - self.check_points[i][1] for i in range(len(list_boxes))))
        return self.heuristic

    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        return self.state_parent.get_line() + [self.board]

    def __gt__(self, other):
        return self.compute_heuristic() > other.compute_heuristic()

    def __lt__(self, other):
        return self.compute_heuristic() < other.compute_heuristic()

def AStar_manhattan_Search(board, list_check_point):
    start_time = time.time()
    result = spf.Result()
    box_push_count = 0

    if spf.check_win(board, list_check_point):
        print("Found Win")
        return [board]

    start_state = State(board, None, list_check_point)
    list_state = set()

    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)

    while not heuristic_queue.empty():
        now_state = heuristic_queue.get()
        cur_pos = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        for next_pos in list_can_move:
            new_board, move_cost = spf.move_with_cost(now_state.board, next_pos, cur_pos, list_check_point)
            if move_cost > 1:
                box_push_count += 1
            board_tuple = tuple(map(tuple, new_board))

            if board_tuple in list_state:
                continue

            if spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = State(new_board, now_state, list_check_point)

            if spf.check_win(new_board, list_check_point):
                print("\nA*(Manhattan)")
                print("Found Win")
                print("  Số trạng thái đã duyệt : {} ".format(len(list_state)))
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024**2)

                result = spf.Result()
                result.countFindBox = box_push_count
                result.approved_states = len(list_state)
                result.memory = memory_usage
                result.time = time.time()
                result.list_board = (new_state.get_line(), len(list_state))
                result.algorithmName = "A*(Manhattan)"

                return result

            list_state.add(board_tuple)
            heuristic_queue.put(new_state)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return result

    print("Not Found")
    return result