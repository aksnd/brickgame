import pygame, sys,random,time
from pygame.locals import *
length_bar = 120 #작대기 길이
reallength = length_bar
nx = 190
ny = 25
#첫번째 버프때의 길이
#첫번째 디버프때의 길이
height_bar = 10 #작대기 높이
buff1time=1 #buff가 가동됬는지 안됬는지를 확인하기 위한변수 시간과 확인하는 변수로 구성되어있다.
buff2time=1
buffcheck1=False
buffcheck2=False
debuff3=False
debuff1time=1
debuff2time=1
debuff3time=1
debuffcheck1=False
highscore=0
debuffcheck2=False
debuffcheck3=False
gotoup=False #무조건 위로 보내는 버프에 사용되는 변수이다
gotodown=False
a=1 # a는 시작 화면을 띄우는 사진저장용
b=1 # b는 끝화면을 띄우는 사진저장용
c=1
CHANGE=1 #바꾸는 횟수를 저장하기 위한 변수
moveV = 2 #작대기 속도
radius = 5 #공 반지름
ballspeed =1 #공속도
life =3#생명
heartimg = pygame.transform.scale(pygame.image.load('heart.png'),(100,100)) #하트를 소환하기 위해 하트이미지 소환
downtime=2e9
downtime2=2e9
score =0 #점수
highspace0 = 50
highspace=50 #위쪽으로 띄운 정도 이자리에 스코어판이 나온다
Left = False #막대기의 왼쪽으로 보내기 위해넣은 변수
Right = False # 막대기의 오른쪽을 보내기 위해 넣은변수
start =False #시작 하기 위해서 넣은변수
#color     R    G    B
GREEN =  (  0, 255,   0)
RED =    (255,   0,   0)
BLUE =   (  0,   0, 255)
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
GRAY =   (116, 116, 116)
DISPLAYX = 1280
gameDISPLAYX = 900
DISPLAYY = 650 # 디스플레이의 크기
gameDISPLAYY = 650
backgroundimg = pygame.transform.scale(pygame.image.load('backgroundimage.PNG'),(DISPLAYX, DISPLAYY))
barimg = pygame.transform.scale(pygame.image.load('bar.png'),(length_bar,height_bar)) #작대기 이미지를 출력하자
BRICKXNUM = 15#벽돌 X개수
BRICKYNUM = 6#벽돌 Y개수
SPACE = 0# 좌우 여분공간
length_brick = (gameDISPLAYX-(2*SPACE))/BRICKXNUM #벽돌길이
height_brick = 40
BRICKPERSPACE=0
pygame.init()
fontis= pygame.font.Font('freesansbold.ttf',40)
textis =fontis.render('score:'+str(int(score)),True,BLUE,WHITE)
textrect = textis.get_rect()
textrect.centerx = DISPLAYX/6
textrect.centery = highspace/2 # textrect는 점수출력으로 된다
highscoreis=fontis.render('highscore'+str(int(highscore)),True,BLUE,WHITE)
highscorerect=highscoreis.get_rect()
highscorerect.centerx=DISPLAYX/2
highscorerect.centery=highspace/2
FPS = 700 #프레임 속도
FPS0 = 700
FPS2 = 315
FPS3 = 300 # FPS 계산하기 필수!
FPS4 = 224
FPS5 = 198
FPS6 = 166
pygame.mixer.music.load('aaa.mp3')
pygame.mixer.music.play(-1,0.0)
soundgun=pygame.mixer.Sound('beep1.ogg') #노래관련
x=1
y=1 #x와 y는 공속도에 이용한다
barx = (gameDISPLAYX-length_bar)/2+nx #작대기의 시작 x위치이다 중간위치이니 주의하자
bary = gameDISPLAYY-40+ny-50#작대기의 시작 y위치이다 이건 유지된다
bally = bary-radius
brickarray = [[0]*100 for j in range(100)]
itemarray = [[0]*100 for j in range(100)]
itemsitex = [[0]*100 for j in range(100)]
itemsitey = [[0]*100 for j in range(100)]
seeing = [[2]*100 for j in range(100)]
seeing2 = [[0]*100 for j in range(100)]  
scorescreen = pygame.Rect(0,-ny,gameDISPLAYX,highspace)
cannot = 1
nx = 190
ny = 0

