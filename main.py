from ctypes.wintypes import SIZE
from msilib.schema import Font
from time import *
import os
from turtle import Screen, color
from matplotlib.pyplot import show
import pygame
import numpy as np
from sympy import false
from utilities import *


# Project AI Nhóm 2
# Thay đổi clock tick ở dòng 103, clock tick càng cao, nhân vật di chuyển càng nhanh

pygame.init()

SCREEN_SIZE = (600,600)
SCREEN_MENU = (600,600)
SCREEN_LEVEL = (600,600)
TITLE_STATE = "Loading"
clock = pygame.time.Clock()

BUTTON = (270,50)
ARROW = (50,50)

max_level = 15
 
def render_level(map_level): 
    map_size = pygame.font.Font("./fonts/minecraft_font.ttf",40)
    screen.blit(title_level,(SCREEN_SIZE[0]/2-title_level.get_width()/2-30,100))
    
    map_number = map_size.render(str(map_level), True, white)
    map_rect = map_number.get_rect(center=(340, 120))
    screen.blit(map_number, map_rect)

map_level=1
maze = load_maze(f'{map_level}.txt')
goal_state = load_goal_state(f'{map_level}.txt')


def level_zone(map_level,maze,mode):
    screen.fill((0,0,0))
    scale_image(SCREEN_SIZE[0]/(2*len(maze[0])),SCREEN_SIZE[0]/(2*len(maze)))
   
    screen.blit(background_menu,(0,0))

    global arrow_left_menu 
    arrow_left_menu = screen.blit(arrow_left,(0,SCREEN_LEVEL[1]/2-ARROW[0]/2))
    global arrow_right_menu
    arrow_right_menu= screen.blit(arrow_right,(SCREEN_LEVEL[0]-ARROW[0],SCREEN_LEVEL[1]/2-ARROW[0]/2))

    render_level(map_level)
    render_map(maze,screen, SCREEN_SIZE[0]/(2*len(maze[0])), SCREEN_SIZE[0]/(2*len(maze)), SCREEN_SIZE[0]/4, SCREEN_SIZE[1]/4)
    if TITLE_STATE == "Not found":
        screen.blit(title_notFound, (20,20))

    global mode_state
    if mode =="Bfs":
        mode_state = screen.blit(title_BFS,(SCREEN_SIZE[0]-return_button.get_width(),70))
    else:
        mode_state = screen.blit(title_Astar,(SCREEN_SIZE[0]-return_button.get_width(),70))
   
    global returnHome_button
    returnHome_button = screen.blit(return_button,(SCREEN_SIZE[0]-return_button.get_width(),0))

def menu_zone():
    button_pos = SCREEN_MENU[0]/2-BUTTON[0]/2
    button_quit_pos = SCREEN_MENU[0]/2-BUTTON[0]*0.4
    
    screen.blit(background_menu,(0,0))
    screen.blit(title_content, title_rect)

    global start_button
    start_button = screen.blit(button_start,(button_pos,200))

    global select_mode_button
    select_mode_button = screen.blit(title_mode,(button_pos,280))

    global exit_button
    exit_button = screen.blit(quit_button,(button_quit_pos,360))      
    
def render_map(maze,screen,width,height,dx=0,dy=0):
     for i in range (len(maze)):
        for j in range (len(maze[i])):
            screen.blit (floor, (j*width+dx, i*height+dy))
            if maze[i][j] == "1":
                screen.blit (wall, (j*width+dx, i*height+dy))
            elif maze[i][j] == "0":
                screen.blit (floor, (j*width+dx, i*height+dy))
            elif maze[i][j] == "x":
                screen.blit (car, (j*width+dx, i*height+dy))
            elif maze[i][j] == "g":
                screen.blit (goal, (j*width+dx, i*height+dy))
            elif maze[i][j] == "*":
                screen.blit (box, (j*width+dx, i*height+dy))

def end_zone(dy,run_time):
    screen.blit(end_background,(0,0))
    screen.blit(car,(SCREEN_SIZE[0]/2-car.get_width()/2,dy))
    #Thay đổi tốc độ hoạt ảnh ở đây!
    clock.tick(7) 

    if dy==SCREEN_SIZE[0]-140:
        global return_home 
        return_home = screen.blit(return_button,(SCREEN_SIZE[0]-return_button.get_width(),0))

    screen.blit(title_run_time,(SCREEN_SIZE[0]/2-title_run_time.get_width()/2-60,50))

    title_time_size = pygame.font.Font("./fonts/minecraft_font.ttf",30)
    
    title_time = title_time_size.render(str(round(run_time,2))+" sec", True, white)
    title_time_rect = title_time.get_rect(center=(410, 60))
    screen.blit(title_time, title_time_rect)
