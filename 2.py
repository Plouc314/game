import pygame
import subprocess
from math import trunc
from time import process_time

pygame.init()

class Dimension():
    def __init__(self,input_dim):
        self.dimension = [input_dim,int(trunc(input_dim * 7/9))]
        self.dim_case = [int(trunc(self.dimension[1] / 10)),int(trunc(self.dimension[1] / 10))]
        self.dim_right_part = [int(trunc( 2 / 9 * self.dimension[0])),self.dimension[1]]
        self.dim_normal_text = int(trunc(1 / 36 * self.dimension[0]))
        self.dim_finish_text = int(trunc(7 / 180 * self.dimension[0]))
        self.dim_marge = self.dim_normal_text

dimension = Dimension(1800)
screen = pygame.display.set_mode(dimension.dimension)

class Case(pygame.sprite.Sprite):
    def __init__(self,color,co=[-1,-1],index=[0,0]):
        super(Case, self).__init__()
        self.surf = pygame.Surface(dimension.dim_case)
        self.color = color
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        self.co = co
        self.index = index
        self.income = False
        self.income_color = 0
        self.pawn_income = False
        self.free = False

class Right_part(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Right_part, self).__init__()
        self.surf = pygame.Surface(dimension.dim_right_part)
        self.color = color
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

class Pawn():
    def __init__(self,color,co_x,co_y,index):
        self.color = color
        if self.color == 'white':
            self.image = pygame.image.load('1_image/image_white_pawn.png')
        else:
            self.image = pygame.image.load('1_image/image_black_pawn.png')
        self.image = pygame.transform.scale(self.image, dimension.dim_case)
        self.co_x = co_x
        self.co_y = co_y
        self.index = index
        self.state = ['normal']
        self.moved = [False,0,0]
        self.attack = False
        self.target = False
        self.controled = False

class Tour():
    def __init__(self,tour=True,pawn_to_move=2,move_remaining=2,pawn_index=0):
        self.tour = tour
        self.pawn_to_move = pawn_to_move
        self.move_remaining = move_remaining
        self.pawn_index = pawn_index
        self.new_pawn_select = True
        self.adding_pawn = False
        self.attack_mode = False
        self.attack_index = [0,0]
        self.finish = [False,0]
    
    def control_tour_count(self):
        #when turn end
        if self.pawn_to_move == 0:
            self.tour = not self.tour
            if not self.tour:
                player_1.money += calculate_income(0) 
            else:
                player_2.money += calculate_income(1)
            self.pawn_to_move = 2
            self.move_remaining = 2
            self.new_pawn_select = True
        if self.move_remaining == 0 and self.pawn_to_move != 0:
                self.pawn_to_move -= 1
                self.move_remaining = 2
                self.new_pawn_select = True

    def control(self,coordonate,pawns):
        if tour.new_pawn_select:
            return True
        index = control_pawn(coordonate,pawns)
        if index == self.pawn_index:
            return True
    
class Player():
    def __init__(self,number_pawn):
        self.money = 0
        self.pawns_alive = number_pawn
        self.death_pawn = 0
        

#color
color1 = (173,216,230)
color2 = (153,196,210)
select_color = (93,136,150)
pawn_income_color = (200,200,70)

#text 
font = pygame.font.SysFont("Calibri", dimension.dim_normal_text)
finish_font = pygame.font.SysFont("Calibri",dimension.dim_finish_text)

#board and right part
right_part = Right_part((255,255,255))
selected_case = Case(select_color)
board = []
test = True
for line in range(10):
    board.append([])
    for column in range(10):
        if test:
            case = Case(color1)
        else:
            case = Case(color2)
        test = not test
        board[line].append(case)
    test = not test

#variable
running = True
tour = Tour()
selection = False


#pawn
pawns = [[],[]]
test = True
for a in range(2):
    index = 0
    if a == 0:
        x = 1
        y = 1
    else:
        x = 1
        y = 8
    for e in range(2):
        if e == 1 and a == 0:
            x = 0
            y = 2
        elif e == 1 and a == 1:
            x = 0
            y = 7
        for i in range(5):
            if test:
                new_pawn = Pawn('white',x,y,index)
                pawns[0].append(new_pawn)
            else:
                new_pawn = Pawn('black',x,y,index)
                pawns[1].append(new_pawn)
            x += 2
            index += 1
    test = not test

