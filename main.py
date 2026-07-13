

import asyncio
import time
import pygame
import sys
import math
import random
from connect_4_ai import minimax
from connect_4_ai import winning_move
from connect_4_ai import get_valid_locations
import numpy as np


sound = 1
falling = 0
flipping = 0
play = 1
fall_speed = 0.05
random_turn = 1
chaning = 0
last_digit = '6'
number = '6'
pygame.init()
pygame.mixer.init()

random.seed()

turn = random.randint(0, 1)
win = 0
space = 4
color = (0,0,0)
text = 'Connect 4'
room = 0
act = 0


#colors 
black = (1, 1, 1)
white = (255, 255, 255)
gold = (212, 175, 55)
blue_color =(0, 56, 168)
pink_color = (214, 2, 112)
menu_color = (35, 55, 110)

# 

do_input = 1
know_flip = 1 
random_flip = 0





def create_board():
    board = np.zeros((6, 7))
    return board

# if 0 just flip y, if 6 flip y and x
h_flip = 0

mini_grid = create_board()

#window size
win_x,win_y = 640, 640

 
 #get scale
screen = pygame.display.set_mode((win_x,win_y))
pygame.display.set_caption("Connect 4")
text = 'Connect 4'
text_color = (255, 255, 255)



scale_x = win_x/7
scale_y = win_y/7

font = pygame.font.SysFont('Arial', 30)
text_surface = font.render(text, True, text_color)
text_rect = text_surface.get_rect(center=(win_x, win_y))
text_rect.center = (win_x/2, scale_y/2 - 20)

text_rect_2 = text_surface.get_rect(center=(win_x, win_y))
text_rect_2.center = (win_x/2, scale_y/2 + 20)

b_place_x = []
b_place_y = []

p_place_x = []
p_place_y = []


f_b_place_x = []
f_b_place_y = []

f_p_place_x = []
f_p_place_y = []
long = 6
next_flip = long

running = True 

grid_2 = [[0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 ]


grid = [[0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0],
 ]



b_temp_x = []
b_temp_y = []
p_temp_x = []
p_temp_y = []



p_fall = {"x": -10000, "y": -100000000000, "row": -1 }
b_fall =  {"x": -1000000, "y": -100000000, "row": -1 }
p_flip = {"x": -10000, "y": -100000000000, "row": -1 }
b_flip =  {"x": -1000000, "y": -100000000, "row": -1 }



def pretty_print_board(board):
    flipped_board = np.flipud(board)

    print("\033[0;37;41m 0 \033[0;37;41m 1 \033[0;37;41m 2 \033[0;37;41m 3 \033[0;37;41m 4 \033[0;37;41m 5 \033[0;37;41m 6 \033[0m")
    for i in flipped_board:
        row_str = ""

        for j in i:
            if j == 1:
                #print(yellow)
                row_str +="\033[0;37;43m 1 "
            elif j ==2:
                row_str +="\033[0;37;44m 2 "
            else:
                #print black
                row_str +="\033[0;37;45m   "

        print(row_str+"\033[0m")






def type_box(pos_x, pos_y, width, height, back_color, border_color, t_color, events):
    global room, running, do_input, long, number, next_flip   
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]    
    b_text = str(long)
    cen_x = width/2
    cen_y = height/2
    new_pos_x = pos_x - cen_x
    next_flip = long
    new_pos_y = pos_y - cen_y   
    pygame.draw.rect(screen, back_color, (new_pos_x, new_pos_y, width, height), 0)
    pygame.draw.rect(screen, border_color, (new_pos_x, new_pos_y, width, height), round(width * 0.05), 2)
    text_surface = font.render(b_text, True, t_color)
                  
    t_width, t_height = text_surface.get_size()
    scale_factor = min(width / t_width, height/ t_height)
    new_width = int((t_width * scale_factor) * 0.8)
    new_height = int((t_height * scale_factor) * 0.8)
    text_surface = pygame.transform.smoothscale(text_surface, (new_width, new_height))
    text_rect = text_surface.get_rect(center=(new_pos_x + cen_x, new_pos_y + cen_y))
    text_rect.center = (new_pos_x + cen_x, new_pos_y + cen_y)
    screen.blit(text_surface, text_rect)
    

    if number == '':
        long = 0
    else:
        long = int(number)
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.unicode.isnumeric():
                last_digit = event.unicode
                number += event.unicode
                
            if event.key == pygame.K_BACKSPACE:
                number = number[:-1]

        if event.type == pygame.QUIT:
            running = False






