import numpy as np
import os
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import bfs
import astar
import astar1
import best_first_search
import depth_limited_search as dls
import ucs
import dfs
import time
import support_function as spf

# https://github.com/PhuongNgan2304/SOKOBAN_GAME
# https://docs.google.com/document/d/118NqEutRUE-oxi2sj6qA7EeEyp5Fw9HK/edit#heading=h.49x2ik5

''' Timeout của mỗi map là 30 phút  '''
TIME_OUT = 120
# !!!PHẦN LẤY PATH MỌI NGƯỜI CHỈNH LẠI CÁI ĐƯỜNG DẪN NHA. LƯU Ở ĐÂU THÌ DẪN Ở ĐÓ, RỒI CHẠY BÌNH THƯỜNG
''' lấy path của folder testcases và checkpoints '''
#path_board = os.getcwd() + '\\..\\Testcases'
#path_checkpoint = os.getcwd() + '\\..\\Checkpoints'
path_board = 'D:/HOC_KY_1_NAM_3/AI/PROJECT_NEW/SOKOBAN_GAME/Testcases'
path_checkpoint = 'D:/HOC_KY_1_NAM_3/AI/PROJECT_NEW/SOKOBAN_GAME/Checkpoints'

''' lấy data từ các testcase để trả lại các bảng gồm các map'''


def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_board}/{file}"
            board = get_board(file_path)
            # in file 
            list_boards.append(board)
    return list_boards


''' truyền data từ các file checkpoint để trả lại vị trí các checkpoint trong map'''


def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}/{file}"
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point


''' chuyển đổi các ký tự trong một hàng từ file TXT sang ký tự tượng trưng để hiện thị map trong game'''


def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':  # wall
            row[i] = '#'  # wall
        elif row[i] == 'p':  # dog
            row[i] = '@'  # dog
        elif row[i] == 'b':  # bone
            row[i] = '$'  # bone
        elif row[i] == 'c':  # house
            row[i] = '%'  # house


''' chuyển đổi ký tự checkpoint từ file txt sao chép sang một mảng '''


def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result


''' trả về bản đồ dưới dạng một mảng NumPy, trong đó các ký tự đã được chuyển đổi thành các ký tự thể hiện các phần tử của bản đồ.'''


def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result


'''trả về checkpoints dưới dạng một mảng NumPy, trong đó các ký tự đã được chuyển đổi thành các ký tự thể hiện các phần tử của checkpoint. '''


def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result


def draw_text(surface, text, position, font_size, alignment="center"):
    font = pygame.font.Font('gameFont.ttf', font_size)
    text_render = font.render(text, True, (0, 0, 0))
    if alignment == "topRight":
        text_rect = text_render.get_rect(topRight=position)
    else:
        text_rect = text_render.get_rect(center=position)

    surface.blit(text_render, text_rect)


'''
//========================//
//     KHAI BÁO VÀ        //
//  KHỞI TẠO BẢN ĐỒ VÀ   //
//      ĐIỂM KIỂM TRA      //
//========================//
'''
maps = get_boards()  # Lấy bản đồ
check_points = get_check_points()  # Lấy điểm kiểm tra

'''
//========================//
//         PYGAME         //
//     KHỞI TẠO HÌNH ẢNH  //
//                        //
//========================//
'''
pygame.init()  # Khởi tạo Pygame
pygame.font.init()  # Khởi tạo font Pygame
screen = pygame.display.set_mode((640, 640))  # Khởi tạo màn hình với kích thước 640x640
pygame.display.set_caption('Corgi Sokoban')  # Đặt tiêu đề cửa sổ là 'Sokoban'
clock = pygame.time.Clock()  # Tạo một đồng hồ
BACKGROUND = (0, 0, 0)  # Màu nền đen
WHITE = (0, 0, 0)  # Màu trắng bị đổi sang đen

'''
LẤY CÁC TÀI SẢN
'''
assets_path = os.getcwd() + "\\..\\Assets"  # Đường dẫn đến thư mục chứa tài sản
os.chdir(assets_path)  # Thay đổi thư mục làm việc hiện tại thành thư mục tài sản
player = pygame.image.load(os.getcwd() + '\\image\\corgi_new.png')  # Tải hình ảnh người chơi
wall = pygame.image.load(os.getcwd() + '\\image\\wall_new.png')  # Tải hình ảnh tường
box = pygame.image.load(os.getcwd() + '\\image\\bone_new2.png')  # Tải hình ảnh hộp
point = pygame.image.load(os.getcwd() + '\\image\\house_new2.png')  # Tải hình ảnh điểm kiểm tra
space = pygame.image.load(os.getcwd() + '\\image\\grass_new.jpg')  # Tải hình ảnh không gian
arrow_left = pygame.image.load(os.getcwd() + '\\image\\arrow_left.png')  # Tải hình ảnh mũi tên trái
arrow_right = pygame.image.load(os.getcwd() + '\\image\\arrow_right.png')  # Tải hình ảnh mũi tên phải
init_background = pygame.image.load(os.getcwd() + '\\image\\background_grass.jpg')  # Tải hình ảnh nền khởi tạo
loading_background = pygame.image.load(os.getcwd() + '\\image\\background_grass.jpg')  # Tải hình ảnh nền tải
notfound_background = pygame.image.load(
    os.getcwd() + '\\image\\background_grass.jpg')  # Tải hình ảnh nền không tìm thấy