def main():
    global highspace,DISPLAYSURF, BASICFONT, BASICFONT2, fpsClock
    pygame.init()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF =pygame.display.set_mode((DISPLAYX,DISPLAYY))
    pygame.display.set_caption('벽돌깨기')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BASICFONT2 = pygame.font.Font('freesansbold.ttf', 40)
    for i in range (BRICKYNUM):
        for j in range (BRICKXNUM):
            brickarray[j][i] = pygame.Rect((length_brick)*j+SPACE+nx,i*(height_brick)+SPACE+highspace+ny,length_brick-BRICKPERSPACE,height_brick-BRICKPERSPACE)#벽돌소환
            seeing[j][i]=1
            pygame.draw.rect(DISPLAYSURF,(10*i, 10*j, 0),brickarray[j][i])
    #pygame.draw.polygon(DISPLAYSURF,RED,((barx,bary),(barx,bary+height_bar),(barx+length_bar,bary+height_bar),(barx+length_bar,bary))) #작대기 소환
    intro()
    StartScreen()
    game()


def brickchecking():
    global cannot, CHANGE,y,x,k,seeing,seeing2,itemsitex,itemsitey,brickarray,DISPLAYSURF,itemarray, ballx,bally,score
    for i in range (BRICKYNUM):
        for j in range (BRICKXNUM):
            if(((brickarray[j][i].left-2<=ballx<=brickarray[j][i].left+2) or (brickarray[j][i].right-2<=ballx<=brickarray[j][i].right+2)) and (bally >= brickarray[j][i].top) and (bally<=brickarray[j][i].bottom) and (seeing[j][i]==1)):
                k = random.randint(0, 2)
                if(cannot == 1 and k == 0):
                    itemsitex[j][i] = (length_brick)*j+SPACE+nx+(length_brick-BRICKPERSPACE)/3
                    itemsitey[j][i] = i*(height_brick)+SPACE+ny+highspace+(height_brick-BRICKPERSPACE)/3
                    itemarray[j][i] = pygame.Rect(itemsitex[j][i], itemsitey[j][i], (length_brick-BRICKPERSPACE)/3, (height_brick-BRICKPERSPACE)/3)
                    pygame.draw.rect(DISPLAYSURF,BLUE,itemarray[j][i])
                    seeing2[j][i]=1
                if(cannot == 1 and k == 1):
                    itemsitex[j][i] = (length_brick)*j+SPACE+nx+(length_brick-BRICKPERSPACE)/3
                    itemsitey[j][i] = i*(height_brick)+SPACE+highspace+ny+(height_brick-BRICKPERSPACE)/3
                    itemarray[j][i] = pygame.Rect(itemsitex[j][i], itemsitey[j][i], (length_brick-BRICKPERSPACE)/3, (height_brick-BRICKPERSPACE)/3)
                    pygame.draw.rect(DISPLAYSURF,BLUE,itemarray[j][i])
                    seeing2[j][i]=2
                if((CHANGE==1) and (brickarray[j][i].left-2<=ballx<=brickarray[j][i].left+2)):
                    CHANGE=0
                    vxleft()
                    ballx=brickarray[j][i].left
                if((CHANGE==1) and (brickarray[j][i].right-2<=ballx<=brickarray[j][i].right+2)):
                    CHANGE=1
                    vxright()
                    ballx=brickarray[j][i].right
                if cannot == 1:
                    seeing[j][i]=0
                    soundgun.play()
                    score +=100
                
                #pygame.draw.rect(DISPLAYSURF,BLACK,brickarray[j][i])
            elif((ballx>=brickarray[j][i].left) and (ballx<=brickarray[j][i].right) and ((brickarray[j][i].top-2<=bally <= brickarray[j][i].top+2) or (brickarray[j][i].bottom-2<=bally<=brickarray[j][i].bottom+2))and(seeing[j][i]==1)):
                k = random.randint(0, 3)
                if(cannot == 1 and k == 0):
                    itemsitex[j][i] = (length_brick)*j+SPACE+nx+(length_brick-BRICKPERSPACE)/3
                    itemsitey[j][i] = i*(height_brick)+SPACE+ny+highspace+(height_brick-BRICKPERSPACE)/3
                    itemarray[j][i] = pygame.Rect(itemsitex[j][i], itemsitey[j][i], (length_brick-BRICKPERSPACE)/3, (height_brick-BRICKPERSPACE)/3)
                    pygame.draw.rect(DISPLAYSURF,BLUE,itemarray[j][i])
                    seeing2[j][i]=1
                elif(cannot == 1 and k == 1):
                    itemsitex[j][i] = (length_brick)*j+SPACE+nx+(length_brick-BRICKPERSPACE)/3
                    itemsitey[j][i] = i*(height_brick)+SPACE+ny+highspace+(height_brick-BRICKPERSPACE)/3
                    itemarray[j][i] = pygame.Rect(itemsitex[j][i], itemsitey[j][i], (length_brick-BRICKPERSPACE)/3, (height_brick-BRICKPERSPACE)/3)
                    pygame.draw.rect(DISPLAYSURF,RED,itemarray[j][i])
                    seeing2[j][i]=2
                if(CHANGE==1 and brickarray[j][i].bottom-2<=bally<=brickarray[j][i].bottom+2):
                    CHANGE=0
                    vydown()
                    bally=brickarray[j][i].bottom
                elif(CHANGE==1 and brickarray[j][i].top-2<=bally <= brickarray[j][i].top+2):
                    CHANGE=0
                    vyup()
                    bally=brickarray[j][i].top
                if cannot == 1:
                    seeing[j][i] = 0
                    soundgun.play()
                    score += 100