def reset():
    global grid, b_place_x, play, number, long, b_place_y, act, p_place_x, p_place_y, turn, win, grid_2, next_flip, random_turn, b_temp_x, b_temp_y, p_temp_x, p_temp_y, random_flip, know_flip
    grid_reset(grid)
    play = 1
    grid_reset(grid_2)
    b_place_x = []
    b_place_y = []
    
    b_temp_x = []
    b_temp_y = []
    turn = random.randint(0, 1)
    win = 0
    sound = 1
    falling = 0
    p_place_x = []
    p_place_y = []
    act = 0
    next_flip = long
    p_temp_x = []
    p_temp_y = []

def reset_settings():
    global long, number, next_flip, random_flip, know_flip
    long = 6
    number = str(long)
    next_flip = long
    random_flip = 0
    know_flip = 1
def grid_reset(which):
    global grid, b_place_x, b_place_y, p_place_x, p_place_y, turn, win, grid_2
    for l in range(6):
        for i in range(7):
            which[l][i] = 0


def piece_fall2(piece, collum):
    global text, turn, color, running, win, grid_2

    row = 0

    while row < 6:
        if grid_2[row][collum] == 0:
            if row == 5:
                        grid_2[row][collum] = piece

                        return row + 1
  

                        row = 7
                    
            else:
                row += 1
                
        else: 
            grid_2[row - 1][collum] = piece

            return (row )



            row = 7
#make peices fall
def piece_fall(piece, collum):
    global text, turn, color, running, win

    row = 0

    while row < 6:
        if grid[row][collum] == 0:
            if row == 5:
                        grid[row][collum] = piece

                        return row + 1
  

                        row = 7
                    
            else:
                
                row += 1
   
                
        else: 
            grid[row - 1][collum] = piece

            return (row )



            row = 7

#detect win
def win_con():
    #check if i - i+3 is equal to 1 blue wins if equal to 16 pink wins ``
    #max i =3 3 x 
    #max i = 2 y
    global text, win, color
    for k in range(6):
        for i in range(4):
            if math.prod(grid[k][i:i + 4]) == 1:
                print("blue wins H")
                text = 'Blue Wins'
                
                win = 1 
                color = blue_color                        
                    
            elif math.prod(grid[k][i:i + 4]) == 16:
                print("Pink wins H")
                text = 'Pink Wins'
                win = 1
                color = pink_color
                    
        #vertical wins

    for l in range(7):
        for i in range(3):
            vertical = [grid[i][l],  grid[i + 1][l], grid[i + 2][l], grid[i + 3][l]]
            if math.prod(vertical) == 1:
                print("blue wins V")
                text = 'Blue Wins'
                win = 1      
                color = blue_color                                 
            elif math.prod(vertical) == 16:
                print("Pink wins V")
                text = 'Pink Wins'
                win = 1
                color = pink_color
        #D wins 
    for l in range(4):
        for i in range(3):
            dia = [grid[i][l],  grid[i + 1][l + 1], grid[i + 2][l + 2], grid[i + 3][l + 3]]
            if math.prod(dia) == 1:
                print("blue wins D")
                text = 'Blue Wins'
                win = 1              
                color = blue_color               
                      
            elif math.prod(dia) == 16:
                print("Pink wins D")
                text = 'Pink Wins'
                win = 1
                color = pink_color
                
    for l in range(4):
        for i in range(3,6):
            dia2 = [grid[i][l],  grid[i - 1][l + 1], grid[i - 2][l + 2], grid[i - 3][l + 3]]
            if math.prod(dia2) == 1:
                print("blue wins D")
                text = 'Blue Wins'
                win = 1              
                color = blue_color                   
                      
            elif math.prod(dia2) == 16:
                print("Pink wins D")
                text = 'Pink Wins'
                win = 1
                color = pink_color

    if math.prod(grid[0])> 0:
        text = 'Tie'
        
    return win 