found_background = pygame.image.load(os.getcwd() + '\\image\\background_grass.jpg')  # Tải hình ảnh nền tìm thấy

'''
HIỂN THỊ BẢN ĐỒ CHO TRÒ CHƠI
'''


def renderMap(board):
    width = len(board[0])
    height = len(board)
    indent = (640 - width * 32) / 2.0  # Tính khoảng cách lề , với width là số lượng 
    for i in range(height):
        for j in range(width):
            screen.blit(space, (j * 32 + indent, i * 32 + 250))  # Hiển thị không gian
            if board[i][j] == '#':
                screen.blit(wall, (j * 32 + indent, i * 32 + 250))  # Hiển thị tường
            if board[i][j] == '$':
                screen.blit(box, (j * 32 + indent, i * 32 + 250))  # Hiển thị hộp
            if board[i][j] == '%':
                screen.blit(point, (j * 32 + indent, i * 32 + 250))  # Hiển thị điểm kiểm tra
            if board[i][j] == '@':
                screen.blit(player, (j * 32 + indent, i * 32 + 250))  # Hiển thị người chơi


'''
KHỞI TẠO CÁC BIẾN
'''
# Mức độ bản đồ
mapNumber = 0
# Thuật toán giải trò chơi
algorithm = "NORMAL"
# Trạng thái cảnh, bao gồm:
# init để chọn bản đồ và thuật toán
# loading để hiển thị cảnh "đang tải"
# executing để giải quyết vấn đề
# playing để hiển thị trò chơi
sceneState = "init"
loading = False

''' HÀM SOKOBAN '''
start_time = 0
end_time = 0
steps = 0  # để lưu số bước di chuyển
steps1 = 0  # để lưu lại stateLength
steps2 = steps  # để lưu lại giá trị của steps
initial_memory = 0


## normal playing
# def normal_playing(event) :


