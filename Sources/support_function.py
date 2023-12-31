from copy import deepcopy
import math
import csv
import os

TIME_OUT = 1800

'''
//========================//
//      CÁC HÀM HỖ TRỢ     //
//========================//
'''


class Result:
    def __init__(self):
        self.approved_states = None
        self.memory = None
        self.map_level = None
        self.time = None
        self.list_board = None
        self.countFindBox = 0
        self.algorithmName = None
        self.countMove = 0 


'''KIỂM TRA XEM BẢNG CÓ PHẢI LÀ MỤC TIÊU HAY KHÔNG'''


def check_win(board, list_check_point):
    '''trả về True nếu tất cả các điểm kiểm tra được che phủ bởi các hộp'''
    for p in list_check_point:
        if board[p[0]][p[1]] != '$':
            return False
    return True


'''GÁN MA TRẬN'''


def assign_matrix(board):
    '''trả về bảng giống như bảng đầu vào'''
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]


'''TÌM VỊ TRÍ HIỆN TẠI CỦA NGƯỜI CHƠI TRONG BẢNG'''


def find_position_player(board):
    '''trả về vị trí của người chơi trong bảng'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '@':
                return (x, y)
    return (-1, -1)  # bảng lỗi


'''SO SÁNH 2 BẢNG'''


def compare_matrix(board_A, board_B):
    '''trả về True nếu bảng A giống bằng bảng B'''
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True


'''KIỂM TRA XEM BẢNG ĐÃ TỒN TẠI TRONG DANH SÁCH ĐÃ ĐI QUA CHƯA'''


def is_board_exist(board, list_state):
    '''trả về True nếu có bảng giống trong danh sách'''
    for state in list_state:
        if compare_matrix(state.board, board):
            return True
    return False


'''KIỂM TRA XEM CÓ ÍT NHẤT MỘT HỘP NẰM TRÊN ĐIỂM KIỂM TRA KHÔNG'''


def is_box_on_check_point(box, list_check_point):
    for check_point in list_check_point:
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False


'''KIỂM TRA XEM ÍT NHẤT MỘT HỘP CÓ BỊ KẸT CẠN Ở GÓC KHÔNG'''


def check_in_corner(board, x, y, list_check_point):
    '''trả về True nếu board[x][y] ở góc'''
    if board[x - 1][y - 1] == '#':
        if board[x - 1][y] == '#' and board[x][y - 1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x + 1][y - 1] == '#':
        if board[x + 1][y] == '#' and board[x][y - 1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x - 1][y + 1] == '#':
        if board[x - 1][y] == '#' and board[x][y + 1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x + 1][y + 1] == '#':
        if board[x + 1][y] == '#' and board[x][y + 1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    return False


'''TÌM TẤT CẢ VỊ TRÍ HỘP TRÊN BẢNG'''


def find_boxes_position(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                result.append((i, j))
    return result


'''KIỂM TRA XEM ÍT NHẤT MỘT HỘP CÓ THỂ DI CHUYỂN ÍT NHẤT 1 HƯỚNG'''


def is_box_can_be_moved(board, box_position):
    left_move = (box_position[0], box_position[1] - 1)
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])
    if (board[left_move[0]][left_move[1]] == ' ' or board[left_move[0]][left_move[1]] == '%' or board[left_move[0]][
        left_move[1]] == '@') and board[right_move[0]][right_move[1]] != '#' and board[right_move[0]][
        right_move[1]] != '$':
        return True
    if (board[right_move[0]][right_move[1]] == ' ' or board[right_move[0]][right_move[1]] == '%' or
        board[right_move[0]][right_move[1]] == '@') and board[left_move[0]][left_move[1]] != '#' and \
            board[left_move[0]][left_move[1]] != '$':
        return True
    if (board[up_move[0]][up_move[1]] == ' ' or board[up_move[0]][up_move[1]] == '%' or board[up_move[0]][
        up_move[1]] == '@') and board[down_move[0]][down_move[1]] != '#' and board[down_move[0]][down_move[1]] != '$':
        return True
    if (board[down_move[0]][down_move[1]] == ' ' or board[down_move[0]][down_move[1]] == '%' or board[down_move[0]][
        down_move[1]] == '@') and board[up_move[0]][up_move[1]] != '#' and board[up_move[0]][up_move[1]] != '$':
        return True
    return False


'''KIỂM TRA XEM TẤT CẢ CÁC HỘP CÓ BỊ KẸT CẠN KHÔNG'''


def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_on_check_point(box_position, list_check_point):
            return False
        if is_box_can_be_moved(board, box_position):
            result = False
    return result


'''KIỂM TRA XEM ÍT NHẤT MỘT HỘP CÓ THỂ ĐẾN ĐƯỢC VỊ TRÍ THÀNH CÔNG ÍT NHẤT 1 HƯỚNG'''


def is_board_can_not_win(board, list_check_point):
    '''trả về True nếu hộp nằm ở góc của bức tường -> không thể thắng'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                if check_in_corner(board, x, y, list_check_point):
                    return True
    return False


