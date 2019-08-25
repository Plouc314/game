#https://www.bing.com/images/search?view=detailV2&id=68E97E71AE1C348459DEDCAC5BAA3CDEC129BBA0&thid=OIP.2vS9fzpm5QsnndvuZMrD6AHaHa&mediaurl=https%3A%2F%2Fcdn2.iconfinder.com%2Fdata%2Ficons%2Fchess-set-pieces%2F100%2FChess_Set_03-White-Classic-Bishop-512.png&exph=512&expw=512&q=pawn+transparent+png&selectedindex=17&ajaxhist=0&vt=2&eim=1,6&ccid=2vS9fzpm&simid=607992906580164786&sim=1&pivotparams=insightsToken%3Dccid_jH4jq%252F7i*mid_3ED06223DABDCF0BCD56641A86A64ED1A1893DBC*simid_608019982040106134*thid_OIP.jH4jq!_7iJIGz0PEuvwL8MwHaHa&iss=VSI
import pygame

pygame.init()

screen = pygame.display.set_mode((704,704))
class Case(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Case, self).__init__()
        self.surf = pygame.Surface((64, 64))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
running = True
enter_on = False
tour = True

#color
color1 = (173,216,230)
color2 = (153,196,210)
color3 = (123,176,210)
curser_color = (113,156,170)
select_color = (93,136,150)

#pawns
white_pawn = []
black_pawn = []
king = [pygame.image.load('king5.png'),5,5]
king[0] = pygame.transform.scale(king[0], (64, 64))
for i in range(12):
    pawn = pygame.image.load('image_white_pawn1.png')
    pawn = pygame.transform.scale(pawn, (64, 64))
    white_pawn.append(pawn)
for i in range(24):
    pawn = pygame.image.load('image_black_pawn1.png')
    pawn = pygame.transform.scale(pawn, (64, 64))
    black_pawn.append(pawn)
white_pawn_placement = [[5,3],[4,4],[5,4],[6,4],[3,5],[4,5],[6,5],[7,5],[4,6],[5,6],[6,6],[5,7]]
black_pawn_placement = [[3,0],[4,0],[5,0],[6,0],[7,0],[5,1],[0,3],[0,4],[0,5],[0,6],[0,7],[1,5],[3,10],[4,10],[5,10],[6,10],[7,10],[5,9],[10,3],[10,4],[10,5],[10,6],[10,7],[9,5]]
pawn_selected = [0,0]
king_selected = None

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

def display_background(color1,color2,color3,curser_color,select_color):
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
                if test_special_case(line,column):
                    case= board[line][column]
                    case.surf.fill(color3)
                    screen.blit(case.surf, (x,y))
                else:
                    if test:
                        case = board[line][column]
                        case.surf.fill(color1)
                        screen.blit(case.surf, (x, y))
                    else:
                        case = board[line][column]
                        case.surf.fill(color2)
                        screen.blit(case.surf, (x, y))
            x += 64
            test = not test
        y += 64

def test_special_case(line,column):
    if line == 0 and (column == 0 or column == 10):
        return True
    elif line == 10 and (column == 0 or column == 10):
        return True
    elif line == 5 and column == 5:
        return True
    else:
        return False

def curser_case(curser_place_x,curser_place_y,curser_color):
    global board
    global place_curser_case
    board[place_curser_case[1]][place_curser_case[0]].surf.fill(place_curser_case[2])
    screen.blit(board[place_curser_case[1]][place_curser_case[0]].surf, (64 * place_curser_case[0],64 * place_curser_case[1]))
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
    screen.blit(board[final_place_y][final_place_x].surf, (64 * final_place_x,64 * final_place_y))
    place_curser_case = [final_place_x,final_place_y,normal_color]

def select_case(curser_place_x,curser_place_y,select_color,white_pawn_placement,black_pawn_placement):
    global enter_on
    global board
    global place_select_case
    global pawn_selected
    global tour
    if enter_on:
        print("enter off")
        if control_deplacement(curser_place_x,curser_place_y):
            board[place_select_case[1]][place_select_case[0]].surf.fill(place_select_case[2])
            screen.blit(board[place_select_case[1]][place_select_case[0]].surf, (64 * place_select_case[0],64 * place_select_case[1]))
            place_select_case = [-1,0,color1]
            print("change")
            enter_on = not enter_on
            tour = not tour
    else:
        test = 0
        print("enter on")
        if tour:
            for i in range(len(white_pawn_placement)):
                if white_pawn_placement[i][0] == curser_place_x and white_pawn_placement[i][1] == curser_place_y: 
                    pawn_selected = [0,i]
                    test = 1
            if king[1] == curser_place_x and king[2] == curser_place_y:
                king_selected = [curser_place_x,curser_place_y]
        if not tour:
            for i in range(len(black_pawn_placement)):
                if black_pawn_placement[i][0] == curser_place_x and black_pawn_placement[i][1] == curser_place_y: 
                    pawn_selected = [1,i]
                    test = 1
        if test == 1:
            normal_color = board[curser_place_y][curser_place_x].surf.get_at((0,0))
            board[curser_place_y][curser_place_x].surf.fill(select_color)
            screen.blit(board[curser_place_y][curser_place_x].surf, (64 * curser_place_x, 64 * curser_place_y))
            place_select_case = [curser_place_x,curser_place_y,normal_color] 
            enter_on = not enter_on
        
