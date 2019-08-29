import pygame
import subprocess

pygame.init()

screen = pygame.display.set_mode((840,640))

class Case(pygame.sprite.Sprite):
    def __init__(self,color,co=[-1,-1],index=[0,0]):
        super(Case, self).__init__()
        self.surf = pygame.Surface((64, 64))
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
        self.surf = pygame.Surface((200, 704))
        self.color = color
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

class Pawn():
    def __init__(self,color,co_x,co_y,index):
        self.color = color
        if self.color == 'white':
            self.image = pygame.image.load('1_image\image_white_pawn.png')
        else:
            self.image = pygame.image.load('1_image\image_black_pawn.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
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
font = pygame.font.SysFont("Calibri", 20)
finish_font = pygame.font.SysFont("Calibri",25)

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
            x += 64
        y += 64
    screen.blit(right_part.surf,(640,0))

def display_pawns(pawns):
    for i in range(len(pawns[0])):
        screen.blit(pawns[0][i].image ,(64 * pawns[0][i].co_x ,64 * pawns[0][i].co_y))
    for i in range(len(pawns[1])):
        screen.blit(pawns[1][i].image ,(64 * pawns[1][i].co_x ,64 * pawns[1][i].co_y))

def mouse_case(mouse_pos):
    x = 0
    y = 0
    co_x = 0
    co_y = 0
    for i in range(10):
        x += 64
        y += 64
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
    screen.blit(text_tour,(650, 30))
    text_money = font.render('Player 1 money: ' + str(player_1.money),True,(0,0,0))
    screen.blit(text_money,(650, 60))
    text_money = font.render('Player 2 money: ' + str(player_2.money),True,(0,0,0))
    screen.blit(text_money,(650, 90))



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