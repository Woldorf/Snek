"""
Made and produced by Broken Keyboard Studios, all rights reserved.
Feel free to edit sound volumes located on lines 64 and 65.
"""
#!/usr/bin/python
import random,sys,pygame
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Dual Snakes - BrokenKeyboard Studios')
GameScreen = pygame.display.set_mode((0,0))
pygame.display.toggle_fullscreen()

GAMEWIDTH=pygame.display.Info().current_w
GAMEHEIGHT=pygame.display.Info().current_h

FONT = pygame.font.Font('freesansbold.ttf', 18)
BIGFONT = pygame.font.Font("freesansbold.ttf",26)

#Colors:
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
CellWidth = int(GAMEWIDTH / CELLSIZE)
CellHeight = int(GAMEHEIGHT / CELLSIZE)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0

TicksPerSec = 10
TicksPerSecCLOCK = pygame.time.Clock()

#Snek 1 is Green
#Snek 2 is Blue

#Sound Objects:
#Eating apple sound effect:
EatingAppleSound = pygame.mixer.Sound("SnekFiles/EatingApple.wav")
EatingAppleChannel = pygame.mixer.Channel(1)
#System music:
GameMusicSound = pygame.mixer.Sound("SnekFiles/GameMusic.wav")
GameMusicChannel = pygame.mixer.Channel(2)
#Winner apple sould:
WinnerAppleSound = pygame.mixer.Sound("SnekFiles/WinningApple.wav")
#Set game music volume lower:
GameMusicChannel.set_volume(0.2)
#EatingAppleChannel.set_volume(0.0)

class Text:
    def __init__(self,Text,Color,Size, Y = None, X = None,):
        self.Text = pygame.font.Font("freesansbold.ttf",Size).render(Text,True,Color)
        self.Obj = self.Text.get_rect()

        if X == None:
            self.X = int(GAMEWIDTH/2)
        if Y != None:
            self.Y = Y
            self.Obj.center = (self.X,self.Y)

    def UpdateScreen(self,ScrollSpeed = None):
        if ScrollSpeed != None:
            self.Y -= ScrollSpeed
            self.Obj.center = (self.X,self.Y)

        GameScreen.blit(self.Text,self.Obj)