#load images 
def load_images(pic, buffer):
    img = pygame.image.load('assets\\' + pic).convert_alpha()
    img = pygame.transform.scale(img, (scale_x - buffer , scale_y - buffer))    

    return img 
 
 
border_img = load_images('4_border.png', 0)
blue_img = load_images('4_blue.png', space)   
pink_img = load_images('4_pink.png', space)

border_x = []
border_y = []

#tie detection
 


for i in range(7):
    for k in range(7):
        border_x.append(i * scale_x)
        border_y.append(k * scale_y)


fall_sound = pygame.mixer.Sound('assets\\fall_sound.ogg')
click_sound = pygame.mixer.Sound('assets\\click_sound.ogg')
win_sound = pygame.mixer.Sound('assets\\win_sound.ogg')

win = 0





def main_game_player(events):
    global text,ani, sound, b_flip, p_flip, falling, turn, color, flipping, pink, running,p_fall, win, act, b_fall, do_input, b_place_x, b_place_y, next_flip, long, b_temp_x, b_temp_y, p_temp_x, p_temp_y

    if win == 1 and sound == 1:
        win_sound.play()
        sound = 0

        
    b_fall["y"] += fall_speed * scale_x
    p_fall["y"] += fall_speed * scale_x
    
    
    b_flip["y"] += fall_speed * scale_x
    p_flip["y"] += fall_speed * scale_x
    if len(b_temp_y) > 0:
            if b_flip["x"] < -100:
                b_flip = {"x": b_temp_x[0], "y": 0, "row": b_temp_y[0] }
                b_temp_x.pop(0)
                b_temp_y.pop(0)
                flipping = 0

    if len(p_temp_y):
        flipping = 0
        print("e")
        if p_flip["x"] < -100:
            p_flip = {"x": p_temp_x[0], "y": 0, "row": p_temp_y[0] }
            p_temp_x.pop(0)
            p_temp_y.pop(0)
            flipping = 0

    
    if b_fall ["y"] >= b_fall["row"]:
        b_fall["y"] = b_fall["row"]
        turn = 0
        next_flip -= 1
        b_place_x.append(b_fall["x"])
        b_place_y.append(b_fall["y"])

        b_fall["x"] = -10000
        b_fall["y"] = -1000000
        fall_sound.play()
        win = win_con()
        falling = 0
        pink = 1

    if p_fall ["y"] >= p_fall["row"]:
        p_fall["y"] = p_fall["row"]
        turn = 1
        next_flip -= 1
        p_place_x.append(p_fall["x"])
        p_place_y.append(p_fall["y"]) 
        p_fall["x"] = -10000
        p_fall["y"] = -1000000
        fall_sound.play()
        pink = 0
        win = win_con()
        falling = 0
    
    if b_flip ["y"] >= b_flip ["row"]:
        b_flip["y"] = b_flip ["row"]

        b_place_x.append(b_flip ["x"])
        b_place_y.append(b_flip ["y"])

        b_flip["x"] = -10000
        b_flip["y"] = -1000000
        fall_sound.play()
        win = win_con()
        if len(p_temp_x) < 1 and len(b_temp_x) < 1 and b_flip["x"] < 0 and p_flip["x"] < 0:
            falling = 0

    if p_flip ["y"] >= p_flip["row"]:
        p_flip["y"] = p_flip["row"]

        p_place_x.append(p_flip["x"])
        p_place_y.append(p_flip["y"]) 
        p_flip["x"] = -10000
        p_flip["y"] = -1000000
        fall_sound.play()
        win = win_con()
        if len(p_temp_x) < 1 and len(b_temp_x) < 1 and b_flip["x"] < 0 and p_flip["x"] < 0:
            falling = 0
        
    
    
    if len(b_temp_x) > 0 or len(p_temp_x) > 0:
        falling = 1



    if next_flip == 0:
        do_input = 0
        time.sleep(0.05)
        
        grid_flip()
        win = win_con()
        if random_flip == 1:
            next_flip = random.randint(1, 6)
        else:
            next_flip = long
        
    if do_input == 0:
        do_input = 1
        return
    if math.prod(grid[0])> 0:
        text = 'Tie'
    screen.fill((204,196,18))
    pygame.draw.rect(screen, color, (0, 0, win_x, scale_y), 0)
    if know_flip == 1:
        make_text("Turns until next flip: " + str(next_flip), win_x/2, scale_y/2 + 20, white)
    make_text(text, win_x/2, scale_y/2 - 20, white)
    menu_button(25, 12.5, 50, 25, "Back", 0, black, white, events, white)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    mouse_collum = float(mouse_x/scale_x)
    mouse_collum = math.floor(mouse_collum)

    
    #switch between turns
    if win == 0:
        if turn == 1: 
            target = 1 #b
            text = 'Blue Turn'
            color = blue_color
            #timer(current_time, time_passed)

        else: 
            text = 'Pink Turn'
            target = 2
            color = pink_color
    #place images on screen    
    for i in range(len(border_x)):
        screen.blit(border_img, (border_x[i], border_y[i] + scale_x))
    if turn == 1:
        screen.blit(blue_img, (mouse_collum *  scale_x, scale_y - 50))
    else:
        screen.blit(pink_img, (mouse_collum *  scale_x, scale_y - 50))
    if len(b_place_y) > 0:
        for i in range(len(b_place_y)):
    
            screen.blit(blue_img, (b_place_x[i], b_place_y[i]))
    for i in range(len(p_place_y)):
        screen.blit(pink_img, (p_place_x[i], p_place_y[i]))
    #animate falling 

    screen.blit(blue_img, (b_fall["x"], b_fall["y"]))
    screen.blit(pink_img, (p_fall["x"], p_fall["y"]))

    screen.blit(blue_img, (b_flip["x"], b_flip["y"]))
    screen.blit(pink_img, (p_flip["x"], p_flip["y"]))
    pygame.display.flip()


       
        
       
   

                
    
    
    for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if win == 0:
                    if event.button == 1 and mouse_y > 25 and falling == 0:
                        act = 1

                        #detrime what column mouse is in

                        
                        #place piece in correct column
                        row = piece_fall(target, mouse_collum)

                        place_x = mouse_collum * scale_x 
                        place_y = row * scale_y 
                        if row > 0:
                            
                            falling = 1
                            if turn == 0:
                                
                                p_fall = {"x": place_x, "y": 0, "row": place_y }
                                do_input = 0
                                

                            else: 
                                b_fall = {"x": place_x, "y": 0, "row": place_y }
                                do_input = 0


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    #print(grid)
                    matrix = np.array(grid)
                    matrix = matrix[::-1]
                    pretty_print_board(matrix)
                if event.key == pygame.K_g:
                    print("no more debugging for you")
   
                    