player_1 = Player(len(pawns[0]))
player_2 = Player(len(pawns[1]))


def control_pawn(coordonate,pawns):
        index = -1
        if tour.tour:
            for i in range(len(pawns[0])):
                if pawns[0][i].co_x == coordonate[0] and pawns[0][i].co_y == coordonate[1]:
                    index= i
        else:
            for i in range(len(pawns[1])):
                if pawns[1][i].co_x == coordonate[0] and pawns[1][i].co_y == coordonate[1]:
                    index = i
        return index

def display_background(board):
    x = 0
    y = 0
    for line in range(10):
        x = 0
        for column in range(10):   
            if line == selected_case.co[1] and column == selected_case.co[0]:
                screen.blit(selected_case.surf, (x,y))
            else:
                screen.blit(board[line][column].surf, (x, y))
            x += dimension.dim_case[0]
        y += dimension.dim_case[0]
    screen.blit(right_part.surf,(dimension.dimension[0] - dimension.dim_right_part[0],0))

def display_pawns(pawns):
    for i in range(len(pawns[0])):
        screen.blit(pawns[0][i].image ,(dimension.dim_case[0] * pawns[0][i].co_x ,dimension.dim_case[0] * pawns[0][i].co_y))
    for i in range(len(pawns[1])):
        screen.blit(pawns[1][i].image ,(dimension.dim_case[0] * pawns[1][i].co_x ,dimension.dim_case[0] * pawns[1][i].co_y))

def display_store(color1):
    store_white_pawn = Pawn('white',0,0,0)
    store_black_pawn = Pawn('black',0,0,0)
    case_store_1 = Case(color1)
    case_store_2 = Case(color1)
    screen.blit(case_store_1.surf,(dimension.dimension[0] - 7 / 8 * dimension.dim_right_part[0],int(trunc( 3 / 9 * dimension.dimension[1]))))
    screen.blit(store_black_pawn.image,(dimension.dimension[0] - 7 / 8 * dimension.dim_right_part[0],int(trunc( 3 / 9 * dimension.dimension[1]))))
    screen.blit(case_store_2.surf,(dimension.dimension[0] - 4 / 8 * dimension.dim_right_part[0],int(trunc( 3 / 9 * dimension.dimension[1]))))
    screen.blit(store_white_pawn.image,(dimension.dimension[0] - 4 / 8 * dimension.dim_right_part[0],int(trunc( 3 / 9 * dimension.dimension[1]))))

def mouse_case(mouse_pos):
    x = 0
    y = 0
    co_x = 0
    co_y = 0
    for i in range(10):
        x += dimension.dim_case[0]
        y += dimension.dim_case[0]
        if mouse_pos[0] >= x:
            co_x = i + 1
        if mouse_pos[1] >= y:
            co_y = i + 1
    return [co_x,co_y]
    
def select_case(mouse_pos,pawns):
    global selection
    coordonate = mouse_case(mouse_pos) 
    selected_case.co = coordonate
    if tour.control(coordonate,pawns):
        if tour.tour:
            for i in range(len(pawns[0])):
                if pawns[0][i].co_x == coordonate[0] and pawns[0][i].co_y == coordonate[1]:
                    if tour.new_pawn_select:
                        tour.pawn_index = i
                        tour.new_pawn_select = False
                    selected_case.index = [0,i]
                    selection = True
        else:
            for i in range(len(pawns[1])):
                if pawns[1][i].co_x == coordonate[0] and pawns[1][i].co_y == coordonate[1]:
                    if tour.new_pawn_select:
                        tour.pawn_index = i
                        tour.new_pawn_select = False
                    selected_case.index = [1,i]
                    tour.pawn_index = i
                    selection = True

def deselect_case():
    global selection
    selection = False
    tour.new_pawn_select = True
    selected_case.co = [-1,-1]