#Snek Class:
class Snek:
    def __init__(self,Color,SecondaryColor,Player,LableColor):
        self.OuterColor = Color
        self.InnerColor = SecondaryColor
        self.CordsList = []
        self.Direction = "None"
        self.Player = Player
        self.LableColor = LableColor
        self.SpeedApples = 0
        self.NormalApples = 0

    def UpdateScreen(self):
        for cord in self.CordsList:
            x = cord["x"] * CELLSIZE
            y = cord["y"] * CELLSIZE
            SnekOuterSegmentRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
            SnekInnerSegmentRect = pygame.Rect(x + 4,y + 4, CELLSIZE - 8, CELLSIZE - 8)
            
            pygame.draw.rect(GameScreen, self.OuterColor, SnekOuterSegmentRect)
            if (cord["x"] == self.CordsList[HEAD]["x"]) and cord["y"] == self.CordsList[HEAD]["y"]:
                pygame.draw.rect(GameScreen, ORANGE, SnekInnerSegmentRect)
            else:
                pygame.draw.rect(GameScreen, self.InnerColor, SnekInnerSegmentRect)

    def DrawLable(self):
        scoreSurf = FONT.render("Snek"+str(self.Player)+" Length:"+str(len(self.CordsList)),True, self.LableColor)
        scoreRect = scoreSurf.get_rect()
        if self.Player == 1:
            scoreRect.topleft = (10,10)
        else:
            scoreRect.topright = ((GAMEWIDTH - 10),10)
        GameScreen.blit(scoreSurf,scoreRect)

    def ChangeDirection(self,Key):
        if self.Player == 1:
            if (Key == K_LEFT or Key == K_j) and self.Direction != RIGHT:
                self.Direction = LEFT
            elif (Key == K_RIGHT or Key == K_l) and self.Direction != LEFT:
                self.Direction = RIGHT
            elif (Key == K_UP or Key == K_i)  and self.Direction != DOWN:
                self.Direction = UP
            elif (Key == K_DOWN or Key == K_k) and self.Direction != UP:
                self.Direction = DOWN
        else:
            if Key == K_a and self.Direction != RIGHT:
               self.Direction = LEFT
            elif Key == K_d and self.Direction != LEFT:
                self.Direction = RIGHT
            elif Key == K_w  and self.Direction != DOWN:
                self.Direction = UP
            elif Key == K_s and self.Direction != UP:
                self.Direction = DOWN 

    def CollisionDetection(self,OtherSnek,Apple,Tics,Won):
        GameOver = False
        NewApple = False
        Grow = False
        #Wall Check:
        if self.CordsList[HEAD]['x'] == -1 or self.CordsList[HEAD]['x'] == CellWidth or self.CordsList[HEAD]['y'] == -1 or self.CordsList[HEAD]['y'] == CellHeight:
            GameOver = True
        #Body Check:
        for SnekBody in self.CordsList[1:]:
            if SnekBody['x'] == self.CordsList[HEAD]['x'] and SnekBody['y'] == self.CordsList[HEAD]['y']:
                GameOver = True
                break
        #Oppenent Check:
        if not GameOver:
            for SnekBody in OtherSnek.CordsList[0:]:
                if self.CordsList[HEAD]['x']==SnekBody['x'] and self.CordsList[HEAD]['y']==SnekBody['y']:
                    GameOver = True
                    break
            #Apple Check:
            if self.CordsList[HEAD]['x'] == Apple['x'] and self.CordsList[HEAD]['y'] == Apple['y'] and Apple["Type"] == "Normal":
                EatingAppleChannel.play(EatingAppleSound)
                self.NormalApples += 1
                NewApple = True
                Grow = True
            elif self.CordsList[HEAD]['x'] == Apple['x'] and self.CordsList[HEAD]['y'] == Apple['y'] and Apple["Type"] == "Speed":
                EatingAppleChannel.play(EatingAppleSound)
                self.SpeedApples += 1
                Tics += 1
                NewApple = True
            elif self.CordsList[HEAD]['x'] == Apple['x'] and self.CordsList[HEAD]['y'] == Apple['y'] and Apple["Type"] == "Master":
                Won = "True"

        if not Grow:
            del self.CordsList[-1]

        if NewApple:
            return GameOver, makeFruits(), Tics, Won
        else:
            return GameOver, Apple, Tics, Won

    def Move(self):
        if self.Direction==UP:
            self.CordsList.insert(HEAD,{'x': self.CordsList[HEAD]['x'], 'y': self.CordsList[HEAD]['y'] - 1})
        elif self.Direction==DOWN:
            self.CordsList.insert(HEAD,{'x': self.CordsList[HEAD]['x'], 'y': self.CordsList[HEAD]['y'] + 1})
        elif self.Direction==LEFT:
            self.CordsList.insert(HEAD,{'x': self.CordsList[HEAD]['x'] - 1, 'y': self.CordsList[HEAD]['y']})
        elif self.Direction==RIGHT:
            self.CordsList.insert(HEAD,{'x': self.CordsList[HEAD]['x'] + 1, 'y': self.CordsList[HEAD]['y']})

    def MakeCordinates(self):
        self.Direction = random.choice([LEFT,RIGHT,UP,DOWN])

        StartSquareX = random.randint(3,CellWidth-3)
        StartSquareY = random.randint(3,CellHeight-3)

        if self.Direction == LEFT:
            DifferenceX = 1
            DifferenceY = 0
        elif self.Direction == RIGHT:
            DifferenceX = -1
            DifferenceY = 0
        elif self.Direction == DOWN:
            DifferenceX = 0
            DifferenceY = -1
        elif self.Direction == UP:
            DifferenceX = 0
            DifferenceY = 1 

        self.CordsList = [
        {"x":StartSquareX, "y":StartSquareY},
        {"x":(StartSquareX + DifferenceX),    "y":(StartSquareY + DifferenceY)},
        {"x":(StartSquareX + 2*DifferenceX), "y":(StartSquareY + 2*DifferenceY)}]

