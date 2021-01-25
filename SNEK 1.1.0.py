import random,sys
import pygame
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Isaacs Very Nice SNEK game')

GameWidth=500
GameHeight=500
StartScreenHeight = 600

FONT = pygame.font.Font('freesansbold.ttf', 18)
BIGFONT = pygame.font.Font("freesansbold.ttf",26)

#             R    G    B
GRAY      = (100, 100, 100)
NAVYBLUE  = ( 60,  60, 100)
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
YELLOW    = (255, 255,   0)
ORANGE    = (255, 128,   0)
PURPLE    = (255,   0, 255)
CYAN      = (  0, 255, 255)
BLACK     = (  0,   0,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
RAINBOW   = [  0,  85, 170]

CELLSIZE=20
CellWidth = int(GameWidth / CELLSIZE)
CellHeight = int(GameHeight / CELLSIZE)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

TicksPerSec = 10
TicksPerSecCLOCK = pygame.time.Clock()

HEAD = 0

#SNEK 1 is GREEN
#SNEK 2 is BLUE

#Sound Objects:
#Eating apple sound effect:
EatingAppleSound = pygame.mixer.Sound("SNEK_Sounds/EatingApple.wav")
EatingAppleChannel = pygame.mixer.Channel(1)
#System music:
GameMusicSound = pygame.mixer.Sound("SNEK_Sounds/GameMusic.wav")
GameMusicChannel = pygame.mixer.Channel(2)
#Winner apple sould:
WinnerAppleSound = pygame.mixer.Sound("SNEK_Sounds/WinningApple.wav")

#Set game music volume lower:
GameMusicChannel.set_volume(0.2)

#System functions:
def terminate():
    pygame.quit()
    sys.exit()

def drawGrid(windowSurface,GameHeight,GameWidth):
    for x in range(0, GameWidth, CELLSIZE): # draw vertical lines
        pygame.draw.line(windowSurface, DARKGRAY, (x, 0), (x, GameHeight))
    for y in range(0, GameHeight, CELLSIZE): # draw horizontal lines
        pygame.draw.line(windowSurface, DARKGRAY, (0, y), (GameWidth, y))

def drawSNEKS(Cords_list,Version,windowSurface):
    for cord in Cords_list:
        x = cord["x"] * CELLSIZE
        y = cord["y"] * CELLSIZE
        SnekSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        SnekInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        
        if Version=="1":
            if (cord["x"] == Cords_list[HEAD]["x"]) and (cord["y"] == Cords_list[HEAD]["y"]):
                pygame.draw.rect(windowSurface, GREEN, SnekSegmentRect)
                pygame.draw.rect(windowSurface, ORANGE, SnekInnerSegmentRect)
            else:
                pygame.draw.rect(windowSurface, GREEN, SnekSegmentRect)
                pygame.draw.rect(windowSurface, DARKGREEN, SnekInnerSegmentRect)
        elif Version=="2":
            if (cord["x"] == Cords_list[HEAD]["x"]) and (cord["y"] == Cords_list[HEAD]["y"]):
                pygame.draw.rect(windowSurface, BLUE, SnekSegmentRect)
                pygame.draw.rect(windowSurface, ORANGE, SnekInnerSegmentRect)
            else:
                pygame.draw.rect(windowSurface, BLUE, SnekSegmentRect)
                pygame.draw.rect(windowSurface, NAVYBLUE, SnekInnerSegmentRect)
        
def drawFruits(AppleCords,windowSurface):
    x=AppleCords['x'] * CELLSIZE
    y=AppleCords['y'] * CELLSIZE

    FruitRect=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    
    if AppleCords["Type"] == "Normal":
        pygame.draw.rect(windowSurface,RED,FruitRect)
    elif AppleCords["Type"] == "Speed":
        pygame.draw.rect(windowSurface,YELLOW,FruitRect)
    elif AppleCords["Type"] == "Board":
        pygame.draw.rect(windowSurface,CYAN,FruitRect)
    elif AppleCords["Type"] == "Master":
        pygame.draw.rect(windowSurface,RAINBOW,FruitRect)

def makeFruits(CellWidth,CellHeight):
    x=random.randint(0, CellWidth - 1)
    y=random.randint(0, CellHeight - 1)
    Chance = random.randint(0,201)

    if (Chance % 200) == 0:
        Type = "Master"
    else:
        TypeList=["Normal","Speed","Board"]
        Type = random.choice(TypeList)

    return {'x':x,'y':y,'Type':Type}

def drawLengths(SnekCords,Side,windowSurface):
    if Side=="LEFT":
        scoreSurf = FONT.render('Snek1 Length: '+str(len(SnekCords)), True, DARKGREEN)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (10,10)
    elif Side=="RIGHT":
        scoreSurf = FONT.render('Snek2 Length: '+str(len(SnekCords)), True, CYAN)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topright = (GameWidth, 10)    
    
    windowSurface.blit(scoreSurf, scoreRect)

def drawStartScreen(Cords_list1,Cords_list2,Snek1,Snek2,Snek1GrowthApples,Snek2GrowthApples,Snek1SpeedApples,Snek2SpeedApples,Snek1BoardApples,Snek2BoardApples):
    LargeWindow = pygame.display.set_mode((GameWidth, StartScreenHeight),0, 32)

    titleSurf1 = FONT.render('BRO TIME FOR A SNEK GAME', True, WHITE, None)
    EnterMessage = FONT.render('PRESS ENTER TO PLAY',True,RED,None)
    QuitMessage = FONT.render("ESC TO QUIT",True,RED,None) 

    Snek1Keys = FONT.render("WASD To Control The BLUE Snek",True,RED,BLACK) 
    Snek2Keys = FONT.render("ARROW KEYS Or IJKL To Control The GREEN Snek",True,RED,BLACK)
    Snek1Placement = {"x":10, "y":(StartScreenHeight - 10)}
    Snek2Placement = {"x":10, "y":(StartScreenHeight - 30)}

    StatsWords = FONT.render(" STATS ",True,BLACK,WHITE)
    StatsRect = pygame.draw.rect(LargeWindow,WHITE,(10,(StartScreenHeight-80),90,100))

    KeyPresses=""

    #Display first message
    TitleRect = titleSurf1.get_rect()
    TitleRect.center = (int(GameWidth/2), int(GameHeight/2))
    #Display "Enter" message
    EnterRect=EnterMessage.get_rect()
    EnterRect.center = (int(GameWidth/2),int((GameHeight - (GameHeight/3))))
    #Display the Quit message
    QuitRect = QuitMessage.get_rect()
    QuitRect.center = (int(GameWidth/2),int((GameHeight - (GameHeight/4))))
    #Display Snek1 Message
    Snek1KeysRect = Snek1Keys.get_rect()
    Snek1KeysRect.bottomleft = (Snek1Placement["x"],Snek1Placement["y"])
    #Display Snek2 Message
    Snek2KeysRect = Snek2Keys.get_rect()
    Snek2KeysRect.bottomleft = (Snek2Placement["x"],Snek2Placement["y"])

    while True:
        LargeWindow.fill(BLACK)
        drawGrid(LargeWindow,GameHeight,GameWidth)
        drawSNEKS(Cords_list1,Snek1,LargeWindow)
        drawSNEKS(Cords_list2,Snek2,LargeWindow)

        LargeWindow.blit(titleSurf1,TitleRect)
        LargeWindow.blit(EnterMessage,EnterRect)
        LargeWindow.blit(QuitMessage,QuitRect)
        LargeWindow.blit(Snek1Keys,Snek1KeysRect)
        LargeWindow.blit(Snek2Keys,Snek2KeysRect)
        StatButton = LargeWindow.blit(StatsWords,StatsRect)
        pygame.display.flip()

        for event in pygame.event.get(): 
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_j:
                    KeyPresses+="L"
                elif event.key == K_RIGHT or event.key == K_l:
                    KeyPresses+="R"
                elif event.key == K_UP or event.key == K_i:
                    KeyPresses+="U"
                elif event.key == K_DOWN or event.key == K_k:
                    KeyPresses+="D"
                elif (event.key == K_a):
                    KeyPresses+="a"
                elif (event.key == K_d):
                    KeyPresses+="d"
                elif (event.key == K_w):
                    KeyPresses+="w"
                elif (event.key == K_s):
                    KeyPresses+="s"
                elif event.key == K_RETURN:
                    return KeyPresses
                elif event.key == K_ESCAPE:
                    terminate()
            elif event.type==MOUSEBUTTONUP and event.button==1:
                MousePosition = pygame.mouse.get_pos()
                if StatButton.collidepoint(MousePosition):
                    drawStatsScreen(LargeWindow,Snek1GrowthApples,Snek2GrowthApples,Snek1SpeedApples,Snek2SpeedApples,Snek1BoardApples,Snek2BoardApples)
        
        if GameMusicChannel.get_busy() == False:
            GameMusicChannel.play(GameMusicSound)
    
def KonamiChecker(KeyPresses,TicksPerSec):
    #Konami Code: wUaLsDdR
    #Konami Code checker:
    for letter in range(0,len(KeyPresses)):
        if len(KeyPresses) > 7:
            if KeyPresses[letter] == "w" and KeyPresses[letter +1]=="U" and KeyPresses[letter+2]=="a" and KeyPresses[letter+3]=="L" and KeyPresses[letter+4]=="s" and KeyPresses[letter+5]=="D" and KeyPresses[letter+6]=="d" and KeyPresses[letter+7]=="R":
                TicksPerSec=5
                break
        else:
            TicksPerSec=10

    return TicksPerSec

def SnekStartingCords():
    DirectionList =["left","right","up","down"]
    FacingDirection = random.choice(DirectionList)

    StartSquareX = random.randint(3,CELLSIZE-3)
    StartSquareY = random.randint(3,CELLSIZE-3)

    if FacingDirection == "left":
        DifferenceX = 1
        DifferenceY = 0
    elif FacingDirection == "right":
        DifferenceX = -1
        DifferenceY = 0
    elif FacingDirection == "down":
        DifferenceX = 0
        DifferenceY = -1
    elif FacingDirection == "up":
        DifferenceX = 0
        DifferenceY = 1 

    SnekCordinates =  [
    {"x":StartSquareX, "y":StartSquareY},
    {"x":(StartSquareX + DifferenceX),    "y":(StartSquareY + DifferenceY)},
    {"x":(StartSquareX + 2*DifferenceX), "y":(StartSquareY + 2*DifferenceY)}]

    return SnekCordinates,FacingDirection

def drawStatsScreen(LargeWindow, Snek1Length, Snek2Length, Snek1Speed, Snek2Speed, Snek1Boards, Snek2Boards):
    WindowOpener = BIGFONT.render("STATS WINDOW - ESC TO RETURN",True,RED)
    WindowOpenerRect = WindowOpener.get_rect()
    WindowOpenerRect.center = ((int(GameWidth/2)),30)

    xSpacing = 10
    ySpacing = 100

    #Stats for SNEK 1:
    Snek1StatsWords = BIGFONT.render("STATS FOR SNEK 1:",True,GREEN)
    Snek1StatsRect = Snek1StatsWords.get_rect()
    Snek1StatsRect.topleft = (xSpacing,ySpacing)

    ySpacing += 40
    Snek1RedApplesWords = FONT.render("RED Apples Eaten: " + Snek1Length,True,GREEN)
    Snek1RedAppleRect = Snek1RedApplesWords.get_rect()
    Snek1RedAppleRect.topleft = (xSpacing,ySpacing)
    
    ySpacing += 20
    Snek1YellowApplesWords = FONT.render("YELLOW Apples Eaten: " + Snek1Speed,True,GREEN)
    Snek1YellowAppleRect = Snek1YellowApplesWords.get_rect()
    Snek1YellowAppleRect.topleft = (xSpacing,ySpacing)

    ySpacing += 20
    Snek1BlueApplesWords = FONT.render("BLUE Apples Eaten: " + Snek1Boards,True,GREEN)
    Snek1BlueAppleRect = Snek1BlueApplesWords.get_rect()
    Snek1BlueAppleRect.topleft = (xSpacing,ySpacing)

    ySpacing += 60
    Snek2StatsWords = BIGFONT.render("STATS FOR SNEK 2:",True,CYAN)
    Snek2StatsRect = Snek2StatsWords.get_rect()
    Snek2StatsRect.topleft = (xSpacing,ySpacing)

    ySpacing += 40
    Snek2RedApplesWords = FONT.render("RED Apples Eaten: " + Snek1Length,True,CYAN)
    Snek2RedAppleRect = Snek1RedApplesWords.get_rect()
    Snek2RedAppleRect.topleft = (xSpacing,ySpacing)

    ySpacing += 20
    Snek2YellowApplesWords = FONT.render("YELLOW Apples Eaten: " + Snek2Speed,True,CYAN)
    Snek2YellowAppleRect = Snek2YellowApplesWords.get_rect()
    Snek2YellowAppleRect.topleft = (xSpacing,ySpacing)

    ySpacing += 20
    Snek2BlueApplesWords = FONT.render("BLUE Apples Eaten: " + Snek2Boards,True,CYAN)
    Snek2BlueAppleRect = Snek2BlueApplesWords.get_rect()
    Snek2BlueAppleRect.topleft = (xSpacing,ySpacing)

    while True:
        for event in pygame.event.get(): 
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN and (event.key == K_ESCAPE):
                return

        LargeWindow.fill(BLACK)
        LargeWindow.blit(WindowOpener,WindowOpenerRect)
        LargeWindow.blit(Snek1StatsWords,Snek1StatsRect)
        LargeWindow.blit(Snek2StatsWords,Snek2StatsRect)
        LargeWindow.blit(Snek1RedApplesWords,Snek1RedAppleRect)
        LargeWindow.blit(Snek1YellowApplesWords,Snek1YellowAppleRect)
        LargeWindow.blit(Snek1BlueApplesWords,Snek1BlueAppleRect)
        LargeWindow.blit(Snek2RedApplesWords,Snek2RedAppleRect)
        LargeWindow.blit(Snek2YellowApplesWords,Snek2YellowAppleRect)
        LargeWindow.blit(Snek2BlueApplesWords,Snek2BlueAppleRect)

        pygame.display.flip()

def Runner(AppleCords,Snake1Cords,Snake1Direction,Snake2Cords,Snake2Direction,TicksPerSec,GameWidth,GameHeight):
    SmallWindow = pygame.display.set_mode((GameWidth, GameHeight),0, 32)
    CellWidth = int(GameWidth / CELLSIZE)
    CellHeight = int(GameHeight / CELLSIZE)

    Color1Direction = True
    Color2Direction = True
    Color3Direction = True

    PlayerWon = False

    Snek1SpeedApplesEaten = 0
    Snek1BoardApplesEaten = 0

    Snek2SpeedApplesEaten = 0
    Snek2BoardApplesEaten = 0

    # main game loop
    while True:
        #Event handling loop
        for event in pygame.event.get(): 
            if event.type == QUIT:
                break
            elif event.type == KEYDOWN:
                #Snek 1 direction settings:
                if (event.key == K_LEFT or event.key == K_j) and Snake1Direction != RIGHT:
                    Snake1Direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_l) and Snake1Direction != LEFT:
                    Snake1Direction = RIGHT
                elif (event.key == K_UP or event.key == K_i)  and Snake1Direction != DOWN:
                    Snake1Direction = UP
                elif (event.key == K_DOWN or event.key == K_k) and Snake1Direction != UP:
                    Snake1Direction = DOWN

                #Snek 2 direction settings:
                elif (event.key == K_a) and Snake2Direction != RIGHT:
                    Snake2Direction = LEFT
                elif (event.key == K_d and Snake2Direction != LEFT):
                    Snake2Direction = RIGHT
                elif (event.key == K_w and Snake2Direction != DOWN):
                    Snake2Direction = UP
                elif (event.key == K_s and Snake2Direction != UP):
                    Snake2Direction = DOWN
                
                elif (event.key == K_ESCAPE) and (PlayerWon == True):
                    return str(len(Snake1Cords)-3),str(len(Snake2Cords)-3), str(Snek1SpeedApplesEaten), str(Snek2SpeedApplesEaten),str(Snek1BoardApplesEaten),str(Snek2BoardApplesEaten)

        #Check if Snek 1 hit walls:
        if Snake1Cords[HEAD]['x'] == -1 or Snake1Cords[HEAD]['x'] == CellWidth or Snake1Cords[HEAD]['y'] == -1 or Snake1Cords[HEAD]['y'] == CellHeight:
            return str(len(Snake1Cords)-3),str(len(Snake2Cords)-3), str(Snek1SpeedApplesEaten), str(Snek2SpeedApplesEaten),str(Snek1BoardApplesEaten),str(Snek2BoardApplesEaten)
        #Check if Snek 2 hit walls
        if Snake2Cords[HEAD]['x'] == -1 or Snake2Cords[HEAD]['x'] == CellWidth or Snake2Cords[HEAD]['y'] == -1 or Snake2Cords[HEAD]['y'] == CellHeight:
            return str(len(Snake1Cords)-3),str(len(Snake2Cords)-3), str(Snek1SpeedApplesEaten), str(Snek2SpeedApplesEaten),str(Snek1BoardApplesEaten),str(Snek2BoardApplesEaten)

        #Check if Snek 1 hit themself:
        for SnekBody in Snake1Cords[1:]:
            if SnekBody['x'] == Snake1Cords[HEAD]['x'] and SnekBody['y'] == Snake1Cords[HEAD]['y']:
                return str(len(Snake1Cords)-3),str(len(Snake2Cords)-3), str(Snek1SpeedApplesEaten), str(Snek2SpeedApplesEaten),str(Snek1BoardApplesEaten),str(Snek2BoardApplesEaten)
        #Check if Snek 2 hit themself:
        for SnekBody in Snake2Cords[1:]:
            if SnekBody['x'] == Snake2Cords[HEAD]['x'] and SnekBody['y'] == Snake2Cords[HEAD]['y']:
                return str(len(Snake1Cords)-3),str(len(Snake2Cords)-3), str(Snek1SpeedApplesEaten), str(Snek2SpeedApplesEaten),str(Snek1BoardApplesEaten),str(Snek2BoardApplesEaten)
        
        #Check if Snek 1 hit Snek 2:
        for body in Snake2Cords[0:]:
            if Snake1Cords[HEAD]['x']==body['x'] and Snake1Cords[HEAD]['y']==body['y']:
                return str(len(Snake1Cords)-3),str(len(Snake2Cords)-3), str(Snek1SpeedApplesEaten), str(Snek2SpeedApplesEaten),str(Snek1BoardApplesEaten),str(Snek2BoardApplesEaten)
        #Check if Snek 2 hit Snek 1:
        for body in Snake1Cords[0:]:
            if Snake2Cords[HEAD]['x']==body['x'] and Snake2Cords[HEAD]['y']==body['y']:
                return str(len(Snake1Cords)-3),str(len(Snake2Cords)-3), str(Snek1SpeedApplesEaten), str(Snek2SpeedApplesEaten),str(Snek1BoardApplesEaten),str(Snek2BoardApplesEaten)

        #If the player has not won...Do everythin:
        if PlayerWon == False:
            #check if SNEK1 has eaten an apple and make it do stuff if it has:
            if Snake1Cords[HEAD]['x'] == AppleCords['x'] and Snake1Cords[HEAD]['y'] == AppleCords['y'] and AppleCords["Type"] == "Normal":
                AppleCords=makeFruits(CellWidth,CellHeight) # set a new apple somewhere
                EatingAppleChannel.play(EatingAppleSound)

            elif Snake1Cords[HEAD]['x'] == AppleCords['x'] and Snake1Cords[HEAD]['y'] == AppleCords['y'] and AppleCords["Type"] == "Speed":
                TicksPerSec +=1
                AppleCords=makeFruits(CellWidth,CellHeight)
                del Snake1Cords[-1]
                EatingAppleChannel.play(EatingAppleSound)
                Snek1SpeedApplesEaten += 1

            elif Snake1Cords[HEAD]['x'] == AppleCords['x'] and Snake1Cords[HEAD]['y'] == AppleCords['y'] and AppleCords["Type"] == "Board":
                GameHeight += CELLSIZE
                GameWidth += CELLSIZE
                AppleCords=makeFruits(CellWidth,CellHeight)
                del Snake1Cords[-1]
                EatingAppleChannel.play(EatingAppleSound)
                Snek1BoardApplesEaten += 1

            elif Snake1Cords[HEAD]['x'] == AppleCords['x'] and Snake1Cords[HEAD]['y'] == AppleCords['y'] and AppleCords["Type"] == "Master":
                PlayerWon = True
                del Snake1Cords[-1]
            else:
                del Snake1Cords[-1] # remove Snek's tail segment
            
            #check if SNEK2 has eaten an apple and make it grow if it has: 
            if Snake2Cords[HEAD]['x'] == AppleCords['x'] and Snake2Cords[HEAD]['y'] == AppleCords['y'] and AppleCords["Type"] == "Normal":
                AppleCords=makeFruits(CellWidth,CellHeight) # set a new apple somewhere
                EatingAppleChannel.play(EatingAppleSound)

            elif Snake2Cords[HEAD]['x'] == AppleCords['x'] and Snake2Cords[HEAD]['y'] == AppleCords['y'] and AppleCords["Type"] == "Speed":
                TicksPerSec +=1
                AppleCords=makeFruits(CellWidth,CellHeight)
                del Snake2Cords[-1]
                EatingAppleChannel.play(EatingAppleSound)
                Snek2SpeedApplesEaten += 1 

            elif Snake2Cords[HEAD]['x'] == AppleCords['x'] and Snake2Cords[HEAD]['y'] == AppleCords['y'] and AppleCords["Type"] == "Board":
                GameHeight += CELLSIZE
                GameWidth += CELLSIZE
                AppleCords=makeFruits(CellWidth,CellHeight)
                del Snake2Cords[-1]
                EatingAppleChannel.play(EatingAppleSound)
                Snek2BoardApplesEaten += 1 

            elif Snake2Cords[HEAD]['x'] == AppleCords['x'] and Snake2Cords[HEAD]['y'] == AppleCords['y'] and AppleCords["Type"] == "Master":
                PlayerWon = True
                del Snake2Cords[-1]
            else:
                del Snake2Cords[-1] # remove Snek's tail segment

            #Add segments in the direction Snek 1 is moving
            if Snake1Direction==UP:
                newHead1 = {'x': Snake1Cords[HEAD]['x'], 'y': Snake1Cords[HEAD]['y'] - 1}
            elif Snake1Direction==DOWN:
                newHead1 = {'x': Snake1Cords[HEAD]['x'], 'y': Snake1Cords[HEAD]['y'] + 1}
            elif Snake1Direction==LEFT:
                newHead1 = {'x': Snake1Cords[HEAD]['x'] - 1, 'y': Snake1Cords[HEAD]['y']}
            elif Snake1Direction==RIGHT:
                newHead1 = {'x': Snake1Cords[HEAD]['x'] + 1, 'y': Snake1Cords[HEAD]['y']}
            Snake1Cords.insert(HEAD,newHead1)
            #Add segments in the direction Snek 2 is moving
            if Snake2Direction==UP:
                newHead2 = {'x': Snake2Cords[HEAD]['x'], 'y': Snake2Cords[HEAD]['y'] - 1}
            elif Snake2Direction==DOWN:
                newHead2 = {'x': Snake2Cords[HEAD]['x'], 'y': Snake2Cords[HEAD]['y'] + 1}
            elif Snake2Direction==LEFT:
                newHead2 = {'x': Snake2Cords[HEAD]['x'] - 1, 'y': Snake2Cords[HEAD]['y']}
            elif Snake2Direction==RIGHT:
                newHead2 = {'x': Snake2Cords[HEAD]['x'] + 1, 'y': Snake2Cords[HEAD]['y']}
            Snake2Cords.insert(HEAD,newHead2)

        Placement = 0
        for color in RAINBOW:
            if Placement == 0:
                if color >= 255:
                    color = 250
                    Color1Direction = False
                elif color < 15:
                    color = 15
                    Color1Direction = True
                
                if Color1Direction == False:
                    color -= 5
                elif Color1Direction == True:
                    color += 5

            elif Placement == 1:
                if color >= 255:
                    color = 250
                    Color2Direction = False
                elif color < 15:
                    color = 15
                    Color2Direction = True
                
                if Color2Direction == False:
                    color -= 5
                elif Color2Direction == True:
                    color += 5
            
            elif Placement == 2:
                if color >= 255:
                    color = 250
                    Color3Direction = False
                elif color < 15:
                    color = 15
                    Color3Direction = True
                
                if Color3Direction == False:
                    color -= 5
                elif Color3Direction == True:
                    color += 5
            
            RAINBOW[Placement] = color
            Placement += 1

        #Fake Global Variables:
        CellWidth = int(GameWidth / CELLSIZE)
        CellHeight = int(GameHeight / CELLSIZE)
        SmallWindow = pygame.display.set_mode((GameWidth, GameHeight),0, 32)

        #Draw everything
        SmallWindow.fill(BLACK)
        drawGrid(SmallWindow,GameHeight,GameWidth)
        drawLengths(Snake1Cords,"LEFT",SmallWindow)
        drawLengths(Snake2Cords,"RIGHT",SmallWindow)
        drawSNEKS(Snake1Cords,"1",SmallWindow)
        drawSNEKS(Snake2Cords,"2",SmallWindow)
        drawFruits(AppleCords,SmallWindow)
        pygame.display.flip()

        #Play the music if not already playing:
        if PlayerWon == False:
            if GameMusicChannel.get_busy() == False:
                GameMusicChannel.play(GameMusicSound)
        else:
            if GameMusicChannel.get_sound() != WinnerAppleSound:
                GameMusicChannel.play(WinnerAppleSound)

        TicksPerSecCLOCK.tick(TicksPerSec)

Snek1Length = "N/A"
Snek2Length = "N/A"
GameScore = "N/A"

Snek1Length = "N/A"
Snek2Length = "N/A" 
Snake1Speed = "N/A" 
Snake2Speed = "N/A" 
Snake1BoardGrowth = "N/A" 
Snake2BoardGrowth = "N/A"

while True:
    TicksPerSec = 10

    Snake1Cords,Snake1Direction = SnekStartingCords()
    Snake2Cords,Snake2Direction = SnekStartingCords()

    KonamiList=drawStartScreen(Snake1Cords,Snake2Cords,"1","2",Snek1Length, Snek2Length, Snake1Speed, Snake2Speed, Snake1BoardGrowth, Snake2BoardGrowth)
     
    TicksPerSec=KonamiChecker(KonamiList,TicksPerSec)
    AppleCords=makeFruits(CellWidth,CellHeight) 

    Snek1Length, Snek2Length, Snake1Speed, Snake2Speed, Snake1BoardGrowth, Snake2BoardGrowth = Runner(AppleCords,Snake1Cords,Snake1Direction,Snake2Cords,Snake2Direction,TicksPerSec,GameHeight,GameWidth)