y=1
def vxright():
    global y,x,FPS
    if(x==1 or x==2 or x==3):
        x=random.randint(1,3)
    elif(x==-1 or x==-2 or x == -3):
        x=random.randint(1,3)
    if(y==1 or y==2 or y==3):
        y=random.randint(1,3)
    elif(y==-1 or y==-2 or y ==-3):
        y=random.randint(-3,-1)
    if((x==1 or x==-1) and (y==1 or y==-1)):
        x = x * 2
        y = y * 2
    if (x == 2 or x == -2) or (y == -2 or y == 2):
        FPS = FPS2
        if (x == 2 or x == -2) and (y == -2 or y == 2):
            FPS = FPS3
    if ((x == 1 or x == -1) and (y == -3 or y == 3)) or ((x == -3 or x == 3) and (y == -1 or y == 1)):
        FPS = FPS4
    elif ((x == 2 or x == -2) and (y == -3 or y == 3)) or ((x == -3 or x == 3) and (y == -2 or y == 2)):
        FPS = FPS5
    elif (x == -3 or x == 3) and (y == 3 or y == -3):
        FPS = FPS6
    elif(x==1 or x==-1) and (y==1 or y==-1):
        FPS = FPS0
def vxleft():
    global y,x,FPS
    if(x==1 or x==2 or x==3):
        x=random.randint(-3,-1)
    elif(x==-1 or x==-2 or x == -3):
        x=random.randint(-3,-1)
    if(y==1 or y==2 or y==3):
        y=random.randint(1,3)
    elif(y==-1 or y==-2 or y ==-3):
        y=random.randint(-3,-1)
    if((x==1 or x==-1) and (y==1 or y==-1)):
        x = x * 2
        y = y * 2
    if (x == 2 or x == -2) or (y == -2 or y == 2):
        FPS = FPS2
        if (x == 2 or x == -2) and (y == -2 or y == 2):
            FPS = FPS3
    if ((x == 1 or x == -1) and (y == -3 or y == 3)) or ((x == -3 or x == 3) and (y == -1 or y == 1)):
        FPS = FPS4
    elif ((x == 2 or x == -2) and (y == -3 or y == 3)) or ((x == -3 or x == 3) and (y == -2 or y == 2)):
        FPS = FPS5
    elif (x == -3 or x == 3) and (y == 3 or y == -3):
        FPS = FPS6
    elif(x==1 or x==-1) and (y==1 or y==-1):
        FPS = FPS0