def mode_zone():

    button_pos = SCREEN_MENU[0]/2-BUTTON[0]*0.35

    screen.blit(background_menu,(0,0))
    screen.blit(title_content, title_rect)

    global bfs_mode
    bfs_mode = screen.blit(title_mode_BFS,(button_pos,220)) 

    global Astar_mode
    Astar_mode = screen.blit(title_mode_Astar,(button_pos,290)) 
    
def load_resource():
    global screen
    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.display.set_caption ('Corgi Brings Bone')
    icon = pygame.image.load ('./assets/icon_corgi.jpg')
    pygame.display.set_icon(icon)
    
    global floor1
    floor1 = pygame.image.load ('./assets/grass.jpg')
    
    global wall1
    wall1 = pygame.image.load ('./assets/wall.png')
   
    global car1
    car1 = pygame.image.load ('./assets/corgi_player.png')
    
    global box1
    box1 = pygame.image.load ('./assets/bone.png')
    
    global goal1
    goal1 = pygame.image.load ('./assets/dog_house.png')
    
    global white
    white = (255,255,255)

    global black
    black = (0,0,0)

    title_size = pygame.font.SysFont("sans",60)

    global title_content
    title_content =  pygame.image.load ('./assets/title_game.png')
    title_content =  pygame.transform.scale(title_content, (BUTTON[0]*1.5,BUTTON[1]*1.5))

    global title_notFound
    title_notFound =  pygame.image.load ('./assets/title_timeout.png')
    title_notFound =  pygame.transform.scale(title_notFound, (BUTTON[0],BUTTON[1]))

    global title_mode
    title_mode =  pygame.image.load ('./assets/Title_mode.png')
    title_mode =  pygame.transform.scale(title_mode, BUTTON)

    global title_level
    title_level =  pygame.image.load ('./assets/title_level.png')
    title_level =  pygame.transform.scale(title_level, (60,40))

    global title_run_time
    title_run_time =  pygame.image.load ('./assets/title_run_time.png')
    title_run_time =  pygame.transform.scale(title_run_time, (BUTTON[0]/2,BUTTON[1]/2))

    global title_BFS
    title_BFS =  pygame.image.load ('./assets/bfs_mode.png')
    title_BFS =  pygame.transform.scale(title_BFS, (BUTTON[0]/2,BUTTON[1]/2))

    global title_Astar
    title_Astar =  pygame.image.load ('./assets/Astar_mode.png')
    title_Astar =  pygame.transform.scale(title_Astar, (BUTTON[0]/2,BUTTON[1]/2))

    global title_mode_BFS
    title_mode_BFS =  pygame.image.load ('./assets/bfs_mode.png')
    title_mode_BFS =  pygame.transform.scale(title_mode_BFS, (BUTTON[0]*0.7,BUTTON[1]*0.7))

    global title_mode_Astar
    title_mode_Astar =  pygame.image.load ('./assets/Astar_mode.png')
    title_mode_Astar =  pygame.transform.scale(title_mode_Astar, (BUTTON[0]*0.7,BUTTON[1]*0.7))

    global title_loading
    title_loading =  pygame.image.load ('./assets/title_loading.png')
    title_loading =  pygame.transform.scale(title_loading, (BUTTON[0],BUTTON[1]))

    global title_rect
    title_rect = title_content.get_rect(center=(300, 60))

    global arrow_left
    arrow_left =  pygame.image.load ('./assets/arrowLeft.png')
    arrow_left =  pygame.transform.scale(arrow_left, ARROW)

    global arrow_right
    arrow_right =  pygame.image.load ('./assets/arrowRight.png')
    arrow_right =  pygame.transform.scale(arrow_right, ARROW)


    global background_menu 
    background_menu =  pygame.image.load ('./assets/loadMenu.png')
    background_menu = pygame.transform.scale(background_menu, SCREEN_MENU)

    global end_background
    end_background =  pygame.image.load ('./assets/endGame.jpg')
    end_background = pygame.transform.scale(end_background, SCREEN_MENU)

    global return_button
    return_button =  pygame.image.load ('./assets/returnHome.png')
    return_button = pygame.transform.scale(return_button, (150,50)) 

    global red 
    red = (235,51,36)

    global button_start 
    button_start =  pygame.image.load ('./assets/buttonStart.png')
    button_start =  pygame.transform.scale(button_start, BUTTON)

    global quit_button
    quit_button = pygame.image.load ('./assets/buttonQuit.png')
    quit_button =  pygame.transform.scale(quit_button, (BUTTON[0]*0.8,BUTTON[1]*0.8))

    global dark_red
    dark_red = (136,0,21)

    global title_end
    title_end = title_size.render('Press Enter to continue', True, white)
    
    
