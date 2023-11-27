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
    def __init__(self, board, state_parent, list_check_point):
        self.board = board
        self.state_parent = state_parent
        if state_parent is None:
            self.cost = 0 # g(N), this is the start state
        else:
            self.cost = state_parent.cost + 1 # g(N), increment cost by 1 for the move
        self.check_points = deepcopy(list_check_point)

    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]
    
    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        else:
            return False

def UCS_Search(board, list_check_point):
    start_time = time.time()

    if spf.check_win(board, list_check_point):
        print("Found Win")
        return [board]

    start_state = state(board, None, list_check_point)
    list_state = [start_state]

    cost_queue = PriorityQueue()
    cost_queue.put((0, start_state))  # Khởi tạo queue với chi phí ban đầu là 0

    while not cost_queue.empty():
        '''LẤY TRẠNG THÁI HIỆN TẠI ĐỂ TÌM KIẾM'''
        current_cost, now_state = cost_queue.get() # Lấy chi phí và trạng thái hiện tại

        '''LẤY VỊ TRÍ HIỆN TẠI CỦA NGƯỜI CHƠI'''
        cur_pos = spf.find_position_player(now_state.board)

        '''LẤY DANH SÁCH VỊ TRÍ MÀ NGƯỜI CHƠI CÓ THỂ DI CHUYỂN ĐẾN'''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        
        '''TẠO TRẠNG THÁI MỚI TỪ DANH SÁCH CÓ THỂ DI CHUYỂN'''
        for next_pos in list_can_move:
            
            '''TẠO BẢNG MỚI'''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            
            '''NẾU BẢNG NÀY CHƯA TỒN TẠI TRONG DANH SÁCH TRẠNG THÁI THÌ BỎ QUA TRẠNG THÁI NÀY'''
            if spf.is_board_exist(new_board, list_state):
                continue
            
            '''NẾU MỘT HOẶC NHIỀU HỘP BỊ KẸT TRONG GÓC THÌ BỎ QUA TRẠNG THÁI NÀY'''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            
            '''NẾU TẤT CẢ HỘP BỊ KẸT THÌ BỎ QUA TRẠNG THÁI NÀY'''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue
            
            '''TẠO TRẠNG THÁI MỚI'''
            new_state = state(new_board, now_state, list_check_point)

            '''KIỂM TRA XEM TRẠNG THÁI MỚI CÓ PHẢI LÀ TRẠNG THÁI KẾT THÚC KHÔNG'''
            if spf.check_win(new_board, list_check_point):
                print("\nUniform Cost Search")
                print("Found Win")
                print("  Số trạng thái đã duyệt : {} ".format(len(list_state)))
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024**2)

                result = spf.Result()
                result.approved_states = len(list_state)
                result.memory = memory_usage
                result.time = time.time()
                result.list_board = (new_state.get_line(), len(list_state))
                result.algorithmName = "Uniform Cost Search"
                
                return result

            '''THÊM TRẠNG THÁI MỚI VÀO HÀNG ĐỢI ƯU TIÊN VÀ DANH SÁCH ĐÃ ĐƯỢC DUYỆT'''
            list_state.append(new_state)
            new_cost = current_cost + 1
            cost_queue.put((new_cost, new_state))
            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / (1024**2)

            '''TÍNH THỜI GIAN TIMEOUT'''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    
    ''' KHÔNG TÌM THẤY GIẢI PHÁP '''
    print("Not Found")
    return []

        