def vydown():
    global y,x,FPS
    if(x==1 or x==2 or x==3):
        x=random.randint(1,3)
    elif(x==-1 or x==-2 or x == -3):
        x=random.randint(-3,-1)
    if(y==1 or y==2 or y==3):
        y=random.randint(-3,-1)
    elif(y==-1 or y==-2 or y ==-3):
        y=random.randint(-3, -1)
    if((x==1 or x==-1) and (y==1 or y==-1)):
        x = x * 2
        y = y * 2
    if (x == 2 or x == -2) or (y == -2 or y == 2):
        FPS = FPS2
        if (x == 2 or x == -2) and (y == -2 or y == 2):
            FPS = FPS3
    if ((x == 1 or x == -1) and (y == -3 or y == 3)) or ((x == -3 or x == 3) and (y == -1 or y == 1)):
        FPS = FPS4
    elif ((x == 2 or x == -2) and (y == -3 or y == 3)) or ((x == -3 or x == 3) and (y == -2 or y == 2)):
        FPS = FPS5
    elif (x == -3 or x == 3) and (y == 3 or y == -3):
        FPS = FPS6
    elif(x==1 or x==-1) and (y==1 or y==-1):
        FPS = FPS0
def vyup():
    global y,x,FPS
    if(x==1 or x==2 or x==3):
        x=random.randint(1, 3)
    elif(x==-1 or x==-2 or x == -3):
        x=random.randint(-3, -1)
    if(y==1 or y==2 or y==3):
        y=random.randint(1, 3)
    elif(y==-1 or y==-2 or y ==-3):
        y=random.randint(1, 3)
    if((x==1 or x==-1) and (y==1 or y==-1)):
        x = x * 2
        y = y * 2
    if (x == 2 or x == -2) or (y == -2 or y == 2):
        FPS = FPS2
        if (x == 2 or x == -2) and (y == -2 or y == 2):
            FPS = FPS3
    if ((x == 1 or x == -1) and (y == -3 or y == 3)) or ((x == -3 or x == 3) and (y == -1 or y == 1)):
        FPS = FPS4
    elif ((x == 2 or x == -2) and (y == -3 or y == 3)) or ((x == -3 or x == 3) and (y == -2 or y == 2)):
        FPS = FPS5
    elif (x == -3 or x == 3) and (y == 3 or y == -3):
        FPS = FPS6
    elif(x==1 or x==-1) and (y==1 or y==-1):
        FPS = FPS0

def PressKey():
    global DISPLAYSURF
    #pressKeySurf = BASICFONT.render('Press any key to play', True, RED)
    #PressKeyRect = pressKeySurf.get_rect()
    #PressKeyRect.topleft = (DISPLAYX / 2, DISPLAYY - 200)
    #PressKeyRect.centerx = (DISPLAYX / 2)
    #DISPLAYSURF.blit(pressKeySurf, PressKeyRect)
    pygame.display.update()

def intro():
    c = pygame.transform.scale(pygame.image.load('hello world.png'),(DISPLAYX, DISPLAYY))
    DISPLAYSURF.blit(c,(0, 0))
    while(True):
        PressKey()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYUP:
                c = 0
                break
        if c == 0:
            break
    pygame.display.update()


def StartScreen():
    global a, DISPLAYSURF, DISPLAYX, DISPLAYY
    DISPLAYSURF.fill(BLACK)
    a = pygame.transform.scale(pygame.image.load('startimg.png'),(DISPLAYX, DISPLAYY))
    DISPLAYSURF.blit(a,(0, 0))
    while(True):
        PressKey()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYUP:
                a = 0
                break
            
        if a == 0:
            break
    pygame.display.update()

def GameOver():
    global DISPLAYSURF
    #pressKeySurf = BASICFONT2.render('GAME OVER', True, BLUE)
    b = pygame.transform.scale(pygame.image.load('gameover.png'),(DISPLAYX, DISPLAYY))
    DISPLAYSURF.blit(b,(0, 0))
    textis =fontis.render('score:'+str(int(score)),True,GREEN,BLACK)
    textrect = textis.get_rect()
    textrect.centerx = DISPLAYX/6
    textrect.centery = 30
    DISPLAYSURF.blit(textis,textrect)
    highscoreis =fontis.render('highscore:'+str(int(score)),True,BLUE,BLACK)
    highscorerect = textis.get_rect()
    highscorerect.centerx = DISPLAYX/2
    textrect.centery = 30
    DISPLAYSURF.blit(highscoreis,highscorerect)
    #PressKeyRect = pressKeySurf.get_rect()
    #PressKeyRect.topleft = (DISPLAYX / 2, DISPLAYY / 2)
    #PressKeyRect.centerx = (DISPLAYX / 2)
    #PressKeyRect.centery = (DISPLAYY / 2)
    #DISPLAYSURF.blit(pressKeySurf, PressKeyRect)
    pygame.display.update()

