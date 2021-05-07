import pygame, sys
from pygame.locals import *
from pygame import *
import time
import serial

pygame.init()

display_width = 800
display_height = 600


gameDisplay = pygame.display.set_mode((800,600), 0, 32) #0, 32?
pygame.display.set_caption('this is an ongoing art project')

clock = pygame.time.Clock()

#colors
black = (0,0,0)
white = (255,255,255)
lightBlue = (106, 178, 201)
lightGreen = (88, 159, 88)
lightPink = (243, 201, 236)
gold = (216, 193, 41)

# last_pos = None
mouse_position = (0, 0)
# drawing = False

crashed = False

gameDisplay.fill(white)

#all images
starMousePic = pygame.image.load('img/cuteSmallStar.png')
star_width = 40

cursedPic = pygame.image.load("img/face.png") #this looks too creepy :(
circlePic = pygame.image.load("img/circle.png")
moonPic = pygame.image.load("img/pinkmoon.png")
dogPic = pygame.image.load("img/doggy.png")

PlayerChosenImage = 0

spaceBackground = pygame.image.load("img/space.png")
dogParkBackground = pygame.image.load("img/dogPark.png")

def chosenIMG(img,x,y):
    gameDisplay.blit(img, (x,y))
    # gameDisplay.mouse.set_cursor() #set the cursor to the image of the star

x =  (display_width * 0.45)
y = (display_height * 0.8)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

#intro to the "game"?
def project_intro():
    # print(pygame.font.get_fonts())
    intro = True
    while intro:
        # print(mspserial.in_waiting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if mspserial.in_waiting > 0:
            if "down" in str(mspserial.readline()):
                # print('choose image done')
                choose_img()


        #background: cup
        gameDisplay.fill(white)
        background = pygame.image.load('img/cup2.png')
        gameDisplay.blit(background, (0, 0))
        
        largeText = pygame.font.Font('freesansbold.ttf',30)
        subtitleText = pygame.font.Font('freesansbold.ttf',20)

        # text = font.render ("Hello!", True, (white))

        TextSurf, TextRect = text_objects("This is an ongoing art project", largeText, white)
        text2, textRect2 = text_objects("--inspired by my love of chaos in art--", subtitleText, white)
        text3, textRect3 = text_objects("press 'down' to begin!", largeText, white)

        TextRect.center = ((display_width/2),(display_height/3))
        textRect2.center = ((display_width/2),(display_height/2.5))
        textRect3.center = ((display_width/2),(display_height/2))

        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(text2, textRect2)
        gameDisplay.blit(text3, textRect3)


        pygame.draw.rect(gameDisplay, lightBlue,(350,400,100,50))

        buttonText = pygame.font.Font("freesansbold.ttf",15)
        textSurf, textRect = text_objects("Let's Begin!", buttonText, black)
        # textRect.center = ( (150+(100/2)), (450+(50/2)) )
        textRect.center = (display_width/2),(display_height/1.4)
        gameDisplay.blit(textSurf, textRect)

        # pygame.draw.rect(gameDisplay, lightGreen,(display_width-50,450,100,50))

        pygame.display.update()
        clock.tick(15)

#CAN CHOOSE THE IMAGE
def choose_img():
    img = True
    while img:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()                
                quit()
        if mspserial.in_waiting > 0:
            if "left" in str(mspserial.readline()):
                # print('choose image done')
                PlayerChosenImage = dogPic
                project_loop(PlayerChosenImage)
            if "right" in str(mspserial.readline()):
                # print('choose image done')
                PlayerChosenImage = starMousePic
                project_loop(PlayerChosenImage)
            if "up" in str(mspserial.readline()):
                # print('choose image done')
                PlayerChosenImage = circlePic
                project_loop(PlayerChosenImage)

        #background: colored pencil sketches
        gameDisplay.fill(white)
        background = pygame.image.load('img/colored_pencil.png')
        gameDisplay.blit(background, (0, 0))

        #WHITE RECTANGLE
        # pygame.draw.rect(gameDisplay, white, pygame.Rect((20, 20, 20, 20)))

        largeText = pygame.font.Font('freesansbold.ttf',30)
        # superSmallText = pygame.font.Font('freesansbold.ttf',10)
        # subtitleText = pygame.font.Font('freesansbold.ttf',20)

        TextSurf, TextRect = text_objects("Please Select Your Image!", largeText, black)
        TextRect.center = ((display_width/4),(display_height/5))

        #DISPLAYING IMAGE OPTIONS

        #up: gradient circle
        gameDisplay.blit(circlePic, ((display_width/4),(display_height/3)))

        #left: dog!
        gameDisplay.blit(dogPic, ((display_width/7),(display_height/2)))

        #right: star
        gameDisplay.blit(starMousePic, ((display_width/3),(display_height/2)))
       
        #actually display the messages
        gameDisplay.blit(TextSurf, TextRect)
        # gameDisplay.blit(textsurf2, textrect2)


        pygame.display.update()
        clock.tick(15)


