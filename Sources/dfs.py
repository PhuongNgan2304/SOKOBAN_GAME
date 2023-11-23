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
        self.cost = 1
        self.heuristic = 0
        self.check_points = deepcopy(list_check_point)
    '''HÀM ĐỆ QUY ĐỂ TRUY VẾT ĐẾN TRẠNG THÁI ĐẦU TIÊN NẾU TRẠNG THÁI HIỆN TẠI LÀ MỤC TIÊU'''
    def get_line(self):
        '''sử dụng vòng lặp để tìm danh sách trạng thái từ đầu đến trạng thái hiện tại'''
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]
    '''TÍNH HÀM HEURISTIC ĐƯỢC SỬ DỤNG CHO GIẢI THUẬT A*'''
    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            self.heuristic = self.cost + abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0] - self.check_points[i][1] for i in range(len(list_boxes))))
           
        return self.heuristic
    '''NẠP TOÁN TỬ CHO PHÉP LƯU TRẠNG THÁI TRONG HÀNG ĐỢI ƯU TIÊN'''
    def __gt__(self, other):
        if self.compute_heuristic() > other.compute_heuristic():
            return True
        else:
            return False
    def __lt__(self, other):
        if self.compute_heuristic() < other.compute_heuristic():
            return True
        else :
            return False


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

            #    print("\nDepth First Search")
            #    print("Found Win")
            #    print(" Số trạng thái đã duyệt : {} ".format(len(list_state)))
            #    process = psutil.Process(os.getpid())
            #    memory_usage = process.memory_info().rss / (1024**2)
            #    print(f" Bộ nhớ: {memory_usage} Mb")

               
            
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