def FinishScreen():
    global reallength, score,downtime2,cannot, x, y, moveV, seeing2, itemsitey, itemarray,debuffcheck2,highspace,highscore,highspace0,downtime,itemsitex, CHANGE, start, Left, Right, BRICKYNUM, fpsClock,buffcheck1,gotoup,buffcheck2, BRICKXNUM, brickarray, ballx, bally, radius, barx, bary, length_bar,buffran,buff1time,buff2time,buffsee1,buffsee2, height_bar, ballspeed, life, seeing
    DISPLAYSURF.fill(BLACK)
    length_bar = 120 #작대기 길이
    reallength = length_bar
    nx = 190
    ny = 25
    #첫번째 버프때의 길이
    #첫번째 디버프때의 길이
    height_bar = 10 #작대기 높이
    buff1time=1 #buff가 가동됬는지 안됬는지를 확인하기 위한변수 시간과 확인하는 변수로 구성되어있다.
    buff2time=1
    buffcheck1=False
    buffcheck2=False
    debuff3=False
    debuff1time=1
    debuff2time=1
    debuff3time=1
    debuffcheck1=False
    debuffcheck2=False
    debuffcheck3=False
    gotoup=False #무조건 위로 보내는 버프에 사용되는 변수이다
    gotodown=False
    a=1 # a는 시작 화면을 띄우는 사진저장용
    b=1 # b는 끝화면을 띄우는 사진저장용
    c=1
    CHANGE=1 #바꾸는 횟수를 저장하기 위한 변수
    moveV = 2 #작대기 속도
    radius = 5 #공 반지름
    ballspeed =1 #공속도
    bally=bary-radius
    life =3#생명
    if(highscore<score):
        highscore=score
    heartimg = pygame.transform.scale(pygame.image.load('heart.png'),(100,100)) #하트를 소환하기 위해 하트이미지 소환
    downtime=2e9
    downtime2=2e9
    highspace0 = 50
    highspace=50 #위쪽으로 띄운 정도 이자리에 스코어판이 나온다
    Left = False #막대기의 왼쪽으로 보내기 위해넣은 변수
    Right = False # 막대기의 오른쪽을 보내기 위해 넣은변수
    for i in range (BRICKYNUM):
        for j in range (BRICKXNUM):
            brickarray[j][i] = pygame.Rect((length_brick)*j+SPACE+nx,i*(height_brick)+SPACE+highspace+ny,length_brick-BRICKPERSPACE,height_brick-BRICKPERSPACE)#벽돌소환
            seeing[j][i]=1
            pygame.draw.rect(DISPLAYSURF,(10*i, 10*j, 0),brickarray[j][i])
    while(True):
        GameOver()
        for event in pygame.event.get():
            if event.type==KEYUP:
                if event.key == K_SPACE:
                    b=0
                    break
            elif event.type== QUIT:
                pygame.quit()
                sys.exit()
        if b == 0:
            break
    score=0
    backgroundimg = pygame.transform.scale(pygame.image.load('backgroundimage.PNG'),(DISPLAYX, DISPLAYY))
    DISPLAYSURF.blit(backgroundimg,(0, 0))
    start=False
    pygame.display.update()
def buff1():
    global highspace0,highspace,buffran,buff1time,buff2time,length_bar,FPS,buffcheck1,buffcheck2,bufflength,gotoup,gotodown
    buffran=random.randint(1,2)
    if highspace <= highspace0:
        buffran = 1
    if buffran ==1:
        length_bar = length_bar * 4 / 3 # 그냥 줄이는 값
        buff1time = time.time()
        buffcheck1=True
    elif buffran ==2:
        highspace -= height_brick
        buffcheck2=True
    elif buffran ==3:
        gotoup=True # 그냥 줄이는 값
        buff2time = time.time()
        gotodown=False
        buffcheck2=True
def debuff1():
    global highspace,height_brick,cannot,buffran,debuff1time,debuff2time,length_bar,FPS,debuffcheck1,debuffcheck2,debufflength,gotodown,debuff3time,debuffcheck3,gotoup
    buffran=random.randint(1,2)
    if buffran ==1:
        length_bar = length_bar * 2 / 3# 그냥 줄이는 값
        debuff1time = time.time()
        debuffcheck1=True
    elif buffran ==2:
        highspace += height_brick
        debuffcheck2=True
    elif buffran==3:
        gotodown=True
        gotoup=False
        debuff3time = time.time()
        debuffcheck3=True
