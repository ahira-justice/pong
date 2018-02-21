"""
    Pong
    By Justice Ahira -> E-mail:justiceahira@gmail.com
    Student, Department of Computer Science, graduating class of 2017/2018,
    Faculty of Science, University of Ibadan, Ibadan.

    start May 5, 2017.
    end June 6, 2017.
"""

import os
import pygame
import sys
import time
import random

from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centre game window.

FPS = 400  # Frames per sec.
FPSCLOCK = pygame.time.Clock()

# Defining constant variables for color
#              R    G    B
ASH =        (128, 128, 128)
Ash =        ( 50,  50,  50)
White =      (255, 255, 255)
Black =      (  0,   0,   0)
Blue =       ( 50,  50, 255)
Red =        (255,  50,  50)

BGCOLOR = Ash

FIELDSIZE = 400, 600
WINDOWWIDTH, WINDOWHEIGHT = 600, 600

PRINTFONTSIZE = 35
SMALLFONTSIZE = 10
BASICFONTSIZE = 30
BIGFONTSIZE = 50
ALTFONTSIZE = 20
ALTFONT1SIZE = 16

TOP = 'TOP'
BOTTOM = 'BOTTOM'

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

YES = 'YES'
NO = 'NO'

EASY = 'EASY'
MEDIUM = 'MEDIUM'
HARD = 'HARD'

PLAYER = 'PLAYER'
COMPUTER = 'COMPUTER'


def main():
    global DISPLAYSURF, BASICFONT, BIGFONT, SMALLFONT, PRINTFONT, ALTFONT, ALTFONT1, collide, _collide
    pygame.init()

    # Setting up the GUI window.
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('PONG')
    SMALLFONT = pygame.font.SysFont('calibri', SMALLFONTSIZE)
    BASICFONT = pygame.font.SysFont('calibri', BASICFONTSIZE)
    BIGFONT = pygame.font.SysFont('calibri', BIGFONTSIZE)
    PRINTFONT = pygame.font.SysFont('calibri', PRINTFONTSIZE)
    ALTFONT = pygame.font.Font('fonts/stroke_dimension.ttf', ALTFONTSIZE)
    ALTFONT1 = pygame.font.Font('fonts/stroke_dimension.ttf', ALTFONT1SIZE)

    #pygame.display.set_icon(pygame.image.load('images/gameicon.png'))

    collide = pygame.mixer.Sound('sound/collide.ogg')
    _collide = pygame.mixer.Sound('sound/_collide.ogg')

    iCECorpAnim()
    # Run the main game.
    while True:
        checkForQuit()
        if runGame() is False:
            break
    terminate()


