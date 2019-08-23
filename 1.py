#https://www.bing.com/images/search?view=detailV2&id=68E97E71AE1C348459DEDCAC5BAA3CDEC129BBA0&thid=OIP.2vS9fzpm5QsnndvuZMrD6AHaHa&mediaurl=https%3A%2F%2Fcdn2.iconfinder.com%2Fdata%2Ficons%2Fchess-set-pieces%2F100%2FChess_Set_03-White-Classic-Bishop-512.png&exph=512&expw=512&q=pawn+transparent+png&selectedindex=17&ajaxhist=0&vt=2&eim=1,6&ccid=2vS9fzpm&simid=607992906580164786&sim=1&pivotparams=insightsToken%3Dccid_jH4jq%252F7i*mid_3ED06223DABDCF0BCD56641A86A64ED1A1893DBC*simid_608019982040106134*thid_OIP.jH4jq!_7iJIGz0PEuvwL8MwHaHa&iss=VSI
import pygame

pygame.init()

screen = pygame.display.set_mode((770,770))
class Case(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Case, self).__init__()
        self.surf = pygame.Surface((70, 70))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
running = True
enter_on = False

#color
color1 = (173,216,230)
color2 = (153,196,210)
curser_color = (113,156,170)
select_color = (93,136,150)

#pawns
white_pawn = []
black_pawn = []
for i in range(12):
    pawn = pygame.image.load('image_pawn4.png')
    pawn = pygame.transform.scale(pawn, (70, 70))
    white_pawn.append(pawn)
for i in range(24):
    pawn = pygame.image.load('image_pawn2.png')
    pawn = pygame.transform.scale(pawn, (70, 70))
    black_pawn.append(pawn)
white_pawn_placement = [[5,3],[4,4],[5,4],[6,4],[3,5],[4,5],[6,5],[7,5],[4,6],[5,6],[6,6],[5,7]]
black_pawn_placement = [[3,0],[4,0],[5,0],[6,0],[7,0],[5,1],[0,3],[0,4],[0,5],[0,6],[0,7],[1,5],[3,10],[4,10],[5,10],[6,10],[7,10],[5,9],[10,3],[10,4],[10,5],[10,6],[10,7],[9,5]]

#board
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
            x += 70
            test = not test
        y += 70

def curser_case(curser_place_x,curser_place_y,curser_color):
    global board
    global place_curser_case
    board[place_curser_case[1]][place_curser_case[0]].surf.fill(place_curser_case[2])
    screen.blit(board[place_curser_case[1]][place_curser_case[0]].surf, (70 * place_curser_case[0],70 * place_curser_case[1]))
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
    screen.blit(board[final_place_y][final_place_x].surf, (70 * final_place_x,70 * final_place_y))
    place_curser_case = [final_place_x,final_place_y,normal_color]

def select_case(curser_place_x,curser_place_y,select_color):
    global enter_on
    global board
    global place_select_case
    if enter_on:
        board[place_select_case[1]][place_select_case[0]].surf.fill(place_select_case[2])
        screen.blit(board[place_select_case[1]][place_select_case[0]].surf, (70 * place_select_case[0],70 * place_select_case[1]))
        place_select_case = [-1,0,color1]
    else:
        normal_color = board[curser_place_y][curser_place_x].surf.get_at((0,0))
        board[curser_place_y][curser_place_x].surf.fill(select_color)
        screen.blit(board[curser_place_y][curser_place_x].surf, (70 * curser_place_x, 70 * curser_place_y))
        place_select_case = [curser_place_x,curser_place_y,normal_color] 
    enter_on = not enter_on
        
def display_pawns(white_pawn_placement,white_pawn,black_pawn_placement,black_pawn):
    for i in range(len(white_pawn)):
        screen.blit(white_pawn[i],(70 * white_pawn_placement[i][0],70 * white_pawn_placement[i][1]))        
    for i in range(len(black_pawn)):
        screen.blit(black_pawn[i],(70 * black_pawn_placement[i][0],70 * black_pawn_placement[i][1]))    


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
    if pressed[pygame.K_SPACE]:
        select_case(curser_place_x,curser_place_y,select_color)
    display_pawns(white_pawn_placement,white_pawn,black_pawn_placement,black_pawn)
    clock.tick(10)
    pygame.display.flip()