def sokoban():
    running = True
    global sceneState
    global loading
    global algorithm
    global list_board
    list_board = None
    global mapNumber
    stateLength = 0
    currentState = 0
    found = True
    global steps
    global steps1
    global steps2
    global board_playing
    board_playing = None
    count_step = 0 
    

    while running:
        screen.blit(init_background, (0, 0))
        if sceneState == "init":
            initGame(maps[mapNumber])
            board_playing = maps[mapNumber]
        if sceneState == "executing":
            list_check_point = check_points[mapNumber]
            # Bắt đầu đếm thời gian
            start_time = time.time()
            if algorithm == "NORMAL":
                sceneState = "normalplaying"
                continue
            elif algorithm == "Euclidean Distance Heuristic":
                result = astar1.AStar_Search1(maps[mapNumber], list_check_point)
            elif algorithm == "Manhattan Distance Heuristic":
                result = astar.AStar_Search(maps[mapNumber], list_check_point)
            elif algorithm == " Greedy Best First Search":
                result = best_first_search.Best_First_Search(maps[mapNumber], list_check_point)
            elif algorithm == "Uniform Cost Search":
                result = ucs.UCS_Search(maps[mapNumber], list_check_point)
            elif algorithm == "DLS":
                max_deep = 300
                result = dls.DLS_Search(maps[mapNumber], list_check_point, max_deep)
            elif algorithm == "DFS":
                result = dfs.DFS_search(maps[mapNumber], list_check_point)
            else:
                result = bfs.BFS_search(maps[mapNumber], list_check_point)

            # Dừng đếm thời gian
            end_time = time.time()
            if isinstance(result, spf.Result) and result.list_board is not None:
                if result.list_board is not None and len(result.list_board) > 0:
                    sceneState = "playing"
                    stateLength = len(result.list_board[0])
                    currentState = 0
                    elapsed_time = end_time - start_time
                    result.time = elapsed_time
                    print(f"  Map: Level {mapNumber + 1} ")
                    #  thời gian giải thuật
                    print(f"  Thời gian: {elapsed_time} seconds")
            elif sceneState == "normalplaying":
                continue
            else:
                sceneState = "end"
                found = False

        if sceneState == "loading":
            loadingGame()
            sceneState = "executing"

        if sceneState == "end":
            if found:
                foundGame(result, result.list_board[0][stateLength - 1], steps2)
                steps = 0
            else:
                notfoundGame()

        if sceneState == "playing":
            clock.tick(20)
            renderMap(result.list_board[0][currentState])
            currentState = currentState + 1
            steps += 1
            draw_text(screen, 'Số bước: {}'.format(steps), (320, 50), 20, alignment='topLeft')
            if currentState == stateLength:
                steps2 = steps
                sceneState = "end"
                found = True
                steps = stateLength  # Đặt số bước là chiều dài trạng thái
                

        if sceneState == "normalplaying":
            draw_text(screen, 'Số bước: {}'.format(count_step), (320, 170), 20)
            renderMap(board_playing)
            if spf.check_win(board_playing,list_check_point):
                draw_text(screen, 'Yeah! Đã tìm thấy lời giải!!!', (320, 20), 30)
                draw_text(screen, 'Số bước: {}'.format(count_step), (320, 90), 20)
                draw_text(screen, 'Nhấn ESC để tiếp tục', (320, 600), 20)
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if sceneState == "init":
                        sceneState = "loading"
                    if sceneState == "end":
                        sceneState = "init"
                if sceneState == "init":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            if mapNumber < len(maps) - 1:
                                mapNumber = mapNumber + 1
                        if event.key == pygame.K_LEFT:
                            if mapNumber > 0:
                                mapNumber = mapNumber - 1
                        if event.key == pygame.K_SPACE:
                            if algorithm == "Euclidean Distance Heuristic":
                                algorithm = "Manhattan Distance Heuristic"
                            elif algorithm == "Manhattan Distance Heuristic":
                                algorithm = "BFS"
                            elif algorithm == "BFS":
                                algorithm = "DFS"
                            elif algorithm == "DFS":
                                algorithm = " Greedy Best First Search"
                            elif algorithm == "Greedy Best First Search":
                                algorithm = "DLS"
                            elif algorithm == "DLS":
                                algorithm = "Uniform Cost Search"
                            elif algorithm == "Uniform Cost Search":
                                algorithm = "NORMAL"
                            else:
                                algorithm = "Euclidean Distance Heuristic"
                if sceneState == "normalplaying":
                    if event.type == pygame.KEYDOWN:
                        current_pos = spf.find_position_player(board_playing)
                        if event.key == pygame.K_RIGHT:
                            board_playing = spf.move_board_by_key(board_playing, current_pos, 'RIGHT', list_check_point)
                            count_step = count_step + 1
                        if event.key == pygame.K_LEFT:
                            board_playing = spf.move_board_by_key(board_playing, current_pos, 'LEFT', list_check_point)
                            count_step = count_step + 1
                        if event.key == pygame.K_UP:
                            board_playing = spf.move_board_by_key(board_playing, current_pos, 'UP', list_check_point)
                            count_step = count_step + 1
                        if event.key == pygame.K_DOWN:
                            board_playing = spf.move_board_by_key(board_playing, current_pos, 'DOWN', list_check_point)
                            count_step = count_step + 1
                        if event.key == pygame.K_ESCAPE:
                            sceneState = "init"

        pygame.display.flip()

    pygame.quit()


# HIỂN THỊ MÀN HÌNH BAN ĐẦU
def initGame(map):
    draw_text(screen, 'Corgi Brings Bones', (320, 80), 60)
    draw_text(screen, 'Chọn Map bằng mũi tên < >', (320, 140), 20)
    # draw_text(screen, 'Số bước: {}'.format(steps), (320, 170), 20)
    draw_text(screen, 'Nhấn SPACE để đổi thuật toán', (320, 550), 20)
    draw_text(screen, " Map: " + str(mapNumber + 1) + " ", (320, 200), 30)
    screen.blit(arrow_left, (240, 188))
    screen.blit(arrow_right, (376, 188))
    draw_text(screen, str(algorithm), (320, 600), 30)
    renderMap(map)


# HIỂN THỊ CẢNH TẢI
def loadingGame():
    screen.blit(loading_background, (0, 0))
    draw_text(screen, 'ĐANG TẢI', (320, 60), 40)
    draw_text(screen, 'Đang tìm lời giải............', (320, 100), 20)


def foundGame(result, map, steps):
    global steps2
    screen.blit(found_background, (0, 0))
    draw_text(screen, 'Yeah! Đã tìm thấy lời giải!!!', (320, 20), 30)
    draw_text(screen, 'Thuật Toán : {}'.format(result.algorithmName), (320, 60), 20)
    draw_text(screen, 'Số bước: {}'.format(steps2), (320, 90), 20)
    draw_text(screen, "Bộ nhớ: {} Mb".format(result.memory), (320, 120), 20)
    draw_text(screen, "Số trạng thái đã duyệt: {}".format(result.approved_states), (320, 160), 20)
    draw_text(screen, "Thời gian : {}s".format(result.time), (320, 200), 20)
    draw_text(screen, 'Nhấn ENTER để tiếp tục', (320, 600), 20)
    renderMap(map)


def notfoundGame():
    screen.blit(notfound_background, (0, 0))
    draw_text(screen, 'Không thể tìm ra lời giải', (320, 100), 40)
    draw_text(screen, 'Nhấn ENTER để tiếp tục', (320, 600), 20)


def main():
    sokoban()


if __name__ == "__main__":
    main()