#System functions:
def drawGrid():
    for x in range(0, GAMEWIDTH + CELLSIZE, CELLSIZE): # draw vertical lines
        pygame.draw.line(GameScreen, DARKGRAY, (x, 0), (x, GAMEHEIGHT + CELLSIZE))
    for y in range(0, GAMEHEIGHT + CELLSIZE, CELLSIZE): # draw horizontal lines
        pygame.draw.line(GameScreen, DARKGRAY, (0, y), (GAMEWIDTH, y))

def drawPaused():
    Words = BIGFONT.render("GAME IS PAUSED",True,RED)
    WordsRect = Words.get_rect()
    WordsRect.center = (int(GAMEWIDTH/2),int(GAMEHEIGHT/2))
    GameScreen.blit(Words,WordsRect)

def drawFruits(AppleCords):
    x=AppleCords['x'] * CELLSIZE
    y=AppleCords['y'] * CELLSIZE

    FruitRect=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    
    if AppleCords["Type"] == "Normal":
        pygame.draw.rect(GameScreen,RED,FruitRect)
    elif AppleCords["Type"] == "Speed":
        pygame.draw.rect(GameScreen,YELLOW,FruitRect)
        """elif AppleCords["Type"] == "Board":
            pygame.draw.rect(windowSurface,CYAN,FruitRect)"""
    elif AppleCords["Type"] == "Master":
        pygame.draw.rect(GameScreen,RAINBOW,FruitRect)

def drawStartScreen(Snek1,Snek2):
    titleWords = BIGFONT.render('DUAL SNEK', True, WHITE, None)
    EnterMessage = BIGFONT.render('PRESS ENTER OR SPACE TO PLAY',True,RED,None)
    QuitMessage = BIGFONT.render("ESC TO QUIT",True,RED,None) 

    StatsWords = FONT.render(" STATS ",True,WHITE)
    StatsRect = pygame.draw.rect(GameScreen,RED,(10,(GAMEHEIGHT-(GAMEHEIGHT/8)),90,100))
    ControlsWords = FONT.render(" CONTROLS ",True,WHITE)
    ControlsRect = pygame.draw.rect(GameScreen,RED,(10,(GAMEHEIGHT-(GAMEHEIGHT/20)),90,100))

    #Display first message
    TitleRect = titleWords.get_rect()
    TitleRect.center = (int(GAMEWIDTH/2), int(GAMEHEIGHT/2))
    #Display "Enter" message
    EnterRect=EnterMessage.get_rect()
    EnterRect.center = (int(GAMEWIDTH/2),int((GAMEHEIGHT - (GAMEHEIGHT/3))))
    #Display the Quit message
    QuitRect = QuitMessage.get_rect()
    QuitRect.center = (int(GAMEWIDTH/2),int((GAMEHEIGHT - (GAMEHEIGHT/4))))

    KeyPresses=""

    while True:
        GameScreen.fill(BLACK)
        drawGrid()
        Snek1.UpdateScreen()
        Snek2.UpdateScreen()

        GameScreen.blit(titleWords,TitleRect)
        GameScreen.blit(EnterMessage,EnterRect)
        GameScreen.blit(QuitMessage,QuitRect)
        StatButton = GameScreen.blit(StatsWords,StatsRect)
        ControlsButton = GameScreen.blit(ControlsWords,ControlsRect)
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
                elif event.key == K_RETURN or event.key == K_SPACE:
                    return KeyPresses
                elif event.key == K_ESCAPE:
                    terminate()
            elif event.type==MOUSEBUTTONUP and event.button==1:
                MousePosition = pygame.mouse.get_pos()
                if StatButton.collidepoint(MousePosition):
                    drawStatsScreen(Snek1,Snek2)
                elif ControlsButton.collidepoint(MousePosition):
                    drawControlsScreen()
        
        if not GameMusicChannel.get_busy():
            GameMusicChannel.play(GameMusicSound)