def display_pawns(white_pawn_placement,white_pawn,black_pawn_placement,black_pawn):
    for i in range(len(white_pawn)):
        screen.blit(white_pawn[i],(64 * white_pawn_placement[i][0],64 * white_pawn_placement[i][1]))        
    for i in range(len(black_pawn)):
        screen.blit(black_pawn[i],(64 * black_pawn_placement[i][0],64 * black_pawn_placement[i][1]))
    screen.blit(king[0],(64 * king[1],64 * king[2]))

def control_deplacement(curser_place_x,curser_place_y):
    global pawn_selected
    global black_pawn_placement
    global white_pawn_placement
    print(str(pawn_selected) + " pawn_selected")
    if pawn_selected[0] == 0:
        if white_pawn_placement[pawn_selected[1]][0] == curser_place_x:
            print(str( white_pawn_placement[pawn_selected[1]]) + " co-pawn_selected")
            if white_pawn_placement[pawn_selected[1]][1] == curser_place_y:
                return False
            if not control_obstacle('vertical',pawn_selected,white_pawn_placement,black_pawn_placement):
                print("vertical block")
                return False
        if white_pawn_placement[pawn_selected[1]][1] == curser_place_y:
            if white_pawn_placement[pawn_selected[1]][0] == curser_place_x:
                return False
            if not control_obstacle('horizontal',pawn_selected,white_pawn_placement,black_pawn_placement):
                print("horizontal block")
                return False
        if white_pawn_placement[pawn_selected[1]][0] == curser_place_x or white_pawn_placement[pawn_selected[1]][1] == curser_place_y:
            white_pawn_placement[pawn_selected[1]] = [curser_place_x,curser_place_y]
            return True
    if pawn_selected[0] == 1:
        if black_pawn_placement[pawn_selected[1]][0] == curser_place_x:
            if black_pawn_placement[pawn_selected[1]][1] == curser_place_y:
                return False
            if not control_obstacle('vertical',pawn_selected,white_pawn_placement,black_pawn_placement):
                print("vertical block")
                return False
        if black_pawn_placement[pawn_selected[1]][1] == curser_place_y:
            if black_pawn_placement[pawn_selected[1]][0] == curser_place_x:
                return False
            if not control_obstacle('horizontal',pawn_selected,white_pawn_placement,black_pawn_placement):
                print("horizontal block")
                return False
        if black_pawn_placement[pawn_selected[1]][1] == curser_place_y or black_pawn_placement[pawn_selected[1]][0] == curser_place_x:
            black_pawn_placement[pawn_selected[1]] = [curser_place_x,curser_place_y]
            return True
    return False