def runGame():
    global paddleSize, ballSize, playerPaddleCoord, computerPaddleCoord, ballCoord, computerPaddle, playerPaddle, playerPiece, computerPiece, playerScore, computerScore

    playerScore, computerScore = 0, 0

    ballSize = [5, 5]
    paddleSize = [50, 3]

    mousex, mousey = 0, 0

    serve = False
    moveLeft = False
    moveRight = False

    cMoveLeft = False
    cMoveRight = False

    DISPLAYSURF.fill(BGCOLOR)
    drawField(FIELDSIZE)
    playerPiece, computerPiece = enterPlayerPiece()

    DISPLAYSURF.fill(BGCOLOR)
    drawField(FIELDSIZE)

    server = [PLAYER, COMPUTER][random.randint(0, 1)]

    difficulty = chooseComputerDiff()

    if difficulty is 'EASY':
        cspeed = 0.4
        cr = 8, 10
    elif difficulty is 'MEDIUM':
        cspeed = 0.5
        cr = 5, 10
    elif difficulty is 'HARD':
        cspeed = 0.6
        cr = 3, 10

    pspeed = 0.5

    while True:  # main game loop.
        DISPLAYSURF.fill(BGCOLOR)
        drawField(FIELDSIZE)

        playerPaddleColor = Blue
        computerPaddleColor = Red

        mouseClicked = False
        pScores, cScores = False, False

        if not serve:
            m = 5
            playerPaddleCoord, computerPaddleCoord = setPaddles(playerPiece)
            if playerPiece is 'TOP':  # computerPiece is BOTTOM
                if server is 'PLAYER':
                    ballxDir = RIGHT
                    ballyDir = DOWN
                    ballx = playerPaddleCoord[0] + int(paddleSize[0] / 2) - int(ballSize[0] / 2)
                    bally = playerPaddleCoord[1] + paddleSize[1] + 2
                elif server is 'COMPUTER':
                    ballxDir = LEFT
                    ballyDir = UP
                    ballx = computerPaddleCoord[0] + int(paddleSize[0] / 2) - int(ballSize[0] / 2)
                    bally = computerPaddleCoord[1] - paddleSize[1] - 5
                ballCoord = (ballx, bally)

                def playerPaddle(coord):
                    return showPaddle(paddleSize, coord, playerPaddleColor)

                def computerPaddle(coord):
                    return showPaddle(paddleSize, coord, computerPaddleColor)

            elif playerPiece is 'BOTTOM':  # computerPiece is TOP
                if server is 'PLAYER':
                    ballxDir = LEFT
                    ballyDir = UP
                    ballx = playerPaddleCoord[0] + int(paddleSize[0] / 2) - int(ballSize[0] / 2)
                    bally = playerPaddleCoord[1] - paddleSize[1] - 5
                if server is 'COMPUTER':
                    ballxDir = RIGHT
                    ballyDir = DOWN
                    ballx = computerPaddleCoord[0] + int(paddleSize[0] / 2) - int(ballSize[0] / 2)
                    bally = computerPaddleCoord[1] + paddleSize[1] + 2
                ballCoord = (ballx, bally)

                def playerPaddle(coord):
                    return showPaddle(paddleSize, coord, playerPaddleColor)

                def computerPaddle(coord):
                    return showPaddle(paddleSize, coord, computerPaddleColor)
            default_ballpos = ballCoord

        ballRect = showBall(ballCoord)
        playerRect = playerPaddle(playerPaddleCoord)
        computerRect = computerPaddle(computerPaddleCoord)

        # event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos  # mousex & mousey assigned when there is a click.
                mouseClicked = True

            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                elif event.key == K_RETURN:
                    if not serve and server is 'PLAYER':
                        showBall(ballCoord)
                        playerPaddle(playerPaddleCoord)
                        computerPaddle(computerPaddleCoord)
                        displayScore([playerScore, computerScore], playerPiece)
                        pygame.display.update()
                        collide.play()
                        _collide.play()
                        serve = True

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False

                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_p:
                    pauseGame()
                if event.key == K_r:
                    displayScore([playerScore, computerScore], playerPiece)
                    if restart() is YES:
                        runGame()

        if not serve and server is 'COMPUTER':
            showBall(ballCoord)
            playerPaddle(playerPaddleCoord)
            computerPaddle(computerPaddleCoord)
            displayScore([playerScore, computerScore], playerPiece)
            pygame.display.update()
            pygame.time.wait(1500)
            collide.play()
            _collide.play()
            serve = True

        # engine code
        if serve:
            # code to move the player paddle.
            if moveLeft and playerPaddleCoord[0] > 110:
                playerPaddleCoord = (playerPaddleCoord[0] - pspeed, playerPaddleCoord[1])
            elif moveRight and playerPaddleCoord[0] < 440:
                playerPaddleCoord = (playerPaddleCoord[0] + pspeed, playerPaddleCoord[1])

            # code to move the computer paddle
            if computerPiece is 'TOP':
                x1, y1 = ballRect.midtop
                y = 20
                x = (y - y1 + m * x1) / m
                pointToReach = [int(x), int(y)]
                if computerRect.midbottom == pointToReach:
                    cMoveLeft = False
                    cMoveRight = False
                elif computerRect.midbottom[0] > pointToReach[0]:
                    cMoveLeft = True
                    cMoveRight = False
                elif computerRect.midbottom[0] < pointToReach[0]:
                    cMoveLeft = False
                    cMoveRight = True

                if cMoveLeft and computerPaddleCoord[0] > 110:
                    computerPaddleCoord = (computerPaddleCoord[0] - cspeed, computerPaddleCoord[1])
                elif cMoveRight and computerPaddleCoord[0] < 440:
                    computerPaddleCoord = (computerPaddleCoord[0] + cspeed, computerPaddleCoord[1])

            elif computerPiece is 'BOTTOM':
                x1, y1 = ballRect.midbottom
                y = WINDOWHEIGHT - 20 - paddleSize[1]
                x = (y - y1 + m * x1) / m
                pointToReach = [int(x), int(y)]
                if computerRect.midtop == pointToReach:
                    cMoveLeft = False
                    cMoveRight = False
                elif computerRect.midtop[0] > pointToReach[0]:
                    cMoveLeft = True
                    cMoveRight = False
                elif computerRect.midtop[0] < pointToReach[0]:
                    cMoveLeft = False
                    cMoveRight = True

                if cMoveLeft and computerPaddleCoord[0] > 110:
                    computerPaddleCoord = (computerPaddleCoord[0] - cspeed, computerPaddleCoord[1])
                elif cMoveRight and computerPaddleCoord[0] < 440:
                    computerPaddleCoord = (computerPaddleCoord[0] + cspeed, computerPaddleCoord[1])

            #  code to move the ball
            if playerPiece is 'TOP':  # computerPiece is BOTTOM
                if ballyDir is 'UP' and playerRect.colliderect(ballRect):
                    m = random.randint(4, 10)
                    ballyDir = DOWN

                    if ballRect.midtop[0] in range(playerRect.left - 3, playerRect.midbottom[0]):
                        ballxDir = LEFT
                    elif ballRect.midtop[0] in range(playerRect.midbottom[0], playerRect.right + 3):
                        ballxDir = RIGHT

                    collide.play()
                    _collide.play()

                elif ballyDir is 'DOWN' and computerRect.colliderect(ballRect):
                    m = random.randint(cr[0], cr[1])
                    ballyDir = UP

                    if ballRect.midbottom[0] in range(computerRect.left - 3, computerRect.midtop[0]):
                        ballxDir = LEFT
                    elif ballRect.midbottom[0] in range(computerRect.midtop[0], computerRect.right + 3):
                        ballxDir = RIGHT

                    collide.play()
                    _collide.play()

                if ballCoord[1] < 0:
                    ballyDir = DOWN
                    pScores = False
                    cScores = True
                    serve = False
                elif ballCoord[1] > 592:
                    ballyDir = DOWN
                    pScores = True
                    cScores = False
                    serve = False

            elif playerPiece is 'BOTTOM':  # computerPiece is TOP
                if ballyDir is 'UP' and computerRect.colliderect(ballRect):
                    m = random.randint(cr[0], cr[1])
                    ballyDir = DOWN

                    if ballRect.midtop[0] in range(computerRect.left, computerRect.midbottom[0] - 5):
                        ballxDir = LEFT
                    elif ballRect.midtop[0] in range(computerRect.midbottom[0] + 5, computerRect.right):
                        ballxDir = RIGHT
                    elif ballRect.midtop[0] in range(playerRect.midbottom[0] - 5, playerRect.midbottom[0] + 5):
                        ballxDir = [LEFT, RIGHT][random.randint(0, 1)]

                    collide.play()
                    _collide.play()
                elif ballyDir is 'DOWN' and playerRect.colliderect(ballRect):
                    m = random.randint(4, 10)
                    ballyDir = UP

                    if ballRect.midbottom[0] in range(playerRect.left, playerRect.midtop[0] - 5):
                        ballxDir = LEFT
                    elif ballRect.midbottom[0] in range(playerRect.midtop[0] + 5, playerRect.right):
                        ballxDir = RIGHT
                    elif ballRect.midbottom[0] in range(playerRect.midtop[0] - 5, playerRect.midtop[0] + 5):
                        ballxDir = [LEFT, RIGHT][random.randint(0, 1)]

                    collide.play()
                    _collide.play()

                if ballCoord[1] < 0:
                    ballyDir = UP
                    pScores = True
                    cScores = False
                    serve = False
                elif ballCoord[1] > 592:
                    ballyDir = UP
                    pScores = False
                    cScores = True
                    serve = False

        ballCoord, ballxDir = moveBall(ballxDir, ballyDir, ballCoord, default_ballpos, serve, server, m)

        playerScore, computerScore = updateScore(pScores, cScores, playerScore, computerScore)
        displayScore([playerScore, computerScore], playerPiece)

        totalScore = playerScore + computerScore

        if pScores or cScores:
            msgx, msgy, text = scoreMsg(playerPiece, pScores, cScores)
            printMsg(text, ALTFONT1, White, msgx, msgy)
            pygame.display.update()
            pygame.time.wait(1000)
            if totalScore % 5 == 0 and totalScore > 0 and not serve:
                if playerScore != 11 and computerScore != 11:
                    server = changeServer(server)
                    drawField(FIELDSIZE, False)
                    showBall(ballCoord)
                    playerPaddle(playerPaddleCoord)
                    computerPaddle(computerPaddleCoord)
                    displayScore([playerScore, computerScore], playerPiece)
                    printMsg('CHANGING SERVER', ALTFONT, White, WINDOWWIDTH/2, WINDOWHEIGHT/2 - 10)
                    pygame.display.update()
                    pygame.time.wait(1500)

        game_over = gameover([playerScore, computerScore])
        while game_over:
            checkForQuit()
            if playerScore > computerScore:
                text = 'YOU WIN'
            else:
                text = 'YOU LOSE'
            printMsg(text, ALTFONT, White, WINDOWWIDTH/2, WINDOWHEIGHT/2 - 50)

            play_again = playAgain()
            if play_again is 'YES':
                return True
            elif play_again is 'NO':
                return False

        checkForQuit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def ball(size, offset, color):
    ballRect = Rect((offset[0], offset[1], size[0], size[1]))
    pygame.draw.rect(DISPLAYSURF, color, ballRect)
    return ballRect