def drawStatsScreen(Snek1,Snek2):
    MEGAFONT = pygame.font.Font("freesansbold.ttf",36)
    Snek1HighScore,Snek2HighScore = GetGameFile()

    HighScoreWords = MEGAFONT.render("HIGH SCORE", True, ORANGE)
    HighScoreWordsRect = HighScoreWords.get_rect()
    HighScoreWordsRect.center = ((int(GAMEWIDTH/2)),(GAMEHEIGHT - (GAMEHEIGHT/4)))

    Snek1ScoreWords = BIGFONT.render(str("SNEK 1: " + Snek1HighScore),True,ORANGE)
    Snek1ScoreRect = Snek1ScoreWords.get_rect()
    Snek1ScoreRect.center = (int(GAMEWIDTH/2),(HighScoreWordsRect.bottom + Snek1ScoreRect.height))

    Snek2ScoreWords = BIGFONT.render(str("SNEK 2: " + Snek2HighScore),True,ORANGE)
    Snek2ScoreRect = Snek2ScoreWords.get_rect()
    Snek2ScoreRect.center = (int(GAMEWIDTH/2),(Snek1ScoreRect.bottom + Snek2ScoreRect.height))

    WindowOpener = BIGFONT.render("STATS WINDOW - ESC TO RETURN",True,RED)
    WindowOpenerRect = WindowOpener.get_rect()
    WindowOpenerRect.center = ((int(GAMEWIDTH/2)),30)

    xSpacing = 10
    ySpacing = 100

    #Stats for SNEK 1:
    Snek1StatsWords = BIGFONT.render("STATS FOR SNEK 1:",True,Snek1.LableColor)
    Snek1StatsRect = Snek1StatsWords.get_rect()
    Snek1StatsRect.topleft = (xSpacing,ySpacing)

    ySpacing += 40
    Snek1RedApplesWords = FONT.render("RED Apples Eaten: " + str(Snek1.NormalApples),True,Snek1.LableColor)
    Snek1RedAppleRect = Snek1RedApplesWords.get_rect()
    Snek1RedAppleRect.topleft = (xSpacing,ySpacing)
    
    ySpacing += 20
    Snek1YellowApplesWords = FONT.render("YELLOW Apples Eaten: " + str(Snek1.SpeedApples),True,Snek1.LableColor)
    Snek1YellowAppleRect = Snek1YellowApplesWords.get_rect()
    Snek1YellowAppleRect.topleft = (xSpacing,ySpacing)

    ySpacing += 60
    Snek2StatsWords = BIGFONT.render("STATS FOR SNEK 2:",True,Snek2.LableColor)
    Snek2StatsRect = Snek2StatsWords.get_rect()
    Snek2StatsRect.topleft = (xSpacing,ySpacing)

    ySpacing += 40
    Snek2RedApplesWords = FONT.render("RED Apples Eaten: " + str(Snek2.NormalApples),True,Snek2.LableColor)
    Snek2RedAppleRect = Snek1RedApplesWords.get_rect()
    Snek2RedAppleRect.topleft = (xSpacing,ySpacing)

    ySpacing += 20
    Snek2YellowApplesWords = FONT.render("YELLOW Apples Eaten: " + str(Snek2.SpeedApples),True,Snek2.LableColor)
    Snek2YellowAppleRect = Snek2YellowApplesWords.get_rect()
    Snek2YellowAppleRect.topleft = (xSpacing,ySpacing)

    while True:
        for event in pygame.event.get(): 
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN and (event.key == K_ESCAPE):
                return

        GameScreen.fill(BLACK)
        drawGrid()
        Snek1.UpdateScreen()
        Snek2.UpdateScreen()
        GameScreen.blit(WindowOpener,WindowOpenerRect)
        GameScreen.blit(Snek1StatsWords,Snek1StatsRect)
        GameScreen.blit(Snek2StatsWords,Snek2StatsRect)
        GameScreen.blit(Snek1RedApplesWords,Snek1RedAppleRect)
        GameScreen.blit(Snek1YellowApplesWords,Snek1YellowAppleRect)
        GameScreen.blit(Snek2RedApplesWords,Snek2RedAppleRect)
        GameScreen.blit(Snek2YellowApplesWords,Snek2YellowAppleRect)
        GameScreen.blit(HighScoreWords,HighScoreWordsRect)
        GameScreen.blit(Snek1ScoreWords,Snek1ScoreRect)
        GameScreen.blit(Snek2ScoreWords,Snek2ScoreRect)

        pygame.display.flip()
        if not GameMusicChannel.get_busy():
            GameMusicChannel.play(GameMusicSound)