def move_pawn(mouse_pos):
    global selection
    global tour
    for a in range(2):
        for i in range(len(pawns[a])):
            if pawns[a][i].moved[0]:
                pawns[a][i].moved[0] = False
    coordonate = mouse_case(mouse_pos) 
    if control_deplacement(coordonate):
        pawns[selected_case.index[0]][selected_case.index[1]].moved = [True,pawns[selected_case.index[0]][selected_case.index[1]].co_x,pawns[selected_case.index[0]][selected_case.index[1]].co_y]
        pawns[selected_case.index[0]][selected_case.index[1]].co_x = coordonate[0]
        pawns[selected_case.index[0]][selected_case.index[1]].co_y = coordonate[1]
        selected_case.co = [-1,-1]
        selection = False
        tour.move_remaining -= 1
        
def control_deplacement(coordonate):
    test = False
    if coordonate[0] == selected_case.co[0] and ( coordonate[1] == selected_case.co[1] + 1 or coordonate[1] == selected_case.co[1] - 1):
        test = True
    elif coordonate[1] == selected_case.co[1] and ( coordonate[0] == selected_case.co[0] + 1 or coordonate[0] == selected_case.co[0] - 1):
        test = True
    if test:
        for i in range(len(pawns[0])):
            if pawns[0][i].co_x == coordonate[0] and pawns[0][i].co_y == coordonate[1]:
                test = False
        for i in range(len(pawns[1])):
            if pawns[1][i].co_x == coordonate[0] and pawns[1][i].co_y == coordonate[1]:
                test = False
    if test:
        return True
    else:
        return False

def control_income_case(pawns,board,pawn_income_color):
    #control new income case
    for a in range(2):
        for i in range(len(pawns[a])):
            test = 0
            pawns_incoming = [i]
            for e in range(len(pawns[a])):
                if pawns[a][i].co_x == pawns[a][e].co_x + 2 and pawns[a][i].co_y == pawns[a][e].co_y:
                    test += 1
                    pawns_incoming.append(e)
                elif pawns[a][i].co_y == pawns[a][e].co_y + 1 and pawns[a][i].co_x == pawns[a][e].co_x + 1:
                    test += 1
                    pawns_incoming.append(e)
                elif pawns[a][i].co_y == pawns[a][e].co_y - 1 and pawns[a][i].co_x == pawns[a][e].co_x + 1:
                    test += 1
                    pawns_incoming.append(e)
            if test == 3:
                co_center_case = [pawns[a][i].co_y,pawns[a][i].co_x - 1]
                board[co_center_case[0]][co_center_case[1]].income = True
                board[co_center_case[0]][co_center_case[1]].income_color = a
                board[co_center_case[0]][co_center_case[1]].surf.fill((255,255,30))
                #update Pawn.state 
                for e in range(4):
                    do = True
                    for u in range(len(pawns[a][pawns_incoming[e]].state)):
                        if pawns[a][pawns_incoming[e]].state[u] == [co_center_case[0],co_center_case[1]]:
                            do = False
                    if do:
                        pawns[a][pawns_incoming[e]].state[0] = 'incoming'
                        pawns[a][pawns_incoming[e]].state.append([co_center_case[0],co_center_case[1]]) 
                        board[pawns[a][pawns_incoming[e]].co_y][pawns[a][pawns_incoming[e]].co_x].pawn_income = True
                        board[pawns[a][pawns_incoming[e]].co_y][pawns[a][pawns_incoming[e]].co_x].surf.fill(pawn_income_color)
    #control old income case
    for line in range(10):
        for column in range(10):
            if board[line][column].income:
                surrounded = False
                for a in range(2):
                    test = 0
                    for i in range(len(pawns[a])):
                        if pawns[a][i].co_x == column + 1 and pawns[a][i].co_y == line:
                            test += 1
                        if pawns[a][i].co_x == column - 1 and pawns[a][i].co_y == line:
                            test += 1
                        if pawns[a][i].co_x == column and pawns[a][i].co_y == line + 1:
                            test += 1
                        if pawns[a][i].co_x == column and pawns[a][i].co_y == line - 1:
                            test += 1
                    if test == 4:
                        surrounded = True
                if not surrounded:
                    board[line][column].income = False
                    board[line][column].surf.fill(board[line][column].color)
                    change_pawns_incomming(pawns, board,line,column)
                                    