def main_game_ai(events, depth):
    global text, falling, sound, b_flip,p_flip,flipping, turn,b_fall, play, p_fall, color, running, win, do_input, b_place_x, b_place_y, act, next_flip, long

    if win == 1 and sound == 1:
        win_sound.play()
        sound = 0

        
    b_fall["y"] += fall_speed * scale_x
    p_fall["y"] += fall_speed * scale_x
    
    
    b_flip["y"] += fall_speed * scale_x
    p_flip["y"] += fall_speed * scale_x
    if len(b_temp_y) > 0:
            print("e")
            if b_flip["x"] < -100:
                b_flip = {"x": b_temp_x[0], "y": 0, "row": b_temp_y[0] }
                b_temp_x.pop(0)
                b_temp_y.pop(0)
                flipping = 0

    if len(p_temp_y):
        flipping = 0
        print("e")
        if p_flip["x"] < -100:
            p_flip = {"x": p_temp_x[0], "y": 0, "row": p_temp_y[0] }
            p_temp_x.pop(0)
            p_temp_y.pop(0)
            flipping = 0

    
    if b_fall ["y"] >= b_fall["row"]:
        b_fall["y"] = b_fall["row"]
        turn = 0
        next_flip -= 1
        b_place_x.append(b_fall["x"])
        b_place_y.append(b_fall["y"])

        b_fall["x"] = -10000
        b_fall["y"] = -1000000
        fall_sound.play()
        win = win_con()
        falling = 0
        pink = 1

    if p_fall ["y"] >= p_fall["row"]:
        p_fall["y"] = p_fall["row"]
        turn = 1
        next_flip -= 1
        p_place_x.append(p_fall["x"])
        p_place_y.append(p_fall["y"]) 
        p_fall["x"] = -10000
        p_fall["y"] = -1000000
        fall_sound.play()
        pink = 0
        win = win_con()
        falling = 0
    
    if b_flip ["y"] >= b_flip ["row"]:
        b_flip["y"] = b_flip ["row"]

        b_place_x.append(b_flip ["x"])
        b_place_y.append(b_flip ["y"])

        b_flip["x"] = -10000
        b_flip["y"] = -1000000
        fall_sound.play()
        win = win_con()
        if len(p_temp_x) < 1 and len(b_temp_x) < 1 and b_flip["x"] < 0 and p_flip["x"] < 0:
            falling = 0

    if p_flip ["y"] >= p_flip["row"]:
        p_flip["y"] = p_flip["row"]

        p_place_x.append(p_flip["x"])
        p_place_y.append(p_flip["y"]) 
        p_flip["x"] = -10000
        p_flip["y"] = -1000000
        fall_sound.play()
        win = win_con()
        if len(p_temp_x) < 1 and len(b_temp_x) < 1 and b_flip["x"] < 0 and p_flip["x"] < 0:
            falling = 0
        
    
    
    if len(b_temp_x) > 0 or len(p_temp_x) > 0:
        falling = 1




        
    if next_flip == 0:
        do_input = 0
        time.sleep(0.05)
        
        grid_flip()
        win = win_con()
        if random_flip == 1:
            next_flip = random.randint(1, 6)
        else:
            next_flip = long
        
    if do_input == 0:
        do_input = 1
        return
    if math.prod(grid[0])> 0:
        text = 'Tie'
    text_surface = font.render(text, True, text_color)
    screen.fill((204,196,18))
    pygame.draw.rect(screen, color, (0, 0, win_x, scale_y), 0)
    
    menu_button(25, 12.5, 50, 25, "Back", 2, black, white, events, white)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    mouse_collum = float(mouse_x/scale_x)
    mouse_collum = math.floor(mouse_collum)
    
    if turn == 0 and falling < 0 and st == 0:
        play == 1

    
    #switch between turns
    if win == 0:
        if turn == 1: 
            target = 1 #b


            text = 'Blue Turn'
            color = (0, 56, 168)
            #timer(current_time, time_passed)

        else: 
            text = 'Pink Turn'

            target = 2
            color = (214, 2, 112)
            matrix = np.array(grid[::-1])

            if falling == 0:
                collumn = minimax(matrix, depth,  -math.inf, math.inf, True, next_flip, know_flip)   
                score = collumn[1]
                collumn = collumn[0]
                print(collumn) 
                if collumn == None or score == 0:
                    collumn = random.randint(0, 6)
                row = piece_fall(target, collumn)
                place_x = collumn * scale_x 
                place_y = row * scale_y  
                p_fall = {"x": place_x, "y": 0, "row": place_y }
                falling = 1
                play = 0
            act = 1
            play = 0
    #place images on screen   

    for i in range(len(border_x)):
                screen.blit(border_img, (border_x[i], border_y[i] + scale_x))
    if turn == 1:
        screen.blit(blue_img, (mouse_collum *  scale_x, scale_y - 50))
    if len(b_place_y) > 0:
        for i in range(len(b_place_y)):
            screen.blit(blue_img, (b_place_x[i], b_place_y[i]))
    for i in range(len(p_place_y)):
        screen.blit(pink_img, (p_place_x[i], p_place_y[i]))
    screen.blit(pink_img, (p_fall["x"], p_fall["y"]))
    screen.blit(blue_img, (b_fall["x"], b_fall["y"]))
    
    screen.blit(pink_img, (p_flip["x"], p_flip["y"]))
    screen.blit(blue_img, (b_flip["x"], b_flip["y"]))


    if know_flip == 1:
        make_text("Turns until next flip: " + str(next_flip), win_x/2, scale_y/2 + 20, white)
    make_text(text, win_x/2, scale_y/2 - 20, white)
   
        
    pygame.display.flip()


    

                
    
    
    for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if win == 0:
                    if event.button == 1 and mouse_y > 25 and falling == 0:

                        act = 1

                        
                        #place piece in correct column
                        row = piece_fall(target, mouse_collum)
                        place_x = mouse_collum * scale_x 
                        place_y = row * scale_y 
                        if row > 0:
                            
                            
                            if turn == 0:
                                
                                
                                

                               pass
                            else: 
                                b_fall = {"x": place_x, "y": 0, "row": place_y }
                                falling = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    #print(grid)
                    matrix = matrix = np.array(grid[::-1])
                    pretty_print_board(matrix)
                    print(math.prod(grid[0][0:9]))
                if event.key == pygame.K_g:
                    matrix = matrix = np.array(grid[::-1])
                    print(get_valid_locations(matrix))
   
                    