def scale_image(width,height):

    global floor
    floor = pygame.transform.scale(floor1, (width, height))
    global wall
    wall = pygame.transform.scale(wall1,(width, height))
    global car
    car = pygame.transform.scale(car1, (width, height))
    global box
    box = pygame.transform.scale(box1, (width, height))
    global goal 
    goal = pygame.transform.scale(goal1, (width, height))

def game_init(k,maze,curr_state, dx =0 , dy = 0):
    clock.tick(25)
    board = k[curr_state]
    render_map(board,screen,SCREEN_SIZE[0]/len(maze[0]),SCREEN_SIZE[0]/len(maze), dx, dy)


def game_zone():
    map_level=1
    maze = load_maze(f'{map_level}.txt')
    goal_state = load_goal_state(f'{map_level}.txt')

    curr_state = 0
    GAME_STATE="Menu"
    MODE_STATE="Bfs"
    running = True
    dy=0
    global screen
    run_time = 0
    while running:
        mode = MODE_STATE
        mouse_pos = pygame.mouse.get_pos()
        if GAME_STATE=="Menu":
            menu_zone()
        if GAME_STATE=="Level":
            maze = load_maze(f'{map_level}.txt')
            goal_state = load_goal_state(f'{map_level}.txt')
            level_zone(map_level,maze,mode)
        if GAME_STATE == "Not found":
            global TITLE_STATE 
            TITLE_STATE = "Not found"
            level_zone(map_level, maze,mode)
            GAME_STATE = "Level"

        if GAME_STATE=="Solve":
            curr_state=0
            problem = SokobanProblem(maze,goal_state)
            dy = 0
            if MODE_STATE=="Astar":
                res,run_time = astar(problem)
            else:
                res,run_time = BFS(problem)
            
            if res == False:
                GAME_STATE = "Not found"
            else:
                global k 
                k = res.solution()
                print(k)
                GAME_STATE="Run game"

        if GAME_STATE=="Run game":
            end_game = False
            scale_image(SCREEN_SIZE[0]/len(maze[0]),SCREEN_SIZE[0]/len(maze))

            if curr_state >= len(k):
                clock.tick(1)
                end_game = True 
                curr_state=len(k)-1
            game_init(k,maze,curr_state)
            game_init(k,maze,curr_state, dx = 700)

            if end_game:
                screen.blit(title_end,(SCREEN_SIZE[0]/2-(title_end.get_width())/2 , SCREEN_SIZE[1]-title_end.get_height()))
            curr_state += 1
        
        if screen.get_width() > SCREEN_SIZE[0] and GAME_STATE != "Run game" :
            screen = pygame.display.set_mode(SCREEN_SIZE)

        if GAME_STATE=="End game":
            end_zone(dy,run_time)
            dy+=15
            if dy>=SCREEN_SIZE[0]-140:
                dy=SCREEN_SIZE[0]-140 
        if GAME_STATE =="Mode":
            mode_zone()    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if GAME_STATE == "Run game":
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and curr_state >= len(k):
                            GAME_STATE="End game"

            if GAME_STATE == "End game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        try:
                            if return_home.collidepoint(mouse_pos):
                                GAME_STATE="Level" 
                        except:
                            continue    
            if GAME_STATE=="Level":
                if event.type == pygame.MOUSEBUTTONDOWN  or event.type == pygame.KEYDOWN:
                        if (event.type == pygame.MOUSEBUTTONDOWN and arrow_left_menu.collidepoint(mouse_pos) and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT ):
                            map_level-=1
                            TITLE_STATE = "Level"
                            if map_level == 0:
                                map_level = 1
                        if (event.type == pygame.MOUSEBUTTONDOWN and arrow_right_menu.collidepoint(mouse_pos) and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                            map_level+=1
                            TITLE_STATE = "Level"
                            if map_level > max_level:
                                map_level = max_level
                        if returnHome_button.collidepoint(mouse_pos) and event.button == 1: 
                            GAME_STATE="Menu"
                            TITLE_STATE=""

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            screen.blit(title_loading,(SCREEN_SIZE[0]/2-title_loading.get_width()/2,SCREEN_SIZE[0]-130))
                            GAME_STATE="Solve"
            if GAME_STATE == "Mode":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if bfs_mode.collidepoint(mouse_pos):
                            MODE_STATE="Bfs"
                            GAME_STATE="Level"
                        if Astar_mode.collidepoint(mouse_pos):
                            MODE_STATE="Astar"
                            GAME_STATE="Level"
            if GAME_STATE=="Menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if start_button.collidepoint(mouse_pos):
                            GAME_STATE="Level"
                        if exit_button.collidepoint(mouse_pos):
                            running = False
                        if select_mode_button.collidepoint(mouse_pos):
                            GAME_STATE = "Mode"
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
   

if __name__ == '__main__':
    load_resource()
    game_zone()