'''LẤY BƯỚC TIẾP THEO CÓ THỂ DI CHUYỂN'''


def get_next_pos(board, cur_pos):
    '''trả về danh sách vị trí mà người chơi có thể di chuyển đến từ vị trí hiện tại'''
    x, y = cur_pos[0], cur_pos[1]
    list_can_move = []
    # DI CHUYỂN LÊN (x - 1, y)
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x - 1, y))
        elif value == '$' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x - 1, y))
    # DI CHUYỂN XUỐNG (x + 1, y)
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x + 1, y))
    # DI CHUYỂN TRÁI (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board[0]):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y - 1))
    # DI CHUYỂN PHẢI (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board[0]):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y + 1))
    return list_can_move


'''DI CHUYỂN BẢNG THEO CÁC HƯỚNG NHẤT ĐỊNH'''


def move(board, next_pos, cur_pos, list_check_point):
    '''trả về một bảng mới sau khi di chuyển'''
    # TẠO BẢNG MỚI NHƯ BẢNG HIỆN TẠI
    new_board = assign_matrix(board)
    # TÌM VỊ TRÍ TIẾP THEO NẾU DI CHUYỂN ĐẾN HỘP
    if new_board[next_pos[0]][next_pos[1]] == '$':
        x = 2 * next_pos[0] - cur_pos[0]
        y = 2 * next_pos[1] - cur_pos[1]
        new_board[x][y] = '$'
    # DI CHUYỂN NGƯỜI CHƠI ĐẾN VỊ TRÍ MỚI
    new_board[next_pos[0]][next_pos[1]] = '@'
    new_board[cur_pos[0]][cur_pos[1]] = ' '
    # KIỂM TRA NẾU TẠI VỊ TRÍ ĐIỂM KIỂM TRA KHÔNG CÓ GÌ THÌ CẬP NHẬT % NHƯ ĐIỂM KIỂM TRA
    for p in list_check_point:
        if new_board[p[0]][p[1]] == ' ':
            new_board[p[0]][p[1]] = '%'
    return new_board

def move_with_cost(board, next_pos, cur_pos, list_check_point):
    '''trả về một bảng mới sau khi di chuyển'''
    # TẠO BẢNG MỚI NHƯ BẢNG HIỆN TẠI
    new_board = assign_matrix(board)
    # TẠO BIẾN COST
    new_cost = 0
    # TÌM VỊ TRÍ TIẾP THEO NẾU DI CHUYỂN ĐẾN HỘP
    if new_board[next_pos[0]][next_pos[1]] == '$':
        x = 2 * next_pos[0] - cur_pos[0]
        y = 2 * next_pos[1] - cur_pos[1]
        new_board[x][y] = '$'
        new_cost += 2  # Di chuyển kèm theo hộp, cost + 2
    # DI CHUYỂN NGƯỜI CHƠI ĐẾN VỊ TRÍ MỚI
    new_board[next_pos[0]][next_pos[1]] = '@'
    new_board[cur_pos[0]][cur_pos[1]] = ' '
    # KIỂM TRA NẾU TẠI VỊ TRÍ ĐIỂM KIỂM TRA KHÔNG CÓ HỘP HAY NHÂN VẬT THÌ CẬP NHẬT % NHƯ CŨ
    for p in list_check_point:
        if new_board[p[0]][p[1]] == ' ':
            new_board[p[0]][p[1]] = '%'
    new_cost += 1
    return new_board ,new_cost



'''TÌM DANH SÁCH CÁC ĐIỂM KIỂM TRA TRÊN BẢNG'''