def main_menu(events):
    
    global text, turn, color, running, win, screen, do_input, grid, grid_start
    if do_input == 0:
        do_input = 1
        return
    screen.fill(menu_color)
    make_text("Connect 4: Flip", win_x/2, win_y/3 - 180, white)

    if act == 1:
        reset_color = (255, 15, 15)
    else:
        reset_color = black
           
    menu_button(win_x/2, win_y/3, 200, 100, "Player Vs Player", 1, black, white, events, white)
    menu_button(win_x/2, win_y/3 + 150, 200, 100, "Player Vs AI", 2, black, white, events, white)
    menu_button(win_x/2, win_y/3 + 300, 200, 100, "Settings", 7, black, white, events, white)
    menu_button(50, 25, 100, 50, "Reset", 6, reset_color, white, events, white)

    pygame.display.flip()


def main_menu_settings(events):

    global text, turn, color, running, win, screen, do_input, know_flip, random_flip
    
    

    if know_flip == 1:
        know_flip_color = (40, 160, 60)
    else:
        know_flip_color = (255, 0, 0)
    
    if random_flip == 1:
        random_flip_color = (40, 160, 60)
    else:
        random_flip_color = (255, 0, 0)

    if do_input == 0:
        do_input = 1
        return
    screen.fill(menu_color)
    make_text("Settings", win_x/2, win_y/3 - 150, white)
    make_text("Flip Interval = Amount of Turns Between Flips", win_x/2, win_y/3 - 100, white)

    if chaning == 1:
        type_box(win_x/2, win_y/2, 200, 100, black, white, white, events)
        menu_button(50, 25, 100, 50, "Back", 10, black, white, events, white)
    else:
        menu_button(50, 25, 100, 50, "Back", 0, black, white, events, white)
        menu_button(win_x - 50, win_y - 25, 100, 50, "Default settings", 11, black, white, events, white)
        menu_button(win_x/2, win_y/3, 200, 100, "Show flip countdown", 8, know_flip_color, white, events, white)
        menu_button(win_x/2, win_y/3 + 150, 200, 100, "Random Flip Interval", 9, random_flip_color, white, events, white)
        if random_flip == 0:
            menu_button(win_x/2, win_y/3 + 300, 200, 100, "Change Flip Interval", 10, black, white, events, white)    
    pygame.display.flip()

    
