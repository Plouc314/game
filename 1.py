#https://www.bing.com/images/search?view=detailV2&id=68E97E71AE1C348459DEDCAC5BAA3CDEC129BBA0&thid=OIP.2vS9fzpm5QsnndvuZMrD6AHaHa&mediaurl=https%3A%2F%2Fcdn2.iconfinder.com%2Fdata%2Ficons%2Fchess-set-pieces%2F100%2FChess_Set_03-White-Classic-Bishop-512.png&exph=512&expw=512&q=pawn+transparent+png&selectedindex=17&ajaxhist=0&vt=2&eim=1,6&ccid=2vS9fzpm&simid=607992906580164786&sim=1&pivotparams=insightsToken%3Dccid_jH4jq%252F7i*mid_3ED06223DABDCF0BCD56641A86A64ED1A1893DBC*simid_608019982040106134*thid_OIP.jH4jq!_7iJIGz0PEuvwL8MwHaHa&iss=VSI
import pygame
import subprocess

pygame.init()

screen = pygame.display.set_mode((1940,1540))
class Case(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Case, self).__init__()
        self.surf = pygame.Surface((140, 140))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

class Right_part(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Right_part, self).__init__()
        self.surf = pygame.Surface((400, 1540))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()


running = True
enter_on = False
tour = True
finish = False
winner = ''
launch = False

#text 
font = pygame.font.SysFont("Calibri", 50)
finish_font = pygame.font.SysFont("Calibri",70)

#color
color1 = (173,216,230)
color2 = (153,196,210)
color3 = (123,176,210)
curser_color = (113,156,170)
select_color = (93,136,150)

#pawns and king
white_pawn = []
black_pawn = []
king = [pygame.image.load('1_image/king.png'),5,5]
king[0] = pygame.transform.scale(king[0], (140, 140))
for i in range(12):
    pawn = pygame.image.load('1_image/image_white_pawn.png')
    pawn = pygame.transform.scale(pawn, (140, 140))
    white_pawn.append(pawn)
for i in range(24):
    pawn = pygame.image.load('1_image/image_black_pawn.png')
    pawn = pygame.transform.scale(pawn, (140, 140))
    black_pawn.append(pawn)
white_pawn_placement = [[5,3],[4,4],[5,4],[6,4],[3,5],[4,5],[6,5],[7,5],[4,6],[5,6],[6,6],[5,7]]
black_pawn_placement = [[3,0],[4,0],[5,0],[6,0],[7,0],[5,1],[0,3],[0,4],[0,5],[0,6],[0,7],[1,5],[3,10],[4,10],[5,10],[6,10],[7,10],[5,9],[10,3],[10,4],[10,5],[10,6],[10,7],[9,5]]
pawn_selected = [0,0]
king_selected = None
close_white_pawn = []

#board and right part
board = []
place_select_case = [-1,0,select_color]
place_curser_case = [0,0,curser_color]
for line in range(11):
    board.append([])
    for column in range(11):
        case = Case(color1)
        board[line].append(case)
right_part = Right_part((255,255,255))


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
            x += 140
            test = not test
        y += 140

def display_text(tour,white_pawn,black_pawn,winner,finish):
    global font
    global finish_font
    screen.blit(right_part.surf, (1540, 0))
    if tour:
        text_tour = font.render('Turn: White',True,(0,0,0))
    else:
        text_tour = font.render('Turn: Black',True,(0,0,0))
    screen.blit(text_tour,(1580, 50))
    text_loose_pawn = font.render('White losses: ' + str(12 - len(white_pawn)),True,(0,0,0))
    screen.blit(text_loose_pawn,(1580, 100))
    text_loose_pawn = font.render('black losses: ' + str(24 - len(black_pawn)),True,(0,0,0))
    screen.blit(text_loose_pawn,(1580, 150))
    if finish:
        text_winner = finish_font.render(str(winner) + " won",True,(0,0,0))
        screen.blit(text_winner,(1600, 400))
        text_new_game = font.render('Press escape to restart.',True,(0,0,0))
        screen.blit(text_new_game,(1550, 450))

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
    screen.blit(board[place_curser_case[1]][place_curser_case[0]].surf, (140 * place_curser_case[0],140 * place_curser_case[1]))
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
    screen.blit(board[final_place_y][final_place_x].surf, (140 * final_place_x,140 * final_place_y))
    place_curser_case = [final_place_x,final_place_y,normal_color]