def change_pawns_incomming(pawns,board,line,column):
    #change Pawn.state for the surrender pawns
    for a in range(2):
        for i in range(len(pawns[a])):
            if pawns[a][i].state[0] == 'incoming':
                e = 1
                test = False
                while not test:
                    if pawns[a][i].state[e] == [line,column]:
                        pawns[a][i].state.pop(e)
                        #control 'incoming'
                        if len(pawns[a][i].state) == 1:
                            if pawns[a][i].moved[0]:
                                board[pawns[a][i].moved[2]][pawns[a][i].moved[1]].surf.fill(board[pawns[a][i].moved[2]][pawns[a][i].moved[1]].color)
                            else:
                                board[pawns[a][i].co_y][pawns[a][i].co_x].surf.fill(board[pawns[a][i].co_y][pawns[a][i].co_x].color)
                            pawns[a][i].state[0] = 'normal'
                        test = True
                        e -= 1
                    e += 1
                    if e == len(pawns[a][i].state):
                        test = True

def calculate_income(number_player):
    earned_money = 0
    for line in range(10):
        for column in range(10):
            if board[line][column].income and board[line][column].income_color == number_player:
                earned_money += 1
    return earned_money

def display_text():
    if tour.tour:
        text_tour = font.render('Turn: White',True,(0,0,0))
    else:
        text_tour = font.render('Turn: Black',True,(0,0,0))
    dim_x = dimension.dimension[0] - dimension.dim_right_part[0] + dimension.dim_marge
    screen.blit(text_tour,(dim_x, dimension.dim_marge))
    text_money = font.render('White money: ' + str(player_1.money),True,(0,0,0))
    screen.blit(text_money,(dim_x, 2 * dimension.dim_marge))
    text_money = font.render('Black money: ' + str(player_2.money),True,(0,0,0))
    screen.blit(text_money,(dim_x, 3 * dimension.dim_marge))
    text_pawn = font.render('White pawns: ' + str(player_1.pawns_alive),True,(0,0,0))
    screen.blit(text_pawn,(dim_x, 4 * dimension.dim_marge))
    text_pawn = font.render('Black pawns: ' + str(player_2.pawns_alive),True,(0,0,0))
    screen.blit(text_pawn,(dim_x, 5 * dimension.dim_marge))
    if tour.finish[0]:
        if tour.finish[1] == 0:
            text_finish = finish_font.render('White won',True,(0,0,0))
        if tour.finish[1] == 1:
            text_finish = finish_font.render('Black won',True,(0,0,0))
        screen.blit(text_finish,(dim_x, 10 * dimension.dim_marge))

def control_store(mouse_pos):
    if not tour.tour:
        if mouse_pos[0] > dimension.dimension[0] - 7 / 8 * dimension.dim_right_part[0] and mouse_pos[0] < dimension.dimension[0] - 7 / 8 * dimension.dim_right_part[0] + dimension.dim_case[0]:
            if mouse_pos[1] > int(trunc( 3 / 9 * dimension.dimension[1])) and mouse_pos[1] < int(trunc( 3 / 9 * dimension.dimension[1])) + dimension.dim_case[1]:
                if player_2.money >= 2:
                    return 2
    if tour.tour:
        if mouse_pos[0] > dimension.dimension[0] - 4 / 8 * dimension.dim_right_part[0] and mouse_pos[0] < dimension.dimension[0] - 4 / 8 * dimension.dim_right_part[0] + dimension.dim_case[0]:
            if mouse_pos[1] > int(trunc( 3 / 9 * dimension.dimension[1])) and mouse_pos[1] < int(trunc( 3 / 9 * dimension.dimension[1])) + dimension.dim_case[1]:
                if player_1.money >= 2:
                    return 1
    return 0

def add_pawns(board,color,color1,color2):
    global pawns
    if color == 1:
        for line in range(3):
            for column in range(10):
                board[line][column].free = False
                test = False
                for i in range(len(pawns[0])):
                    if pawns[0][i].co_x == column and pawns[0][i].co_y == line:
                        test = True
                if not test and not board[line][column].income:
                    board[line][column].free = True
                    if board[line][column].color == color1:
                        board[line][column].surf.fill((50,210,50))
                    else:
                        board[line][column].surf.fill((30,190,30))
    
    if color == 2:
        for line in range(3):
            for column in range(10):
                board[line + 7][column].free = False
                test = False
                for i in range(len(pawns[1])):
                    if pawns[1][i].co_x == column and pawns[1][i].co_y == line + 7:
                        test = True
                if not test and not board[line + 7][column].income:
                    board[line + 7][column].free = True
                    if board[line + 7][column].color == color1:
                        board[line + 7][column].surf.fill((50,210,50))
                    else:
                        board[line + 7][column].surf.fill((30,190,30))
    tour.adding_pawn = True

