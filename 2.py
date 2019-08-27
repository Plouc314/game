import pygame
import subprocess

pygame.init()

screen = pygame.display.set_mode((840,640))
class Case(pygame.sprite.Sprite):
    def __init__(self,color,co=[0,0]):
        super(Case, self).__init__()
        self.surf = pygame.Surface((64, 64))
        self.color = color
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        self.co = co

class Right_part(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Right_part, self).__init__()
        self.surf = pygame.Surface((200, 704))
        self.color = color
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

class Pawn():
    def __init__(self,color,co_x,co_y):
        self.color = color
        if self.color == 'white':
            self.image = pygame.image.load('1_image\image_white_pawn.png')
        else:
            self.image = pygame.image.load('1_image\image_black_pawn.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.co_x = co_x
        self.co_y = co_y

#color
color1 = (173,216,230)
color2 = (153,196,210)
select_color = (93,136,150)

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
tour = True

#pawn
pawns = [[],[]]
test = True
for a in range(2):
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
                new_pawn = Pawn('white',x,y)
                pawns[0].append(new_pawn)
            else:
                new_pawn = Pawn('black',x,y)
                pawns[1].append(new_pawn)
            x += 2
    test = not test


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
        screen.blit(pawns[1][i].image ,(64 * pawns[0][i].co_x ,64 * pawns[1][i].co_y))

def select_case(mouse_pos):
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
    selected_case.co = [co_x,co_y]
    




clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            select_case(mouse_pos)
    display_background(board)
    display_pawns(pawns)
    clock.tick(60)
    pygame.display.flip()