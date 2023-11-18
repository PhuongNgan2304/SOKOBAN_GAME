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
    
    ''' GIẢI PHÁP TÌM KIẾM BEST FIRST SEARCH '''
    
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
                print("\nBest First Search")
                print("Found Win")
                print("  Số trạng thái đã duyệt : {} ".format(len(list_state)))
                process = psutil.Process(os.getpid())
                memory_usage = process.memory_info().rss / (1024**2)
                print(f"  Bộ nhớ: {memory_usage} Mb")
                return (new_state.get_line(), len(list_state))
            
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