def control_add_case(board,mouse_pos,return_store):
    global pawns
    case_select = mouse_case(mouse_pos)
    if return_store == 1:
        if case_select[1] <= 2 and board[case_select[1]][case_select[0]].free and tour.adding_pawn:
            tour.adding_pawn = False
            player_1.pawns_alive += 1
            index = len(pawns[0])
            pawns[0].append(Pawn('white',case_select[0],case_select[1],index))
            player_1.money -= 2
    else:
        if case_select[1] >= 7 and board[case_select[1]][case_select[0]].free and tour.adding_pawn:
            tour.adding_pawn = False
            player_2.pawns_alive += 1
            index = len(pawns[1])
            pawns[1].append(Pawn('black',case_select[0],case_select[1],index))
            print(index)
            player_2.money -= 2

def control_free_case(board):
    for line in range(10):
        for column in range(10):
            if board[line][column].free and not board[line][column].income:
                board[line][column].surf.fill(board[line][column].color)

def reset_board_color(board,pawns,pawn_income_color):
    for line in range(10):
        for column in range(10):
            test = True
            for a in range(2):
                for i in range(len(pawns[a])):
                    if pawns[a][i].co_x == column and pawns[a][i].co_y == line:
                        if len(pawns[a][i].state) != 1:
                            test = False
            if not board[line][column].income and test:
                board[line][column].surf.fill(board[line][column].color)
            if board[line][column].pawn_income:
                board[line][column].surf.fill(pawn_income_color)

def search_target_pawn(board,pawns,selected_case):
    if tour.tour:
        player = 1
        player2 = 0
    else:
        player = 0
        player2 = 1
    ### search attack pawn
    for i in range(len(pawns[player2])):
        if pawns[player2][i].co_x == selected_case.co[0] and pawns[player2][i].co_y == selected_case.co[1]:
            tour.attack_index = [player2,pawns[player2][i].index]
    ### search target(s)
    for i in range(len(pawns[player])):
        test = False
        if pawns[player][i].co_x == selected_case.co[0] + 1 and pawns[player][i].co_y == selected_case.co[1]:
            test = True
        elif pawns[player][i].co_x == selected_case.co[0] - 1 and pawns[player][i].co_y == selected_case.co[1]:
            test = True
        elif pawns[player][i].co_x == selected_case.co[0] and pawns[player][i].co_y == selected_case.co[1] + 1:
            test = True
        elif pawns[player][i].co_x == selected_case.co[0] and pawns[player][i].co_y == selected_case.co[1] -1:
            test = True
        if test:
            pawns[player][i].target = True
            board[pawns[player][i].co_y][pawns[player][i].co_x].surf.fill((240,60,60))

def select_target(pawns,mouse_pos):
    global selected_case
    coordonate = mouse_case(mouse_pos)
    selected_case.co = coordonate
    if tour.tour:
        player = 1
    else:
        player = 0
    for i in range(len(pawns[player])):
        if pawns[player][i].co_x == coordonate[0] and pawns[player][i].co_y == coordonate[1]:
            if pawns[player][i].target:
                pawns[tour.attack_index[0]][tour.attack_index[1]].moved = [True,pawns[tour.attack_index[0]][tour.attack_index[1]].co_x,pawns[tour.attack_index[0]][tour.attack_index[1]].co_y]
                pawns[tour.attack_index[0]][tour.attack_index[1]].co_x = coordonate[0]
                pawns[tour.attack_index[0]][tour.attack_index[1]].co_y = coordonate[1] 
                pawns[player][i].target = 'confirmed'
                attack_number = search_support(pawns,tour.attack_index)
                defence_number = search_support(pawns,[player,i])
                if attack_number - defence_number <= 0:
                    attack_execution(pawns,tour.attack_index,selected_case)
                else:
                    attack_execution(pawns,[player,i],selected_case)
                return 0

