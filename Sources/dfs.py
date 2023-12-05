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
   box_push_count = 0
   
   if spf.check_win(board, list_check_point):
       print("Found Win")
       return [board]
   
   ''' KHỞI TẠO TRẠNG THÁI BẮT ĐẦU '''
   start_state = state(board, None, list_check_point)
   
   ''' KHỞI TẠO 2 DANH SÁCH ĐƯỢC SỬ DỤNG CHO TÌM KIẾM DFS '''
   stack = [start_state]
   visited = set()
   
   while stack:
       now_state = stack.pop()
       cur_pos = spf.find_position_player(now_state.board)
       list_can_move = spf.get_next_pos(now_state.board, cur_pos)
       for next_pos in list_can_move:
           new_board, move_cost = spf.move_with_cost(now_state.board, next_pos, cur_pos, list_check_point)
           if move_cost > 1:
                box_push_count += 1
           board_tuple = tuple(map(tuple, new_board))  # convert board to tuple of tuples so it can be added to a set
           if board_tuple in visited:
               continue
           
           if spf.is_board_can_not_win(new_board, list_check_point):
               continue
           
           if spf.is_all_boxes_stuck(new_board, list_check_point):
               continue
           
           new_state = state(new_board, now_state, list_check_point)
           
           if spf.check_win(new_board, list_check_point):
                print("\nDepth First Search")
                print("Found Win")
                print("  Số trạng thái đã duyệt : {} ".format(len(visited)))
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024**2)
                result = spf.Result()
                result.countFindBox = box_push_count
                result.approved_states = len(visited)
                result.memory = memory_usage
                result.time = time.time()
                result.list_board = (new_state.get_line(), len(visited))
                result.algorithmName = "Depth First Search"
                return result
           
           visited.add(board_tuple)
           stack.append(new_state)
           process = psutil.Process(os.getpid())
           memory_usage = process.memory_info().rss / (1024**2)
           
           end_time = time.time()
           if end_time - start_time > TIME_OUT:
               return result
       
       end_time = time.time()
       if end_time - start_time > TIME_OUT:
           return result
   
   print("Not Found")
   return result