def drawControlsScreen():
    ALMOSTMEDIUMFONT = pygame.font.Font("freesansbold.ttf",20)
    MEDIUMFONT = pygame.font.Font("freesansbold.ttf",24)
    WindowX = 10
    WindowY =  100
    WindowGap = 50
    #Messages to display:
    WindowOpener = MEDIUMFONT.render("CONTROLS WINDOW - ESC TO RETURN",True,RED)
    Snek1Keys = ALMOSTMEDIUMFONT.render("WASD To Control The BLUE Snek",True,CYAN) 
    Snek2Keys = ALMOSTMEDIUMFONT.render("IJKL To Control The GREEN Snek",True,GREEN)
    StartGame = ALMOSTMEDIUMFONT.render("ENTER OR SPACE To Start Game",True,ORANGE)
    PauseGame = ALMOSTMEDIUMFONT.render("H To Pause/UnPause Game",True,ORANGE)
        
    WindowOpenerRect = WindowOpener.get_rect()
    WindowOpenerRect.center = ((int(GAMEWIDTH/2)),30)
    #Display Snek1 Message
    Snek1KeysRect = Snek1Keys.get_rect()
    Snek1KeysRect.topleft = (WindowX,WindowY)
    #Display Snek2 Message
    Snek2KeysRect = Snek2Keys.get_rect()
    Snek2KeysRect.topleft = (WindowX,(WindowY + WindowGap))
    #Display StartGame message
    StartGameRect = StartGame.get_rect()
    StartGameRect.topleft = (WindowX,(WindowY + (2 * WindowGap)))
    #Display PauseGame message
    PauseGameRect = PauseGame.get_rect()
    PauseGameRect.topleft = (WindowX,(WindowY + (3 * WindowGap)))

    while True:
        GameScreen.fill(BLACK)
        drawGrid()
        Snek1.UpdateScreen()
        Snek2.UpdateScreen()
        GameScreen.blit(WindowOpener,WindowOpenerRect)
        GameScreen.blit(Snek1Keys,Snek1KeysRect)
        GameScreen.blit(Snek2Keys,Snek2KeysRect)
        GameScreen.blit(StartGame,StartGameRect)
        GameScreen.blit(PauseGame,PauseGameRect)
        pygame.display.flip()

        for event in pygame.event.get(): 
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        if not GameMusicChannel.get_busy():
            GameMusicChannel.play(GameMusicSound)