def control_obstacle(orientation,pawn_selected,white_pawn_placement,black_pawn_placement):
    if pawn_selected[0] == 0:
        if orientation == "vertical":
            if white_pawn_placement[pawn_selected[1]][1] - curser_place_y > 0:
                print("BLOCK")
                for i in range(len(white_pawn_placement)):
                    if i != pawn_selected[1]:
                        if white_pawn_placement[i][0] == white_pawn_placement[pawn_selected[1]][0] and white_pawn_placement[i][1] >= curser_place_y and white_pawn_placement[i][1] < white_pawn_placement[pawn_selected[1]][1]:
                            return False
                for i in range(len(black_pawn_placement)):
                    if i != pawn_selected[1]:
                        if black_pawn_placement[i][0] == white_pawn_placement[pawn_selected[1]][0] and black_pawn_placement[i][1] >= curser_place_y and black_pawn_placement[i][1] < white_pawn_placement[pawn_selected[1]][1]:
                            return False
            else:
                for i in range(len(white_pawn_placement)):
                    if i != pawn_selected[1]:
                        if white_pawn_placement[i][0] == white_pawn_placement[pawn_selected[1]][0] and white_pawn_placement[i][1] <= curser_place_y and white_pawn_placement[i][1] > white_pawn_placement[pawn_selected[1]][1]:
                            return False
                for i in range(len(black_pawn_placement)):
                    if i != pawn_selected[1]:
                        if black_pawn_placement[i][0] == white_pawn_placement[pawn_selected[1]][0] and black_pawn_placement[i][1] <= curser_place_y and black_pawn_placement[i][1] > white_pawn_placement[pawn_selected[1]][1]:
                            return False
        else:
            if white_pawn_placement[pawn_selected[1]][0] - curser_place_x > 0:
                for i in range(len(white_pawn_placement)):
                    if i != pawn_selected[1]:
                        if white_pawn_placement[i][1] == white_pawn_placement[pawn_selected[1]][1] and white_pawn_placement[i][0] >= curser_place_x and white_pawn_placement[i][0] < white_pawn_placement[pawn_selected[1]][0]:
                            return False
                for i in range(len(black_pawn_placement)):
                    if i != pawn_selected[1]:
                        if black_pawn_placement[i][1] == white_pawn_placement[pawn_selected[1]][1] and black_pawn_placement[i][0] >= curser_place_x and black_pawn_placement[i][0] < white_pawn_placement[pawn_selected[1]][0]:
                            return False
            else:
                for i in range(len(white_pawn_placement)):
                    if i != pawn_selected[1]:
                        if white_pawn_placement[i][1] == white_pawn_placement[pawn_selected[1]][1] and white_pawn_placement[i][0] <= curser_place_x and white_pawn_placement[i][0] > white_pawn_placement[pawn_selected[1]][0]:
                            return False
                for i in range(len(black_pawn_placement)):
                    if i != pawn_selected[1]:
                        if black_pawn_placement[i][1] == white_pawn_placement[pawn_selected[1]][1] and black_pawn_placement[i][0] <= curser_place_x and black_pawn_placement[i][0] > white_pawn_placement[pawn_selected[1]][0]:
                            return False
    else:
        if orientation == "vertical":
            if black_pawn_placement[pawn_selected[1]][1] - curser_place_y > 0:
                print("BLOCK")
                for i in range(len(white_pawn_placement)):
                    if i != pawn_selected[1]:
                        if white_pawn_placement[i][0] == black_pawn_placement[pawn_selected[1]][0] and white_pawn_placement[i][1] >= curser_place_y and white_pawn_placement[i][1] < black_pawn_placement[pawn_selected[1]][1]:
                            return False
                for i in range(len(black_pawn_placement)):
                    if i != pawn_selected[1]:
                        if black_pawn_placement[i][0] == black_pawn_placement[pawn_selected[1]][0] and black_pawn_placement[i][1] >= curser_place_y and black_pawn_placement[i][1] < black_pawn_placement[pawn_selected[1]][1]:
                            return False
            else:
                for i in range(len(white_pawn_placement)):
                    if i != pawn_selected[1]:
                        if white_pawn_placement[i][0] == black_pawn_placement[pawn_selected[1]][0] and white_pawn_placement[i][1] <= curser_place_y and white_pawn_placement[i][1] > black_pawn_placement[pawn_selected[1]][1]:
                            return False
                for i in range(len(black_pawn_placement)):
                    if i != pawn_selected[1]:
                        if black_pawn_placement[i][0] == black_pawn_placement[pawn_selected[1]][0] and black_pawn_placement[i][1] <= curser_place_y and black_pawn_placement[i][1] > black_pawn_placement[pawn_selected[1]][1]:
                            return False
        else:
            if black_pawn_placement[pawn_selected[1]][0] - curser_place_x > 0:
                for i in range(len(white_pawn_placement)):
                    if i != pawn_selected[1]:
                        if white_pawn_placement[i][1] == black_pawn_placement[pawn_selected[1]][1] and white_pawn_placement[i][0] >= curser_place_x and white_pawn_placement[i][0] < black_pawn_placement[pawn_selected[1]][0]:
                            return False
                for i in range(len(black_pawn_placement)):
                    if i != pawn_selected[1]:
                        if black_pawn_placement[i][1] == black_pawn_placement[pawn_selected[1]][1] and black_pawn_placement[i][0] >= curser_place_x and black_pawn_placement[i][0] < black_pawn_placement[pawn_selected[1]][0]:
                            return False
            else:
                for i in range(len(white_pawn_placement)):
                    if i != pawn_selected[1]:
                        if white_pawn_placement[i][1] == black_pawn_placement[pawn_selected[1]][1] and white_pawn_placement[i][0] <= curser_place_x and white_pawn_placement[i][0] > black_pawn_placement[pawn_selected[1]][0]:
                            return False
                for i in range(len(black_pawn_placement)):
                    if i != pawn_selected[1]:
                        if black_pawn_placement[i][1] == black_pawn_placement[pawn_selected[1]][1] and black_pawn_placement[i][0] <= curser_place_x and black_pawn_placement[i][0] > black_pawn_placement[pawn_selected[1]][0]:
                            return False
    return True