def select_case(curser_place_x,curser_place_y,select_color,white_pawn_placement,black_pawn_placement):
    global enter_on
    global board
    global place_select_case
    global pawn_selected
    global tour
    global king_selected
    global king
    if enter_on:
        if king_selected != None:
            if control_king_deplacement(curser_place_x,curser_place_y,king_selected):
                king[1] = curser_place_x
                king[2] = curser_place_y
                board[place_select_case[1]][place_select_case[0]].surf.fill(place_select_case[2])
                screen.blit(board[place_select_case[1]][place_select_case[0]].surf, (140 * place_select_case[0],140 * place_select_case[1]))
                place_select_case = [-1,0,color1]
                king_selected = None
                enter_on = not enter_on
                tour = not tour
        if control_deplacement(curser_place_x,curser_place_y,king):
            board[place_select_case[1]][place_select_case[0]].surf.fill(place_select_case[2])
            screen.blit(board[place_select_case[1]][place_select_case[0]].surf, (140 * place_select_case[0],140 * place_select_case[1]))
            place_select_case = [-1,0,color1]
            enter_on = not enter_on
            tour = not tour
    else:
        test = 0
        if tour:
            for i in range(len(white_pawn_placement)):
                if white_pawn_placement[i][0] == curser_place_x and white_pawn_placement[i][1] == curser_place_y: 
                    pawn_selected = [0,i]
                    test = 1
            if king[1] == curser_place_x and king[2] == curser_place_y:
                king_selected = [curser_place_x,curser_place_y]
                test = 1
        if not tour:
            for i in range(len(black_pawn_placement)):
                if black_pawn_placement[i][0] == curser_place_x and black_pawn_placement[i][1] == curser_place_y: 
                    pawn_selected = [1,i]
                    test = 1
        if test == 1:
            normal_color = board[curser_place_y][curser_place_x].surf.get_at((0,0))
            board[curser_place_y][curser_place_x].surf.fill(select_color)
            screen.blit(board[curser_place_y][curser_place_x].surf, (140 * curser_place_x, 140 * curser_place_y))
            place_select_case = [curser_place_x,curser_place_y,normal_color] 
            enter_on = not enter_on
        
def display_pawns(white_pawn_placement,white_pawn,black_pawn_placement,black_pawn):
    for i in range(len(white_pawn)):
        screen.blit(white_pawn[i],(140 * white_pawn_placement[i][0],140 * white_pawn_placement[i][1]))        
    for i in range(len(black_pawn)):
        screen.blit(black_pawn[i],(140 * black_pawn_placement[i][0],140 * black_pawn_placement[i][1]))
    screen.blit(king[0],(140 * king[1],140 * king[2]))

def control_deplacement(curser_place_x,curser_place_y,king):
    global pawn_selected
    global black_pawn_placement
    global white_pawn_placement
    if king[1] == curser_place_x and king[2] == curser_place_y:
        return False
    if pawn_selected[0] == 0:
        if white_pawn_placement[pawn_selected[1]][0] == curser_place_x:
            if white_pawn_placement[pawn_selected[1]][1] == curser_place_y:
                return False
            if not control_obstacle('vertical',pawn_selected,white_pawn_placement,black_pawn_placement):
                return False
        if white_pawn_placement[pawn_selected[1]][1] == curser_place_y:
            if white_pawn_placement[pawn_selected[1]][0] == curser_place_x:
                return False
            if not control_obstacle('horizontal',pawn_selected,white_pawn_placement,black_pawn_placement):
                return False
        if white_pawn_placement[pawn_selected[1]][0] == curser_place_x or white_pawn_placement[pawn_selected[1]][1] == curser_place_y:
            white_pawn_placement[pawn_selected[1]] = [curser_place_x,curser_place_y]
            return True
    if pawn_selected[0] == 1:
        if black_pawn_placement[pawn_selected[1]][0] == curser_place_x:
            if black_pawn_placement[pawn_selected[1]][1] == curser_place_y:
                return False
            if not control_obstacle('vertical',pawn_selected,white_pawn_placement,black_pawn_placement):
                return False
        if black_pawn_placement[pawn_selected[1]][1] == curser_place_y:
            if black_pawn_placement[pawn_selected[1]][0] == curser_place_x:
                return False
            if not control_obstacle('horizontal',pawn_selected,white_pawn_placement,black_pawn_placement):
                return False
        if black_pawn_placement[pawn_selected[1]][1] == curser_place_y or black_pawn_placement[pawn_selected[1]][0] == curser_place_x:
            black_pawn_placement[pawn_selected[1]] = [curser_place_x,curser_place_y]
            return True
    return False

def control_king_deplacement(curser_place_x,curser_place_y,king_selected):
    global white_pawn_placement
    global black_pawn_placement
    for i in range(len(white_pawn_placement)):
        if white_pawn_placement[i][0] == curser_place_x and white_pawn_placement[i][1] == curser_place_y:
            return False
    for i in range(len(black_pawn_placement)):
        if black_pawn_placement[i][0] == curser_place_x and black_pawn_placement[i][1] == curser_place_y:
            return False
    if king_selected[0] == curser_place_x and (king_selected[1] == curser_place_y + 1 or king_selected[1] == curser_place_y - 1):
        return True
    if king_selected[1] == curser_place_y and (king_selected[0] == curser_place_x + 1 or king_selected[0] == curser_place_x - 1):
        return True
    return False