#showcasing the final work!
def finalWork(screenshot):
    print('hey')
    gameDisplay.fill(white)
    pygame.display.update()
    gameDisplay.blit(screenshot, (0,0))
    print(screenshot)
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects("Please Select Your Image!", largeText, black)
    TextRect.center = ((display_width/4),(display_height/5))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    clock.tick(15)


#the main loop
def project_loop(PlayerChosenImage):
    projectExit = False
    drawing = False
    last_pos = None
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0


    gameDisplay.fill(white)
    if PlayerChosenImage == starMousePic:
        gameDisplay.blit(spaceBackground, (0, 0))
    elif PlayerChosenImage == dogPic:
        gameDisplay.blit(dogParkBackground, (0, 0))

    pygame.display.update()

    while not projectExit:
        # running game loop until we physically exit


        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user exits the window
                pygame.quit()
                quit()

            ## DRAWING W/ THE MOUSE
            elif event.type == pygame.MOUSEMOTION:
                if (drawing):
                    mouse_position = pygame.mouse.get_pos()
                    if last_pos is not None:
                        if PlayerChosenImage == circlePic:
                            pygame.draw.line(gameDisplay, lightPink, last_pos, mouse_position, 5)
                        elif PlayerChosenImage == starMousePic:
                            pygame.draw.line(gameDisplay, lightGreen, last_pos, mouse_position, 5)
                        elif PlayerChosenImage == dogPic:
                            pygame.draw.line(gameDisplay, gold, last_pos, mouse_position, 5)
                    last_pos = mouse_position
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = (0,0)
                drawing = False
                if event.button == 3: #if the user presses the right side of the mouse, can start over and choose an image
                    choose_img()
                # if event.button == 2: #future plans to display the final project, give ability to share
                #     screenshot = gameDisplay.copy()
                #     projectExit = True
                #     finalWork(screenshot)

        if mspserial.in_waiting > 0:
            direction = str(mspserial.readline())
            if "left" in direction:
                x1 = -5
                x2 = 0
                y1 = 0
                y2 = 0
            if "right" in direction:
                x2 = 5 #up, if combo of left, then pressing up, will be left+up direction
                x1 = 0
                y1 = 0
                y2 = 0
                # print("this is x2")
                # print(x2)
            if "up" in direction:
                y1 = -5
                y2 = 0
                x1 = 0
                x2 = 0
            if "down" in direction:
                y2 = 5
                y1 = 0
                x1 = 0
                x2 = 0
        

        #ideas: rotate canvas based on potentiometer, q: how to make use of info from desktop to the msp? (if color is red/green, turn on LED)
        #features: startup screen, choose which image (ideally would be drawing with a line, not the image itself), change line for mouse
        
        x += x1 + x2
        y += y1 + y2
        # print("this is x, y")
        # print(x,y)
        chosenIMG(PlayerChosenImage,x,y)
        

#adding bounds!!
        if x > display_width - star_width:
            x = display_width - star_width
        if x < 0:
            x = 0
        if y > display_height - star_width:
            y = display_height - star_width
        if y < 0:
            y = 0

        pygame.display.update()
        clock.tick(60)

mspserial = serial.Serial('/dev/cu.usbmodem142103', 9600)

project_intro()
mspserial.close()
pygame.quit()
quit()


#have to mspserial.close() somewhere ://