def showBall(offset):
    return ball(ballSize, offset, White)


def moveBall(XDIR, YDIR, oldpos, default_ballpos, serve, server, m):
    x1, y1 = oldpos[0], oldpos[1]
    dy = 1.5
    dx = dy / m
    if serve is True:
        if YDIR is 'UP':
            y2 = y1 - dy
        elif YDIR is 'DOWN':
            y2 = y1 + dy

        if XDIR is 'LEFT':
            x2 = x1 - dx
        elif XDIR is 'RIGHT':
            x2 = x1 + dx

        if x1 < 100:
            collide.play()
            _collide.play()
            XDIR = RIGHT
        elif x1 > 492:
            collide.play()
            _collide.play()
            XDIR = LEFT
        newpos = x2, y2
        return newpos, XDIR
    return default_ballpos, XDIR


def showPaddle(size, offset, color):
    paddleRect = Rect(offset[0], offset[1], size[0], size[1])
    pygame.draw.rect(DISPLAYSURF, color, paddleRect)
    return paddleRect


def setPaddles(playerPiece):
    paddle1Coord = (int(WINDOWWIDTH / 3), 20)
    paddle2Coord = (2 * int(WINDOWWIDTH / 3) - 50, WINDOWHEIGHT - 20 - paddleSize[1])
    if playerPiece is 'TOP':  # computerPiece is BOTTOM
        return paddle1Coord, paddle2Coord
    elif playerPiece is 'BOTTOM':  # computerPiece is TOP
        return paddle2Coord, paddle1Coord