def control_king_capture(white_pawn_placement,black_pawn_placement,king):
    global finish
    global winner
    test = 0
    for i in range(len(black_pawn_placement)):
        if black_pawn_placement[i][0] == king[1] and (black_pawn_placement[i][1] == king[2] + 1 or black_pawn_placement[i][1] == king[2] - 1):
            test += 1
        elif black_pawn_placement[i][1] == king[2] and (black_pawn_placement[i][0] == king[1] + 1 or black_pawn_placement[i][0] == king[1] - 1):
            test += 1
    if test == 4:
        return True
    if control_king_case(king,white_pawn_placement,black_pawn_placement):
        if control_chain_white_pawn(white_pawn_placement,black_pawn_placement,king):
            winner = 'Black'
            finish = True

def control_king_case(king,white_pawn_placement,black_pawn_placement):
    global close_white_pawn
    case = [[king[1] + 1,king[2]],[king[1] - 1,king[2]],[king[1],king[2] + 1],[king[1],king[2] - 1]]
    close_white_pawn = []
    occuped_case = 0
    for i in range(4):
        for e in range(len(black_pawn_placement)):
            if black_pawn_placement[e][0] == case[i][0] and black_pawn_placement[e][1] == case[i][1]:
                occuped_case += 1
        for e in range(len(white_pawn_placement)):
            if white_pawn_placement[e][0] == case[i][0] and white_pawn_placement[e][1] == case[i][1]:
                close_white_pawn.append([0,white_pawn_placement[e][0],white_pawn_placement[e][1]])
                occuped_case += 1
    if occuped_case == 4:
        return True
    return False 

def control_chain_white_pawn(white_pawn_placement,black_pawn_placement,king):
    global close_white_pawn
    test = 1
    while test == 1:
        test = 0
        for i in range(len(close_white_pawn)):
            if close_white_pawn[i][0] == 0:
                test = 1
                case = [[close_white_pawn[i][1] + 1,close_white_pawn[i][2]],[close_white_pawn[i][1] - 1,close_white_pawn[i][2]],[close_white_pawn[i][1],close_white_pawn[i][2] + 1],[close_white_pawn[i][1],close_white_pawn[i][2] - 1]]
                occuped_case = 0
                for a in range(4):
                    if king[1] == case[a][0] and king[2] == case[a][1]:
                        occuped_case += 1
                    for e in range(len(black_pawn_placement)):
                        if black_pawn_placement[e][0] == case[a][0] and black_pawn_placement[e][1] == case[a][1]:
                            occuped_case += 1
                    for e in range(len(white_pawn_placement)):
                        if white_pawn_placement[e][0] == case[a][0] and white_pawn_placement[e][1] == case[a][1]:
                            test_same_pawn = 0
                            for u in range(len(close_white_pawn)):
                                if close_white_pawn[u] == [0,white_pawn_placement[e][0],white_pawn_placement[e][1]] or close_white_pawn[u] == [1,white_pawn_placement[e][0],white_pawn_placement[e][1]] :
                                    test_same_pawn = 1
                            if test_same_pawn == 0:
                                close_white_pawn.append([0,white_pawn_placement[e][0],white_pawn_placement[e][1]])
                            occuped_case += 1
                if occuped_case != 4:
                    return False
                else:
                    close_white_pawn[i][0] = 1
    return True 

def control_white_win(king):
    if king[1] == 0 and king[2] == 0:
        return True
    if king[1] == 10 and king[2] == 0:
        return True
    if king[1] == 0 and king[2] == 10:
        return True
    if king[1] == 10 and king[2] == 10:
        return True
    return False

def control_obstacle(orientation,pawn_selected,white_pawn_placement,black_pawn_placement):
    if pawn_selected[0] == 0:
        if orientation == "vertical":
            if white_pawn_placement[pawn_selected[1]][1] - curser_place_y > 0:
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
        white_pawn_to_delete = control_white_pawn_capture(white_pawn_placement,black_pawn_placement)
        if len(white_pawn_to_delete) != 0:
            delete_pawn('white',white_pawn_to_delete)
    else:
        black_pawn_to_delete = control_black_pawn_capture(white_pawn_placement,black_pawn_placement)
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

def control_white_pawn_capture(white_pawn_placement,black_pawn_placement):
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

def control_black_pawn_capture(white_pawn_placement,black_pawn_placement):
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
    display_text(tour,white_pawn,black_pawn,winner,finish)
    pressed = pygame.key.get_pressed()
    if not finish:
        if move_curser():
            curser_case(curser_place_x,curser_place_y,select_color)
        if pressed[pygame.K_SPACE]:
            select_case(curser_place_x,curser_place_y,select_color,white_pawn_placement,black_pawn_placement)
        if pressed[pygame.K_BACKSPACE]:
            enter_on = False
            place_select_case = [-1,0,color1]
        control_pawn_capture()
    display_pawns(white_pawn_placement,white_pawn,black_pawn_placement,black_pawn)
    if not finish:
        control_king_capture(white_pawn_placement,black_pawn_placement,king)
    else:
        if pressed[pygame.K_ESCAPE]:
            launch = True
    if finish and launch:
        subprocess.call(["python3.7","1.py"])
        exit()
    if control_white_win(king):
        finish = True
        winner = 'White'
    clock.tick(10)
    pygame.display.flip()