def drawCredits(ScrollCounter):
    ScrollSpeed = 2 * ScrollCounter

    #If there is an easier way of doing this, it will need to be redone
    #Bigninning of the pain:
    HeaderSize = 40
    NameSize = 30
    HeaderGap = 60
    NameGap = 40
    HeaderColor = ORANGE
    NameColor = PURPLE

    CreditsList = []
    CreditsList.append(Text("CREDITS",HeaderColor,58,GAMEHEIGHT))
    HeaderSpace = HeaderGap + CreditsList[-1].Obj.height + CreditsList[-1].Y
    CreditsList.append(Text("ENGINEERS",HeaderColor,HeaderSize,HeaderSpace))
    NameSpace = NameGap + CreditsList[-1].Y
    CreditsList.append(Text("Woldorf",NameColor,NameSize,NameSpace))
    #CreditsList.append(Text("ARTISTS",ORANGE,HeaderSize,HeaderSpace))
    #CreditsList.append(Text("Woldorf",,NameSize,NameSpace))
    HeaderSpace = HeaderGap + CreditsList[-1].Y
    CreditsList.append(Text("DEVELOPERS",HeaderColor,HeaderSize,HeaderSpace))
    NameSpace = NameGap + CreditsList[-1].Y
    CreditsList.append(Text("Woldorf",NameColor,NameSize,NameSpace))
    HeaderSpace = HeaderGap + CreditsList[-1].Y
    CreditsList.append(Text("ORIGINAL CONCEPT",HeaderColor,HeaderSize,HeaderSpace))
    NameSpace = NameGap + CreditsList[-1].Y
    CreditsList.append(Text("Woldorf",NameColor,NameSize,NameSpace))
    NameSpace = NameGap + CreditsList[-1].Y
    CreditsList.append(Text("01c",NameColor,NameSize,NameSpace))
    HeaderSpace = HeaderGap + CreditsList[-1].Y
    CreditsList.append(Text("SPECIAL THANKS TO",HeaderColor,HeaderSize,HeaderSpace))
    NameSpace = NameGap + CreditsList[-1].Y
    CreditsList.append(Text("Brambrew",NameColor,NameSize,NameSpace))                 
    NameSpace = NameGap + CreditsList[-1].Y
    CreditsList.append(Text("KelserVin",NameColor,NameSize,NameSpace))                #WIll need double checked
    NameSpace = NameGap + CreditsList[-1].Y
    CreditsList.append(Text("Froststormer",NameColor,NameSize,NameSpace))             #Will need double checked
    HeaderSpace = HeaderGap + CreditsList[-1].Y
    CreditsList.append(Text("ESC TO EXIT CREDITS",RED,HeaderSize,HeaderSpace))
    #CreditsList.append(Text("",ORANGE,HeaderSize,HeaderSpace))
    #CreditsList.append(Text("",BLUE,NameSize,NameSpace))
    #NameSpace = NameGap + CreditsList[-1].Y
    #HeaderSpace = HeaderGap + CreditsList[-1].Y

    for Name in CreditsList:
        Name.UpdateScreen(ScrollSpeed)

    return CreditsList

def terminate():
    pygame.quit()
    sys.exit()

def makeFruits():
    x=random.randint(0, int(GAMEWIDTH / CELLSIZE)-1)
    y=random.randint(0, int(GAMEHEIGHT / CELLSIZE)-1)

    if random.randint(0,1000) == 1:
        Type = "Master"
    else:
        TypeList=["Normal","Speed","Normal"]
        Type = random.choice(TypeList)

    return {'x':x,'y':y,'Type':"Master"}

def KonamiChecker(KeyPresses,TicksPerSec):
    #Konami Code: wUaLsDdR
    #Konami Code checker:
    if KeyPresses == "wUaLsDdR":
        TicksPerSec=5
    else:
        TicksPerSec=10
    return TicksPerSec

