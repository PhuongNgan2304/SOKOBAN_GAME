import support_function as spf
import time
from queue import PriorityQueue
import psutil
import os
from copy import deepcopy

#CHECK LẠI SAU CHO CHẮC

'''
//========================//
//     GIẢI THUẬT A*      //
//    IMPLEMENTATION     //
//========================//
'''

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
        list_boxes = spf.find_boxes_position(self.board)
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



def AStar_Search(board, list_check_point):
    start_time = time.time()
    
    ''' GIẢI PHÁP TÌM KIẾM A* '''
    
    ''' NẾU BẢNG BẮT ĐẦU LÀ BẢNG KẾT THÚC HOẶC KHÔNG CÓ ĐIỂM KIỂM TRA '''
    if spf.check_win(board, list_check_point):
        print("Found Win")
        return [board]
    
    ''' KHỞI TẠO TRẠNG THÁI BẮT ĐẦU '''
    start_state = state(board, None, list_check_point)
    list_state = [start_state]
    
    ''' KHỞI TẠO HÀNG ĐỢI ƯU TIÊN '''
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    
    ''' LẶP QUA HÀNG ĐỢI ƯU TIÊN '''
    while not heuristic_queue.empty():
        
        '''LẤY TRẠNG THÁI HIỆN TẠI ĐỂ TÌM KIẾM'''
        now_state = heuristic_queue.get()
        
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
                print("\nManhattan Distance Heuristic")
                print("Found Win")
                print("  Số trạng thái đã duyệt : {} ".format(len(list_state)))
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024**2)

                result = spf.Result()
                result.approved_states = len(list_state)
                result.memory = memory_usage
                result.time = time.time()
                result.list_board = (new_state.get_line(), len(list_state))
                result.algorithmName = "Manhattan Distance Heuristic"
                
                return result
            
            '''THÊM TRẠNG THÁI MỚI VÀO HÀNG ĐỢI ƯU TIÊN VÀ DANH SÁCH ĐÃ ĐƯỢC DUYỆT'''
            list_state.append(new_state)
            heuristic_queue.put(new_state)
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