def find_list_check_point(board):
    '''trả về danh sách điểm kiểm tra từ bảng
        nếu không có bất kỳ điểm kiểm tra nào, trả về danh sách trống
        nó sẽ kiểm tra số hộp, nếu số hộp < số điểm kiểm tra
            trả về danh sách [(-1, -1)]'''
    list_check_point = []
    num_of_box = 0
    '''KIỂM TRA TOÀN BỘ BẢNG ĐỂ TÌM ĐIỂM KIỂM TRA VÀ SỐ HỘP'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                num_of_box += 1
            elif board[x][y] == '%':
                list_check_point.append((x, y))
    '''KIỂM TRA NẾU SỐ HỘP < SỐ LƯỢNG ĐIỂM KIỂM TRA'''
    if num_of_box < len(list_check_point):
        return [(-1, -1)]
    return list_check_point


# DI CHUYỂN BẢNG THEO HÀNH ĐỘNG NGƯỜI DÙNG
def move_board_by_key(board, cur_pos, key, list_check_point):
    key_list = ['LEFT', 'UP', "RIGHT", "DOWN"]
    if key in key_list:
        if key == 'LEFT':
            next_pos = (cur_pos[0], cur_pos[1] - 1)
        elif key == 'RIGHT':
            next_pos = (cur_pos[0], cur_pos[1] + 1)
        elif key == 'UP':
            next_pos = (cur_pos[0] - 1, cur_pos[1])
        elif key == 'DOWN':
            next_pos = (cur_pos[0] + 1, cur_pos[1])

        # Kiểm tra xem nước đi tiếp theo có hợp lệ hay không
        if 0 <= next_pos[0] < len(board) and 0 <= next_pos[1] < len(board[0]) and board[next_pos[0]][
            next_pos[1]] != '#':
            if board[next_pos[0]][next_pos[1]] == '$':
                # Kiểm tra xem hộp có thể được đẩy hay không
                if key == 'LEFT':
                    next_box_pos = (next_pos[0], next_pos[1] - 1)
                elif key == 'RIGHT':
                    next_box_pos = (next_pos[0], next_pos[1] + 1)
                elif key == 'UP':
                    next_box_pos = (next_pos[0] - 1, next_pos[1])
                elif key == 'DOWN':
                    next_box_pos = (next_pos[0] + 1, next_pos[1])
                if 0 <= next_box_pos[0] < len(board) and 0 <= next_box_pos[1] < len(board[0]) and (
                        board[next_box_pos[0]][next_box_pos[1]] == ' ' or board[next_box_pos[0]][
                    next_box_pos[1]] == '%'):
                    new_board = move(board, next_pos, cur_pos, list_check_point)
                    return new_board
            else:
                new_board = move(board, next_pos, cur_pos, list_check_point)
                return new_board
    return board  # Trả về bảng hiện tại nếu nước đi không hợp lệ
    if board[next_pos[0]][next_pos[1]] == '$':
        # Kiểm tra xem hộp có thể được đẩy hay không
        if key == 'LEFT':
            next_box_pos = (next_pos[0], next_pos[1] - 1)
        elif key == 'RIGHT':
            next_box_pos = (next_pos[0], next_pos[1] + 1)
        elif key == 'UP':
            next_box_pos = (next_pos[0] - 1, next_pos[1])
        elif key == 'DOWN':
            next_box_pos = (next_pos[0] + 1, next_pos[1])
        if 0 <= next_box_pos[0] < len(board) and 0 <= next_box_pos[1] < len(board[0]) and (board[next_box_pos[0]][next_box_pos[1]] == ' ' or board[next_box_pos[0]][next_box_pos[1]] == '%'):
            new_board = move(board, next_pos, cur_pos, list_check_point)
            return new_board
    else:
        new_board = move(board, next_pos, cur_pos, list_check_point)
        return new_board

    return board  # Trả về bảng hiện tại nếu nước đi không hợp lệ

def export_result_to_csv(result, map_name, csv_folder="thongke"):
    # Tạo thư mục nếu nó chưa tồn tại
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    csv_file_path = os.path.join(csv_folder, f"{map_name}_thongke.csv")

    # Write the header if the file is newly created
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Algorithm', 'Approved States', 'Memory (MB)', 'Map Level', 'Time (s)', 'Count Push Box', 'Count Move']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # Read existing rows from the CSV file to check for existing algorithm name
    existing_rows = []
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            existing_rows = list(reader)

    # Check if the algorithm name already exists in the CSV file
    algorithm_exists = any(row[0] == result.algorithmName for row in existing_rows)

    # If the algorithm name already exists, find its index
    if algorithm_exists:
        index = next((i for i, row in enumerate(existing_rows) if row[0] == result.algorithmName), None)

        # Replace the existing row with the new result
        if index is not None:
            existing_rows[index] = [
                result.algorithmName,
                result.approved_states,
                result.memory,
                result.map_level,
                result.time,
                result.countFindBox,
                result.countMove
            ]
    else:
        # Append a new row for the new algorithm
        existing_rows.append([
            result.algorithmName,
            result.approved_states,
            result.memory,
            result.map_level,
            result.time,
            result.countFindBox,
            result.countMove
        ])

    # Write all rows (either modified or new) back to the CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(existing_rows)