def attack_execution(pawns,index,selected_case):
    global selection
    global pawn_income_color
    select_case.co = [-1,-1]
    selection = False
    if index[0] == 0:
        player_1.pawns_alive -= 1
    else:
        player_2.pawns_alive -= 1
    pawns[index[0]].pop(index[1])
    for i in range(len(pawns[index[0]]) - index[1]):
        pawns[index[0]][i + index[1]].index -= 1
    tour.attack_mode = False
    tour.new_pawn_select = True
    for a in range(2):
        for i in range(len(pawns[a])):
            pawns[a][i].target = False
            pawns[a][i].controled = False
            pawns[a][i].attack = False
            pawns[a][i].moved = [False,-1,-1]
    reset_board_color(board,pawns,pawn_income_color)

def search_support(pawns,pawn_index):
    pawn_chain = [pawns[pawn_index[0]][pawn_index[1]]]
    pawn_controled = 0
    new_pawn = []
    i = 0
    while pawn_controled != len(pawn_chain):
        if pawn_chain[i].color == 'white':
            new_pawn = control_proximity(pawns,pawn_chain[i],0)
        else:
            new_pawn = control_proximity(pawns,pawn_chain[i],1)
        pawn_chain[i].controled = True
        for a in range(len(new_pawn)):
            pawn_chain.append(new_pawn[a])
        pawn_controled += 1
        i += 1
    print(len(pawn_chain))
    return len(pawn_chain)
    
def control_proximity(pawns,pawn_to_control,player):
    returned = []
    for i in range(len(pawns[player])):
        if not pawns[player][i].controled:
            test = False
            if pawn_to_control.co_x == pawns[player][i].co_x + 1 and pawn_to_control.co_y == pawns[player][i].co_y:
                test = True
            elif pawn_to_control.co_x == pawns[player][i].co_x - 1 and pawn_to_control.co_y == pawns[player][i].co_y:
                test = True
            elif pawn_to_control.co_x == pawns[player][i].co_x and pawn_to_control.co_y == pawns[player][i].co_y + 1:
                test = True
            elif pawn_to_control.co_x == pawns[player][i].co_x and pawn_to_control.co_y == pawns[player][i].co_y - 1:
                test = True
            elif pawn_to_control.co_x == pawns[player][i].co_x + 1 and pawn_to_control.co_y == pawns[player][i].co_y + 1:
                test = True
            elif pawn_to_control.co_x == pawns[player][i].co_x - 1 and pawn_to_control.co_y == pawns[player][i].co_y - 1:
                test = True
            elif pawn_to_control.co_x == pawns[player][i].co_x - 1 and pawn_to_control.co_y == pawns[player][i].co_y + 1:
                test = True
            elif pawn_to_control.co_x == pawns[player][i].co_x + 1 and pawn_to_control.co_y == pawns[player][i].co_y - 1:
                test = True
            if test and pawns[player][i].state[0] != 'incoming':
                returned.append(pawns[player][i])
    return returned

def control_win(pawns):
    if len(pawns[0]) == 0:
        tour.finish = [True,1]
    elif len(pawns[1]) == 0:
        tour.finish = [True,0]

clock = pygame.time.Clock()

while running:
    pressed = pygame.key.get_pressed() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if not tour.adding_pawn and not tour.attack_mode and not tour.finish[0]:
                return_store = control_store(mouse_pos)
                if return_store == 1:
                    add_pawns(board, 1,color1,color2)
                elif return_store == 2:
                    add_pawns(board, 2,color1,color2)
            if not selection and not tour.finish[0]:
                select_case(mouse_pos,pawns)
            elif selection and not tour.attack_mode:
                move_pawn(mouse_pos)
            elif selection and tour.attack_mode:
                select_target(pawns,mouse_pos)
    if pressed[pygame.K_BACKSPACE]:
        deselect_case()
        tour.attack_mode = False
        tour.adding_pawn = False
        reset_board_color(board,pawns,pawn_income_color)
    if pressed[pygame.K_a] and selection:
        tour.attack_mode = True
        search_target_pawn(board,pawns,selected_case)
    display_background(board)
    display_pawns(pawns)
    display_text()
    if not tour.adding_pawn and not tour.attack_mode and not tour.finish[0]:
        display_store(color1)
        control_income_case(pawns,board,pawn_income_color)
        tour.control_tour_count()
        control_free_case(board)
    else:
        control_add_case(board,mouse_pos,return_store)
    control_win(pawns)
    clock.tick(60)
    pygame.display.flip()