def main_menu_dif(events):

    global text, turn, color, running, win, screen, do_input
    
    if do_input == 0:
        do_input = 1
        return
    screen.fill(menu_color)
    menu_button(50, 25, 100, 50, "Back", 0, black, white, events, white)
    menu_button(win_x/2, win_y/3, 200, 100, "Easy", 3, black, white, events, white)
    menu_button(win_x/2, win_y/3 + 150, 200, 100, "Normal", 4, black, white, events, white)
    menu_button(win_x/2, win_y/3 + 300, 200, 100, "Hard", 5, black, white, events, white)
    pygame.display.flip()




def make_text(text, pos_x, pos_y, t_color):
    global screen, font
    cen_x = pos_x/2
    cen_y = pos_y/2
    text_surface = font.render(text, True, t_color)
    text_rect = text_surface.get_rect(center=(pos_x, pos_y ))
    text_rect.center = (pos_x, pos_y)
    screen.blit(text_surface, text_rect)

def menu_button(pos_x, pos_y, width, height, b_text, room_num, back_color, t_color, events, border_color):
    global room, running, do_input   
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]    
    
    cen_x = width/2
    cen_y = height/2
    new_pos_x = pos_x - cen_x
    if mouse_x >= new_pos_x and mouse_x <= new_pos_x + width and mouse_y >= pos_y - cen_y and mouse_y <= pos_y + cen_y:
      new_pos_y= (pos_y - cen_y) - 5
      back_color = tuple(min(255, x + 40) for x in back_color)
    else:
        new_pos_y = pos_y - cen_y   
    pygame.draw.rect(screen, back_color, (new_pos_x, new_pos_y, width, height), 0)
    pygame.draw.rect(screen, border_color, (new_pos_x, new_pos_y, width, height), round(width * 0.05), 2)
    text_surface = font.render(b_text, True, t_color)
                  
    t_width, t_height = text_surface.get_size()
    scale_factor = min(width / t_width, height/ t_height)
    new_width = int((t_width * scale_factor) * 0.8)
    new_height = int((t_height * scale_factor) * 0.8)
    text_surface = pygame.transform.smoothscale(text_surface, (new_width, new_height))
    text_rect = text_surface.get_rect(center=(new_pos_x + cen_x, new_pos_y + cen_y))
    text_rect.center = (new_pos_x + cen_x, new_pos_y + cen_y)
    screen.blit(text_surface, text_rect)
    

  
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and do_input == 1:
            if event.button == 1:
                if mouse_x >= new_pos_x and mouse_x <= new_pos_x + width and mouse_y >= new_pos_y and mouse_y <= new_pos_y + height:
                        click_sound.play()
                        time.sleep(0.05)
                        room = room_num
                        do_input = 0
        if event.type == pygame.QUIT:
            running = False



