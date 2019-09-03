import pygame
from math import trunc
from math import ceil

pygame.init()

class Dimension():
    def __init__(self,input_dim):
        self.dimension = [input_dim,int(trunc(input_dim * 7/9))]
        self.dim_normal_text = int(trunc(1 / 16 * self.dimension[0]))
        self.dim_button = [int(trunc(3 / 20 * self.dimension[0])),int(trunc(3 / 40 * self.dimension[0]))]

dimension = Dimension(800)

screen = pygame.display.set_mode(dimension.dimension)

class Background(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Background, self).__init__()
        self.surf = pygame.Surface((dimension.dimension[0], dimension.dimension[1]))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

class Button(pygame.sprite.Sprite):
    def __init__(self,color):
        super(Button, self).__init__()
        self.surf = pygame.Surface(dimension.dim_button)
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()

#text 
font = pygame.font.SysFont("Calibri", dimension.dim_normal_text)

background = Background((255,255,255))
#button_yes = Button((170,210,230))
#button_no = Button((170,210,230))
running = True

#money
file = open('support_2/money.txt')
content = file.read().split(" ")
content[1] = int(content[1])
file.close()

def display_background():
    screen.blit(background.surf,(0,0))
    text_how_many = font.render('How many pawns do you want to add?',True,(0,0,0))
    if content[1] > 19:
        max_add = 9
    else:
        max_add = int(ceil(content[1] / 2 - 0.5))
    text_under = font.render('Press a number (max ' + str(max_add) + "):",True,(0,0,0))
    screen.blit(text_how_many,(int(trunc(1 / 16 * dimension.dimension[0])),int(trunc(1 / 16 * dimension.dimension[0]))))
    screen.blit(text_under,(int(trunc(1 / 16 * dimension.dimension[0])),int(trunc(2 / 16 * dimension.dimension[0]))))

    #text_ask = font.render('Want you to add one/several pawn(s)?',True,(0,0,0))
    #screen.blit(text_ask,(int(trunc(1 / 16 * dimension.dimension[0])),int(trunc(1 / 16 * dimension.dimension[0]))))
    #screen.blit(button_yes.surf, (int(trunc(1 / 16 * dimension.dimension[0])), int(trunc(4 / 16 * dimension.dimension[0]))))
    #text_yes = font.render('Yes',True,(0,0,0))
    #screen.blit(text_yes,(int(trunc(9 / 100 * dimension.dimension[0])),int(trunc(107 / 400 * dimension.dimension[0]))))
    #screen.blit(button_no.surf, (int(trunc(11 / 16 * dimension.dimension[0])), int(trunc(4 / 16 * dimension.dimension[0]))))
    #text_yes = font.render('No',True,(0,0,0))
    #screen.blit(text_yes,(int(trunc(73 / 100 * dimension.dimension[0])),int(trunc(107 / 400 * dimension.dimension[0]))))

#def display_add_pawns(content):
    
#def control_mouse(mouse_pos):
#    if mouse_pos[0] > int(trunc(1 / 16 * dimension.dimension[0])) and mouse_pos[0] < (int(trunc(1 / 16 * dimension.dimension[0])) + dimension.dim_button[0]):
#        if mouse_pos[1] > int(trunc(4 / 16 * dimension.dimension[0])) and mouse_pos[1] < (int(trunc(4 / 16 * dimension.dimension[0])) + dimension.dim_button[1]):
#            return 'Yes'
#    if mouse_pos[0] > int(trunc(11 / 16 * dimension.dimension[0])) and mouse_pos[0] < (int(trunc(11 / 16 * dimension.dimension[0])) + dimension.dim_button[0]):
#        if mouse_pos[1] > int(trunc(4 / 16 * dimension.dimension[0])) and mouse_pos[1] < (int(trunc(4 / 16 * dimension.dimension[0])) + dimension.dim_button[1]):
#            return 'No'
#    return False

def control_number(pressed,max):
    number = False
    if pressed[pygame.K_1] and max >= 1:
        number = 1
    elif pressed[pygame.K_2] and max >= 2:
        number = 2
    elif pressed[pygame.K_3] and max >= 3:
        number = 3
    elif pressed[pygame.K_4] and max >= 4:
        number = 4
    elif pressed[pygame.K_5] and max >= 5:
        number = 5
    elif pressed[pygame.K_6] and max >= 6:
        number = 6
    elif pressed[pygame.K_7] and max >= 7:
        number = 7
    elif pressed[pygame.K_8] and max >= 8:
        number = 8
    elif pressed[pygame.K_9] and max >= 9:
        number = 9
    if number != False:
        return [True,number]
    else:
        return [False,0]
    
    


while running:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
            file = open('support_2/inter.txt','w')
            file.write('None')
            file.close()
            running = False
    display_background()
    returned = control_number(pressed,int(ceil(content[1] / 2 - 0.5)))
    if returned[0]:
        file = open('support_2/inter.txt','w')
        file.write(str(content[0]) + " " + str(returned[1]))
        file.close()
        running = False
    pygame.display.flip()