def drawField(size, centerline=True):
    offset = (100, 0)
    pygame.draw.rect(DISPLAYSURF, White, (offset[0], offset[1], size[0], size[1]), 1)
    pygame.draw.rect(DISPLAYSURF, Black, (offset[0] + 1, offset[1], size[0] - 2, size[1]))
    if centerline:
        pygame.draw.line(DISPLAYSURF, White, (100 + 1, 300), (500 - 1, 300), 1)
    elif not centerline:
        pygame.draw.line(DISPLAYSURF, White, (100 + 1, 300), (230, 300), 1)
        pygame.draw.line(DISPLAYSURF, White, (370, 300), (500 - 1, 300), 1)


def gameover(scores):
    if scores[0] == 11:
        return True
    elif scores[1] == 11:
        return True
    return False


def changeServer(server):
    if server is 'PLAYER':
        return COMPUTER
    elif server is 'COMPUTER':
        return PLAYER


def updateScore(pScores, cScores, playerScore, computerScore):
    if pScores:
        playerScore += 1
    elif cScores:
        computerScore += 1
    return playerScore, computerScore


def displayScore(scores, playerPiece):
    if playerPiece is 'TOP':  # computerPiece is BOTTOM
        printMsg(str(scores[0]), BASICFONT, White, 80, 50)
        printMsg(str(scores[1]), BASICFONT, White, 80, 520)
    elif playerPiece is 'BOTTOM':  # computerPiece is TOP
        printMsg(str(scores[0]), BASICFONT, White, 80, 520)
        printMsg(str(scores[1]), BASICFONT, White, 80, 50)

    return