def buffdebuffcheck():
    global cannot,highspace, height_brick, length_bar,FPS,buff1time,buff2time,buffcheck1,buffcheck2,debuffcheck1,debuffcheck2,debuff1time,debuff2time,gotoup,gotodown,debuff3time,debuffcheck3
    if(buff1time +5<time.time() and buffcheck1==True):
        length_bar =int(reallength)
        buffcheck1 =False
    if(buff2time +10<time.time()and buffcheck2 == True):
        gotoup =False
        buffcheck2 =False
    if(debuff1time +5<time.time() and debuffcheck1==True):
        length_bar =int(reallength)
        debuffcheck1=False
    #if(debuff2time +10<time.time() and debuffcheck2==True):
        #debuffcheck2=False
    if(debuff3time +3<time.time() and debuffcheck3==True):
        gotodown=False
        debuffcheck3=False
def game():
    global reallength, downtime2,cannot, x, y, moveV, seeing2, itemsitey, highscore,itemarray,debuffcheck2,highspace,highspace0,downtime,itemsitex, CHANGE, start, Left, Right, BRICKYNUM, fpsClock,buffcheck1,gotoup,buffcheck2, BRICKXNUM, brickarray, ballx, bally, radius, barx, bary, length_bar,buffran,buff1time,buff2time,buffsee1,buffsee2, height_bar, ballspeed, life, seeing
    DISPLAYSURF.blit(backgroundimg,(0, 0))
    while(True):
        buffdebuffcheck()
        pygame.draw.rect(DISPLAYSURF, BLACK, (nx, ny, gameDISPLAYX, gameDISPLAYY))
        for i in range (BRICKYNUM):
            for j in range (BRICKXNUM):
                brickarray[j][i] = pygame.Rect((length_brick)*j+SPACE+nx,i*(height_brick)+SPACE+highspace+ny,length_brick-BRICKPERSPACE,height_brick-BRICKPERSPACE)#벽돌소환
        if(downtime+10<time.time() and start==True):
            highspace0 +=height_brick
            highspace +=height_brick
            downtime=time.time()
        if(downtime2+20<time.time() and start==True):
            length_bar -= 10
            reallength -= 10
            downtime2=time.time()
            #debuffcheck2=False
        #DISPLAYSURF.blit(backgroundimg,(0,0))
        scorescreen = pygame.Rect(nx,0,gameDISPLAYX,highspace+ny)
        pygame.draw.rect(DISPLAYSURF,WHITE,scorescreen) 
        for i in range (BRICKYNUM):
            for j in range (BRICKXNUM):# 벽돌들의 색깔을 결정해줌
                if(cannot == 1 and seeing2[j][i] == 1 and (barx-(length_brick-BRICKPERSPACE)/3 < itemsitex[j][i] < barx+length_bar+(length_brick-BRICKPERSPACE)/3 and bary-(height_brick-BRICKPERSPACE)/3 < itemsitey[j][i] < bary+height_bar+(height_brick-BRICKPERSPACE)/3)):
                    seeing2[j][i] = 0
                    buff1()
                elif(seeing2[j][i] == 1):
                    itemsitey[j][i] += 1
                    itemarray[j][i] = pygame.Rect(itemsitex[j][i], itemsitey[j][i], (length_brick-BRICKPERSPACE)/3, (height_brick-BRICKPERSPACE)/3)
                    pygame.draw.rect(DISPLAYSURF,BLUE,itemarray[j][i])
                if(cannot == 1 and seeing2[j][i] == 2 and (barx-(length_brick-BRICKPERSPACE)/3 < itemsitex[j][i] < barx+length_bar+(length_brick-BRICKPERSPACE)/3 and bary-(height_brick-BRICKPERSPACE)/3 < itemsitey[j][i] < bary+height_bar+(height_brick-BRICKPERSPACE)/3)):
                    seeing2[j][i] = 0
                    debuff1()
                elif(seeing2[j][i] == 2):
                    itemsitey[j][i] += 1
                    itemarray[j][i] = pygame.Rect(itemsitex[j][i], itemsitey[j][i], (length_brick-BRICKPERSPACE)/3, (height_brick-BRICKPERSPACE)/3)
                    pygame.draw.rect(DISPLAYSURF,RED,itemarray[j][i])
                if(seeing[j][i] == 1):
                    pygame.draw.rect(DISPLAYSURF,(40*i, 18*j, 255-40*i),brickarray[j][i])
        if(start == False): # 공의 시작 위치 결정
            ballx = barx + length_bar/2
            pygame.draw.circle(DISPLAYSURF,RED,(int(ballx),int(bally)), radius, 0)
            
        elif(start==True): #공의 이동에 관한 부분
            ballx = ballx + (ballspeed * x)
            bally = bally - (ballspeed * y)
            pygame.draw.circle(DISPLAYSURF,RED,(int(ballx),int(bally)), radius, 0)
            if ballx<=nx+radius:
                vxright()
                if(gotoup==True):
                    vyup()
                if(gotodown==True):
                    vydown()
            elif ballx >=gameDISPLAYX+nx-radius:
                vxleft()
                if(gotoup==True):
                    vyup()
                if(gotodown==True):
                    vydown()
            if bally < radius + ny + highspace:
                vydown()
                
            if bally > gameDISPLAYY+ny-radius:
                for i in range (BRICKYNUM):
                    for j in range (BRICKXNUM):
                        if(seeing2[j][i] == 1):
                            seeing2[j][i] = 0
                        elif(seeing2[j][i] == 2):
                            seeing2[j][i] = 0
                if(life!=1):
                    pygame.time.wait(500)
                    life-=1
                    downtime=time.time()
                    downtime2=time.time()
                    start=False
                    length_bar=reallength
                    y=-y
                    ballx=barx + length_bar/2
                    bally=bary-radius
                
                elif(life==1):
                    #pygame.mixer.music.stop()
                    FinishScreen()
                    life=3
                    continue
                    
        if bary<bally+radius<bary+4 and barx-2<ballx<barx+length_bar+2:
            vyup()
        #pygame.draw.polygon(DISPLAYSURF,RED,((barx,bary),(barx,bary+height_bar),(barx+length_bar,bary+height_bar),(barx+length_bar,bary)))
        brickchecking()
        for event in pygame.event.get():
            if event.type==KEYUP:
                if event.key == K_LEFT:
                    Left=False
                if event.key == K_RIGHT:
                    Right=False
                if event.key == K_SPACE:
                    start=True
                    downtime=time.time()
                    downtime2=time.time()
            if event.type==KEYDOWN:
                if event.key == K_LEFT and barx > 0:
                    Left=True
                elif event.key == K_RIGHT and barx < DISPLAYX-length_bar:
                    Right=True
            if event.type== QUIT:
                pygame.quit()
                sys.exit()
        if Left==True and barx >nx+moveV:
            barx = barx -moveV
        elif Right==True and barx<gameDISPLAYX+nx-length_bar-moveV:
            barx = barx +moveV
        CHANGE=1
        #pygame.draw.polygon(DISPLAYSURF,RED,((barx,bary),(barx,bary+height_bar),(barx+length_bar,bary+height_bar),(barx+length_bar,bary)))
        barimg = pygame.transform.scale(pygame.image.load('bar.png'),(int(length_bar),height_bar))
        DISPLAYSURF.blit(barimg,(barx,bary))
        if(FPS == FPS2):
            moveV=3
        elif(FPS == FPS3 or FPS == FPS4): 
           moveV = 4
        elif(FPS == FPS6 or FPS == FPS5):
            moveV = 5
        else:
            moveV = 2
        if(highscore<score):
            highscore=score
        textis =fontis.render('score:'+str(int(score)),True,BLACK,WHITE)
        textrect = textis.get_rect()
        textrect.centerx = gameDISPLAYX/12+nx+40
        textrect.centery = 20+ny
        DISPLAYSURF.blit(textis,textrect)
        highscoreis =fontis.render('highscore:'+str(int(highscore)),True,BLACK,WHITE)
        highscorerect = textis.get_rect()
        highscorerect.centerx = gameDISPLAYX/3+nx+50
        highscorerect.centery = 20+ny
        DISPLAYSURF.blit(highscoreis,highscorerect)
        for z in range(life):
            DISPLAYSURF.blit(heartimg,(DISPLAYX*3/6+50*(z-1)+nx+30,-30+ny))
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