def grid_flip():
    global grid, b_place_x, b_place_y, p_place_x, p_place_y, grid_2, b_fall, p_fall, flipping
    
    #clear out old visuals 
    b_place_x = []
    b_place_y = []
    
    p_place_x = []
    p_place_y = []
    for i in range(6, -1, -1):
        for l in range(6): 
            if grid[l][i] == 1:
                row_2 = piece_fall2(1, abs(h_flip - i)) 
                
                b_temp_x.append(abs((h_flip - i)) * scale_x)
                b_temp_y.append(row_2 * scale_y)
                print(b_temp_y)
                #b_place_x.append(abs((h_flip - i)) * scale_x)
                #b_place_y.append(row_2 * scale_y)
            elif grid[l][i] == 2:
                row_2 = piece_fall2(2, abs(h_flip- i)) 
                #p_place_x.append(abs((h_flip - i)) * scale_x)
                #p_place_y.append(row_2 * scale_y)
                
                p_temp_x.append(abs((h_flip - i)) * scale_x)
                p_temp_y.append(row_2 * scale_y)
                            
     #make the main grid match the temp grid
    for l in range(6):
        for i in range(7):
            grid[l][i] = grid_2[l][i]
            
    #clear the temp grid
    grid_reset(grid_2)
    
async def main():
    global sound, running, falling, flipping, play, fall_speed, random_turn, chaning, last_digit, number, turn, win, space, color, text, room, act, black, white, gold, blue_color, pink_color, menu_color, do_input, know_flip, random_flip
    running = True  
        

    while running:    
        events = pygame.event.get()             
        
        #output of button presses 
        if room == 0:
            main_menu(events)
        if room == 1:
            main_game_player(events)
        if room == 2:
            main_menu_dif(events)
        if room == 3:
            main_game_ai(events, 2)
        if room == 4:
            main_game_ai(events, 5)
        if room == 5:
            main_game_ai(events, 6)
        if room == 6:
            #rest grid
            reset()
            print("reset")
            room = 0
        if room == 7:
            main_menu_settings(events) 
        if room == 8:
            if know_flip == 1:
                know_flip = 0
            else:
                know_flip = 1
            room = 7
        if room == 9:
            if random_flip == 1:
                random_flip = 0
            else:
                random_flip = 1
            room = 7
        if room == 10:
            if chaning == 1:
                chaning = 0
            else:
                chaning = 1
            room = 7
        if room == 11:
            reset_settings()
            room = 7
        await asyncio.sleep(0) 
    pygame.QUIT 

asyncio.run(main())

