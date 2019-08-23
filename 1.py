import pygame

pygame.init()

screen = pygame.display.set_mode((880,660))
class Case(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Case, self).__init__()
        self.surf = pygame.Surface((80, 60))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
running = True
enter_on = False

color1 = (173,216,230)
color2 = (153,196,210)
curser_color = (113,156,170)
select_color = (93,136,150)

board = []
place_select_case = [-1,0,select_color]
place_curser_case = [0,0,curser_color]
for line in range(11):
    board.append([])
    for column in range(11):
        case = Case(color1)
        board[line].append(case)

curser_place_x = 0
curser_place_y = 0

def display_background(color1,color2,curser_color,select_color):
    global place_curser_case
    global place_select_case
    x = 0
    y = 0
    test = True
    for line in range(11):
        x = 0
        for column in range(11):
            if line == place_curser_case[1] and column == place_curser_case[0]:
                case = board[line][column]
                case.surf.fill(curser_color)
                screen.blit(case.surf, (x, y))
            elif line == place_select_case[1] and column == place_select_case[0]:
                case = board[line][column]
                case.surf.fill(select_color)
                screen.blit(case.surf, (x, y))
            else:
                if test:
                    case = board[line][column]
                    case.surf.fill(color1)
                    screen.blit(case.surf, (x, y))
                else:
                    case = board[line][column]
                    case.surf.fill(color2)
                    screen.blit(case.surf, (x, y))
            x += 80
            test = not test
        y += 60

def curser_case(curser_place_x,curser_place_y,curser_color):
    global board
    global place_curser_case
    board[place_curser_case[1]][place_curser_case[0]].surf.fill(place_curser_case[2])
    screen.blit(board[place_curser_case[1]][place_curser_case[0]].surf, (80 * place_curser_case[0],60 * place_curser_case[1]))
    final_place_x = curser_place_x
    final_place_y = curser_place_y
    if curser_place_x > 10:
        final_place_x = 10
    if curser_place_x < 0:
        final_place_x = 0
    if curser_place_y > 10:
        final_place_y = 10
    if curser_place_y < 0:
        final_place_y = 0
    normal_color = board[final_place_y][final_place_x].surf.get_at((0,0))
    board[final_place_y][final_place_x].surf.fill(curser_color)
    screen.blit(board[final_place_y][final_place_x].surf, (80 * final_place_x,60 * final_place_y))
    place_curser_case = [final_place_x,final_place_y,normal_color]

def select_case(curser_place_x,curser_place_y,select_color):
    global enter_on
    global board
    global place_select_case
    print("selected")
    if enter_on:
        print("True")
        board[place_select_case[1]][place_select_case[0]].surf.fill(place_select_case[2])
        screen.blit(board[place_select_case[1]][place_select_case[0]].surf, (80 * place_select_case[0],60 * place_select_case[1]))
        place_select_case = [-1,0,color1]
    else:
        print("False")
        normal_color = board[curser_place_y][curser_place_x].surf.get_at((0,0))
        print(normal_color)
        board[curser_place_y][curser_place_x].surf.fill(select_color)
        screen.blit(board[curser_place_y][curser_place_x].surf, (80 * curser_place_x, 60 * curser_place_y))
        place_select_case = [curser_place_x,curser_place_y,normal_color] 
        print(place_select_case) 
    enter_on = not enter_on
        

def move_curser():
    global curser_place_x
    global curser_place_y
    test = 0
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        curser_place_y -= 1
        test = 1
    if pressed[pygame.K_DOWN]:
        curser_place_y += 1
        test = 1
    if pressed[pygame.K_LEFT]:
        curser_place_x -= 1
        test = 1
    if pressed[pygame.K_RIGHT]:
        curser_place_x += 1
        test = 1
    if test == 1:
        return True
    else: 
        return False

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
    display_background(color1,color2,curser_color,select_color)
    if move_curser():
        curser_case(curser_place_x,curser_place_y,select_color)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_BACKSPACE]:
        select_case(curser_place_x,curser_place_y,select_color)
    clock.tick(10)
    pygame.display.flip()