def GetGameFile(Write = False, Snek1Score = None, Snek2Score = None):
        GameFileRead = open("SnekFiles/Scores.txt","r")
        GameFileList = GameFileRead.readlines()
        Placement = 0
        for line in GameFileList:
            if line == "--Snek1HighScore\n":
                Snek1HighScore = GameFileList[Placement + 1].replace("\n","")
            if line == "--Snek2HighScore\n":
                Snek2HighScore = GameFileList[Placement + 1].replace("\n","")
            Placement += 1

        if not Write:
            GameFileRead.close()
            return Snek1HighScore,Snek2HighScore
        else:
            GameFileRead.close()
            if Snek1HighScore == "None Set":
                Snek1HighScore = 0
                Snek2HighScore = 0

            if Snek1Score >= int(Snek1HighScore) and Snek2Score >= int(Snek2HighScore):
                GameFile = open("SnekFiles/Scores.txt","w")
                WriteLines = ["--Snek1HighScore\n",str(Snek1Score)+"\n","--Snek2HighScore\n",str(Snek2Score)+"\n"]
                GameFile = open("SnekFiles/Scores.txt","w")
                for Item in WriteLines:
                    GameFile.write(Item)
                GameFile.close()

def Runner(AppleCords,Snek1,Snek2,TicksPerSec):
    PlayerWon = False
    Paused = False
    Color1Direction = True
    Color2Direction = True
    Color3Direction = True
    CreditPlacement = 0

    while True:
        #Event handling loop
        for event in pygame.event.get(): 
            if event.type == QUIT:
                return Snek1, Snek2
            elif event.type == KEYDOWN:
                #Snek 1 direction settings:
                if not Paused:
                    Snek1.ChangeDirection(event.key)
                    Snek2.ChangeDirection(event.key)

                if event.key == K_ESCAPE:
                    return Snek1,Snek2
                elif event.key == K_h:
                    Paused = not Paused

        if not PlayerWon:
                GameOver, AppleCords, TicksPerSec, PlayerWon = Snek1.CollisionDetection(Snek2,AppleCords,TicksPerSec,PlayerWon)
                if GameOver:
                    Snek1.CordsList.append("+1")
                    return Snek1, Snek2
                GameOver, AppleCords, TicksPerSec, PlayerWon = Snek2.CollisionDetection(Snek1,AppleCords,TicksPerSec,PlayerWon)
                if GameOver:
                    Snek2.CordsList.append("+1")
                    return Snek1,Snek2
                if not Paused:
                    Snek1.Move()
                    Snek2.Move()

        Placement = 0
        for color in RAINBOW:
            if Placement == 0:
                if color >= 255:
                    color = 250
                    Color1Direction = False
                elif color < 15:
                    color = 15
                    Color1Direction = True
                
                if not Color1Direction:
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
                
                if not Color2Direction:
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
                
                if not Color3Direction:
                    color -= 5
                elif Color3Direction == True:
                    color += 5
            
            RAINBOW[Placement] = color
            Placement += 1

        #Draw everything
        GameScreen.fill(BLACK)
        drawGrid()
        Snek1.UpdateScreen()
        Snek2.UpdateScreen()
        drawFruits(AppleCords)
        Snek1.DrawLable()
        Snek2.DrawLable()
        if Paused:
            drawPaused()
        if PlayerWon:
            CreditPlacement += 1
            drawCredits(CreditPlacement)

        pygame.display.flip()

        #Play the music if not already playing:
        if not PlayerWon:
            if not GameMusicChannel.get_busy():
                GameMusicChannel.play(GameMusicSound)
        else:
            if GameMusicChannel.get_sound() != WinnerAppleSound:
                GameMusicChannel.set_volume(0.2)
                GameMusicChannel.play(WinnerAppleSound)

        TicksPerSecCLOCK.tick(TicksPerSec)

while True:
    TicksPerSec = 10

    Snek1 = Snek(GREEN, DARKGREEN, 1,DARKGREEN)
    Snek2 = Snek(BLUE, NAVYBLUE, 2, CYAN)
    Snek1.MakeCordinates()
    Snek2.MakeCordinates()

    KonamiList=drawStartScreen(Snek1,Snek2)
    TicksPerSec=KonamiChecker(KonamiList,TicksPerSec)
    Snek1, Snek2 = Runner(makeFruits(),Snek1,Snek2,TicksPerSec)

    GetGameFile(True, len(Snek1.CordsList), len(Snek2.CordsList))