def control_pawn_capture():
    global white_pawn_placement
    global black_pawn_placement
    global white_pawn
    global black_pawn
    global tour
    if tour:
        white_pawn_to_delete = control_white_pawn_capture(white_pawn,black_pawn,white_pawn_placement,black_pawn_placement)
        if len(white_pawn_to_delete) != 0:
            delete_pawn('white',white_pawn_to_delete)
    else:
        black_pawn_to_delete = control_black_pawn_capture(white_pawn,black_pawn,white_pawn_placement,black_pawn_placement)
        if len(black_pawn_to_delete) != 0:
            delete_pawn('black',black_pawn_to_delete)

def delete_pawn(color,pawn_to_delete):
    global white_pawn_placement
    global black_pawn_placement
    global white_pawn
    global black_pawn
    if color == 'white':
        i = 0
        dif_i = 0
        iteration = 0
        while iteration != len(pawn_to_delete):
            i = pawn_to_delete[i]
            white_pawn.pop(i - dif_i)
            white_pawn_placement.pop(i - dif_i)
            dif_i += 1
            iteration += 1
    else:
        i = 0
        dif_i = 0
        iteration = 0
        while iteration != len(pawn_to_delete):
            i = pawn_to_delete[i]
            black_pawn.pop(i - dif_i)
            black_pawn_placement.pop(i - dif_i)
            dif_i += 1
            iteration += 1

def control_white_pawn_capture(white_pawn,black_pawn,white_pawn_placement,black_pawn_placement):
    returned = []
    for i in range(len(white_pawn_placement)):
        co_of_white_pawn = [white_pawn_placement[i][0],white_pawn_placement[i][1]]
        test_vertical = [False,False]
        test_horizontal = [False,False]
        for e in range(len(black_pawn_placement)):
            co_of_black_pawn = [black_pawn_placement[e][0],black_pawn_placement[e][1]]
            #test vertical dessus
            if co_of_white_pawn[0] == co_of_black_pawn[0] and co_of_white_pawn[1] == co_of_black_pawn[1] + 1:
                test_vertical[0] = True
            #test vertical dessous
            if co_of_white_pawn[0] == co_of_black_pawn[0] and co_of_white_pawn[1] == co_of_black_pawn[1] - 1:
                test_vertical[1] = True
            #test horizontal droite
            if co_of_white_pawn[1] == co_of_black_pawn[1] and co_of_white_pawn[0] == co_of_black_pawn[0] + 1:
                test_horizontal[0] = True
            #test horizontal gauche
            if co_of_white_pawn[1] == co_of_black_pawn[1] and co_of_white_pawn[0] == co_of_black_pawn[0] - 1:
                test_horizontal[1] = True
        if test_vertical == [True,True] or test_horizontal == [True,True]:
            returned.append(i)
    return returned

def control_black_pawn_capture(white_pawn,black_pawn,white_pawn_placement,black_pawn_placement):
    returned = []
    for i in range(len(black_pawn_placement)):
        co_of_black_pawn = [black_pawn_placement[i][0],black_pawn_placement[i][1]]
        test = 0
        for e in range(len(white_pawn_placement)):
            co_of_white_pawn = [white_pawn_placement[e][0],white_pawn_placement[e][1]]
            #test vertical dessus
            if co_of_black_pawn[0] == co_of_white_pawn[0] and co_of_black_pawn[1] == co_of_white_pawn[1] + 1:
                test += 1
            #test vertical dessous
            if co_of_black_pawn[0] == co_of_white_pawn[0] and co_of_black_pawn[1] == co_of_white_pawn[1] - 1:
                test += 1
            #test horizontal droite
            if co_of_black_pawn[1] == co_of_white_pawn[1] and co_of_black_pawn[0] == co_of_white_pawn[0] + 1:
                test += 1
            #test horizontal gauche
            if co_of_black_pawn[1] == co_of_white_pawn[1] and co_of_black_pawn[0] == co_of_white_pawn[0] - 1:
                test += 1
        if test >= 2:
            returned.append(i)
    return returned

def move_curser():
    global curser_place_x
    global curser_place_y
    test = 0
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and curser_place_y >= 1:
        curser_place_y -= 1
        test = 1
    if pressed[pygame.K_DOWN] and curser_place_y <= 9:
        curser_place_y += 1
        test = 1
    if pressed[pygame.K_LEFT] and curser_place_x >= 1:
        curser_place_x -= 1
        test = 1
    if pressed[pygame.K_RIGHT] and curser_place_x <= 9:
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
    display_background(color1,color2,color3,curser_color,select_color)
    if move_curser():
        curser_case(curser_place_x,curser_place_y,select_color)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        select_case(curser_place_x,curser_place_y,select_color,white_pawn_placement,black_pawn_placement)
    if pressed[pygame.K_BACKSPACE]:
        print("delete")
        enter_on = False
        place_select_case = [-1,0,color1]
    control_pawn_capture()
    display_pawns(white_pawn_placement,white_pawn,black_pawn_placement,black_pawn)
    clock.tick(10)
    pygame.display.flip()