def pauseGame():
    mousex, mousey = 0, 0
    textSurf = ALTFONT.render('Paused', True, White, ASH)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    while checkForKeyPress() is None:
        mouseClicked = False
        checkForQuit()

        DISPLAYSURF.fill(BGCOLOR)
        drawField(FIELDSIZE)
        showBall(ballCoord)
        playerPaddle(playerPaddleCoord)
        computerPaddle(computerPaddleCoord)
        displayScore([playerScore, computerScore], playerPiece)
        OptionsRect = OptionsButton(ALTFONT1, 'OPTIONS', White, 530, 530)

        DISPLAYSURF.blit(textSurf, textRect)

        printMsg('Press a key to play.', SMALLFONT, ASH, 551, 581)
        printMsg('Press a key to play.', SMALLFONT, White, 550, 580)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos  # mousex & mousey assigned when there is a click.
                mouseClicked = True

        # code to operate the options button
        if mouseClicked and OptionsRect.collidepoint(mousex, mousey):
            OptionsPage(BASICFONT)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    drawField(FIELDSIZE)


def makeText(text, FONT, color, centerx, top):
    # create the Surface and Rect objects for some text.
    textSurf = FONT.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.midtop = (centerx, top)
    return textSurf, textRect


def printMsg(msg, FONT, color, centerx, top):
    textSurf, textRect = makeText(msg, FONT, color, centerx, top)
    DISPLAYSURF.blit(textSurf, textRect)


def scoreMsg(piece, pscores, cscores):
    if piece is 'TOP':
        if pscores:
            text = 'YOU SCORED'
            msgx = WINDOWWIDTH / 2
            msgy = WINDOWHEIGHT / 6
            return msgx, msgy, text
        elif cscores:
            text = 'PYTHON SCORED'
            msgx = WINDOWWIDTH / 2
            msgy = 5 * WINDOWHEIGHT / 6
            return msgx, msgy, text
    elif piece is 'BOTTOM':
        if pscores:
            text = 'YOU SCORED'
            msgx = WINDOWWIDTH / 2
            msgy = 5 * WINDOWHEIGHT / 6
            return msgx, msgy, text
        elif cscores:
            text = 'PYTHON SCORED'
            msgx = WINDOWWIDTH / 2
            msgy = WINDOWHEIGHT / 6
            return msgx, msgy, text


def OptionsButton(FONT, text, color, left, top):
    OptionsSurf = FONT.render(text, True, color, ASH)
    OptionsRect = OptionsSurf.get_rect()
    OptionsRect.topleft = (left, top)
    DISPLAYSURF.blit(OptionsSurf, OptionsRect)
    return OptionsRect


