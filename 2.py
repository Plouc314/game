import pygame
import subprocess
from math import trunc

pygame.init()

class Dimension():
    def __init__(self,input_dim):
        self.dimension = [input_dim,int(trunc(input_dim * 7/9))]
        self.dim_case = [int(trunc(self.dimension[1] / 10)),int(trunc(self.dimension[1] / 10))]
        self.dim_right_part = [int(trunc( 2 / 9 * self.dimension[0])),self.dimension[1]]
        self.dim_normal_text = int(trunc(1 / 36 * self.dimension[0]))
        self.dim_finish_text = int(trunc(17 / 180 * self.dimension[0]))
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

class Tour():
    def __init__(self,tour=True,pawn_to_move=2,move_remaining=2,pawn_index=0):
        self.tour = tour
        self.pawn_to_move = pawn_to_move
        self.move_remaining = move_remaining
        self.pawn_index = pawn_index
        self.new_pawn_select = True
    
    def control_tour_count(self):
        #when turn end
        if self.pawn_to_move == 0:
            self.tour = not self.tour
            if not self.tour:
                player_1.money += calculate_income(0)
            else:
                player_2.money += calculate_income(1)
            subprocess.call(['python3','support_2/buy_point.py'])
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

#text 
print(str(dimension.dim_normal_text)+ " normal")
print(str(dimension.dim_finish_text)+ " finish")
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
    
def move_pawn(mouse_pos):
    global selection
    global tour
    coordonate = mouse_case(mouse_pos) 
    if control_deplacement(coordonate):
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

def control_income_case(pawns,board):
    #control new income case
    for a in range(2):
        for i in range(len(pawns[a])):
            test = 0
            for e in range(len(pawns[a])):
                if pawns[a][i].co_x == pawns[a][e].co_x + 2 and pawns[a][i].co_y == pawns[a][e].co_y:
                    test += 1
                elif pawns[a][i].co_y == pawns[a][e].co_y + 1 and pawns[a][i].co_x == pawns[a][e].co_x + 1:
                    test += 1
                elif pawns[a][i].co_y == pawns[a][e].co_y - 1 and pawns[a][i].co_x == pawns[a][e].co_x + 1:
                    test += 1
            if test == 3:
                board[pawns[a][i].co_y][pawns[a][i].co_x - 1].income = True
                board[pawns[a][i].co_y][pawns[a][i].co_x - 1].income_color = a
                board[pawns[a][i].co_y][pawns[a][i].co_x - 1].surf.fill((255,255,30))
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

def calculate_income(number_player):
    earned_money = 0
    for line in range(10):
        for column in range(10):
            if board[line][column].income and board[line][column].income_color == number_player:
                earned_money += 1
    return earned_money

def display_text():
    if tour:
        text_tour = font.render('Turn: White',True,(0,0,0))
    else:
        text_tour = font.render('Turn: White',True,(0,0,0))
    dim_x = dimension.dimension[0] - dimension.dim_right_part[0] + dimension.dim_marge
    screen.blit(text_tour,(dim_x, dimension.dim_marge))
    text_money = font.render('Player 1 money: ' + str(player_1.money),True,(0,0,0))
    screen.blit(text_money,(dim_x, 2 * dimension.dim_marge))
    text_money = font.render('Player 2 money: ' + str(player_2.money),True,(0,0,0))
    screen.blit(text_money,(dim_x, 3 * dimension.dim_marge))



clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if not selection:
                select_case(mouse_pos,pawns)
            else:
                move_pawn(mouse_pos)
    display_background(board)
    display_pawns(pawns)
    display_text()
    control_income_case(pawns,board)
    tour.control_tour_count()
    clock.tick(60)
    pygame.display.flip()