def OptionsPage(FONT):
    while checkForKeyPress() is None:
        checkForQuit()
        DISPLAYSURF.fill(BGCOLOR)

        textSurfa = FONT.render('PONG', True, White)
        textRecta = textSurfa.get_rect()
        textRecta.center = (WINDOWWIDTH / 2, 40)

        textSurfb = FONT.render('PONG', True, ASH)
        textRectb = textSurfb.get_rect()
        textRectb.center = (WINDOWWIDTH / 2 + 1, 40 + 1)

        DISPLAYSURF.blit(textSurfb, textRectb)
        DISPLAYSURF.blit(textSurfa, textRecta)

        printMsg('Press a key to continue.', SMALLFONT, ASH, 536, 581)
        printMsg('Press a key to continue.', SMALLFONT, White, 535, 580)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def iCECorpAnim():
    a, b, c = 50, 50, 50
    d, e, f = 50, 50, 50

    p, q, r = 50, 50, 50
    s, t, u = 50, 50, 50

    FinTime = time.time()
    IniTime = time.time()
    FiniTime = time.time()
    InitTime = time.time()
    startAnim = False
    while checkForKeyPress() is None:
        DISPLAYSURF.fill(BGCOLOR)
        checkForQuit()
        COLOR = (a, b, c)
        color = (d, e, f)

        sCOLOR = (p, q, r)
        scolor = (s, t, u)

        if FinTime - IniTime >= 1:
            checkForQuit()
            printMsg('\'iCE CORP', BIGFONT, color, 302, 202)
            printMsg('\'iCE CORP', BIGFONT, COLOR, 300, 200)

            printMsg('Press a key to play.', SMALLFONT, color, 551, 581)
            printMsg('Press a key to play.', SMALLFONT, COLOR, 550, 580)
            startAnim = True
        if a < 255 and startAnim:
            a += 1
            b += 1
            c += 1
        if e < 128 and startAnim:
            d += 1
            e += 1
            f += 1
        if FiniTime - InitTime >= 2.5:
            printMsg('PONG', PRINTFONT, scolor, 302, 352)
            printMsg('PONG', PRINTFONT, sCOLOR, 300, 350)
            if p < 255 and startAnim:
                p += 1
                q += 1
                r += 1
            if t < 128 and startAnim:
                s += 1
                t += 1
                u += 1
        FiniTime = time.time()
        FinTime = time.time()
        pygame.display.update()
        FPSCLOCK.tick(50)

    return


def enterPlayerPiece():
    # Draws the text and handles the mouse click events for letting
    # the player choose which paddle they want to be. Returns
    # [TOP, BOTTOM] if the player chooses to be Top,
    # [BOTTOM, TOP] if Bottom.

    # Create the text.
    xSurf = ALTFONT.render('   TOP   ', True, White, Blue)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 15)

    oSurf = ALTFONT.render('BOTTOM', True, Black, Red)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 15)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint((mousex, mousey)):
                    return [TOP, BOTTOM]
                elif oRect.collidepoint((mousex, mousey)):
                    return [BOTTOM, TOP]

        # Draw the screen.
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def chooseComputerDiff():
    # Draws the text and handles the mouse click events for letting
    # the player choose which difficulty they want to play. Returns
    # EASY or MEDIUM or HARD.

    # Create the text.
    xSurf = ALTFONT.render('EASY', True, White, ASH)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 25)

    ySurf = ALTFONT.render('MEDIUM', True, White, ASH)
    yRect = ySurf.get_rect()
    yRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    zSurf = ALTFONT.render('HARD', True, White, ASH)
    zRect = zSurf.get_rect()
    zRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 25)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint((mousex, mousey)):
                    return EASY
                elif yRect.collidepoint((mousex, mousey)):
                    return MEDIUM
                elif zRect.collidepoint((mousex, mousey)):
                    return HARD

        # Draw the screen.
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(ySurf, yRect)
        DISPLAYSURF.blit(zSurf, zRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def restart():
    # Draws the text and handles the mouse click events for letting
    # the player choose which if they want to play again.  Returns
    # YES if the player chooses to play again,
    # NO if not.

    # Create the text.
    textSurf = ALTFONT.render('restart?', True, White, ASH)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = ALTFONT.render('Yes', True, White, ASH)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 30, int(WINDOWHEIGHT / 2) + 40)

    oSurf = ALTFONT.render(' No ', True, White, ASH)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 30, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on an option.
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint((mousex, mousey)):
                    return YES
                elif oRect.collidepoint((mousex, mousey)):
                    return NO

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def playAgain():
    # Draws the text and handles the mouse click events for letting
    # the player choose which if they want to play again.  Returns
    # YES if the player chooses to play again,
    # NO if not.

    # Create the text.
    textSurf = ALTFONT.render('play again?', True, White, ASH)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = ALTFONT.render('Yes', True, White, ASH)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 30, int(WINDOWHEIGHT / 2) + 40)

    oSurf = ALTFONT.render(' No ', True, White, ASH)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 30, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on an option.
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint((mousex, mousey)):
                    return YES
                elif oRect.collidepoint((mousex, mousey)):
                    return NO

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
