#Run a graphic version of the game instead off running in terminal
import pygame as pg
import sys
from Game4InLine import Game4InLine as G4
from MCTS import MCTS 


pg.init()
pg.display.set_caption("Connect-4")
WIDTH, HEIGHT = 1200,850
WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
FPS = 120
TIME_MCTS = 5 #time for the MCTS algo to execute

#fonts
FONT = pg.font.SysFont("Brush Script MT Italic",90)


#Colors
RED = (255, 0, 0)
WHITE = (255,255,255)
BLACK = (0,0,0)

#images
RC = pg.image.load(("assets/coin-red.png"))
YC = pg.image.load(("assets/coin-yellow.png"))
DEF_BACK = pg.image.load(("assets/background.png"))
BOARD_PVP = pg.image.load(("assets/GameBoard.png"))
BOARD_PVIA = pg.image.load(("assets/GameBoardIA.png"))
TO_PLAY = pg.image.load(("assets/playerToplay.png"))
PLAY_AGAIN = pg.image.load(("assets/PlayAgain.png"))
DRAW = pg.image.load(("assets/draw.png"))
P1 = pg.image.load(("assets/winp1.png"))
P2 = pg.image.load(("assets/winp2.png"))
IA = pg.image.load(("assets/winIA.png"))


#drawing func
def draw_extras(game: G4,score: list[int]):
    #pieces on the board
    pieces = {"X":RC, "O":YC}
    for i in range(len(game.board)-1,-1,-1):
        for j in range(len(game.board[0])):
            if game.board[i][j] != "-":
                WINDOW.blit(pieces[game.board[i][j]], (226+(125*j),95+(125*i)))
    over_col(game)

    #arrow to know player turn
    if game.turn:
        WINDOW.blit(TO_PLAY, (124,701))
    else:
        WINDOW.blit(TO_PLAY, (124,593))

    #score
    img = FONT.render(f"{score[0]} - {score[1]}", True, WHITE)
    WINDOW.blit(img, (25,140))


def over_col(game: G4):
    pieces = {0:RC, 1:YC}
    mx,my = pg.mouse.get_pos()

    c1 = pg.Rect(220,75,120,750)
    if c1.collidepoint(mx,my): WINDOW.blit(pieces[game.turn], (226,15))
    c2 = pg.Rect(345,75,120,750)
    if c2.collidepoint(mx,my): WINDOW.blit(pieces[game.turn], (226+125,15))
    c3 = pg.Rect(470,75,120,750)
    if c3.collidepoint(mx,my): WINDOW.blit(pieces[game.turn], (226+(125*2),15))
    c4 = pg.Rect(595,75,120,750)
    if c4.collidepoint(mx,my): WINDOW.blit(pieces[game.turn], (226+(125*3),15))
    c5 = pg.Rect(720,75,120,750)
    if c5.collidepoint(mx,my): WINDOW.blit(pieces[game.turn], (226+(125*4),15))
    c6 = pg.Rect(845,75,120,750)
    if c6.collidepoint(mx,my): WINDOW.blit(pieces[game.turn], (226+(125*5),15))
    c7 = pg.Rect(970,75,120,750)
    if c7.collidepoint(mx,my): WINDOW.blit(pieces[game.turn], (226+(125*6),15))

    


#main loops
def start_menu():
    clock = pg.time.Clock()
    B_pvp = pg.Rect(60,510,500,300)
    B_pvia = pg.Rect(640,510,500,300)

    while True:
        WINDOW.blit(DEF_BACK, (0,0))
        mx,my = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if B_pvp.collidepoint(mx,my):
                        pvp()

                    if B_pvia.collidepoint(mx,my):
                        pvia()


        pg.display.update()
        clock.tick(FPS)


def pvp():
    game = G4(6,7)
    clock = pg.time.Clock()
    score = [0,0]
    B_menu = pg.Rect(14,359,185,198)
    B_pl_ag = pg.Rect(525,455,250,125)
    res_game = 0

    while True:
        WINDOW.blit(BOARD_PVP, (0,0))
        draw_extras(game,score)

        
        if res_game:
            if res_game == 2: # draw
                WINDOW.blit(DRAW,(360,205))
            else: #some1 win
                score[game.turn-1] += 1
                if game.turn: WINDOW.blit(P1,(360,205))
                else: WINDOW.blit(P2,(360,205))
            #update score view
            pg.draw.rect(WINDOW, BLACK, pg.Rect(25,140,150,100))
            text = FONT.render(f"{score[0]} - {score[1]}", True, WHITE)
            WINDOW.blit(text, (25,140))
            WINDOW.blit(PLAY_AGAIN,(525,455))
            
            #make a cicle to wait for a option (play again or go back to menu)
            next_event = False
            while not next_event:
                mx,my = pg.mouse.get_pos()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            return
                        
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if B_menu.collidepoint(mx,my):
                                return
                            if B_pl_ag.collidepoint(mx,my):
                                game = G4(6,7)
                                next_event = True
                                res_game = 0

                pg.display.update()
                clock.tick(FPS)


        mx,my = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if B_menu.collidepoint(mx,my):
                        return

                    col = column_played(mx,my)
                    if col in game.legal_moves():
                        game.play(col)
                        res_game = game.isFinished(col)


        pg.display.update()
        clock.tick(FPS)


def pvia():
    game = G4(6,7)
    clock = pg.time.Clock()
    score = [0,0]
    B_menu = pg.Rect(14,359,185,198)
    B_pl_ag = pg.Rect(525,455,250,125)
    res_game = 0
    ia_play = False

    while True:
        WINDOW.blit(BOARD_PVIA, (0,0))
        draw_extras(game,score)
    
        if res_game:
            if res_game == 2: # draw
                WINDOW.blit(DRAW,(360,205))
            else: #some1 win
                score[game.turn-1] += 1
                if game.turn: WINDOW.blit(P1,(360,205))
                else: WINDOW.blit(IA,(360,205))
            #update score view
            pg.draw.rect(WINDOW, BLACK, pg.Rect(25,140,150,100))
            text = FONT.render(f"{score[0]} - {score[1]}", True, WHITE)
            WINDOW.blit(text, (25,140))
            WINDOW.blit(PLAY_AGAIN,(525,455))
            
            #make a cicle to wait for a option (play again or go back to menu)
            next_event = False
            while not next_event:
                mx,my = pg.mouse.get_pos()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            return
                        
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if B_menu.collidepoint(mx,my):
                                return
                            if B_pl_ag.collidepoint(mx,my):
                                game = G4(6,7)
                                next_event = True
                                res_game = 0

                pg.display.update()
                clock.tick(FPS)


        if ia_play:
            tree = MCTS(game)
            tree.search(TIME_MCTS) 
            column = tree.best_move()
            game.play(column)
            res_game = game.isFinished(column)
            ia_play = False

        else:
            mx,my = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if B_menu.collidepoint(mx,my):
                            return

                        col = column_played(mx,my)
                        if col in game.legal_moves() and not ia_play:
                            game.play(col)
                            res_game = game.isFinished(col)
                            ia_play = True
                            WINDOW.blit(BOARD_PVIA, (0,0))
                            draw_extras(game,score)

        pg.display.update()
        clock.tick(FPS)


#game extra
def column_played(mx,my):
    c0 = pg.Rect(220,75,120,750)
    if c0.collidepoint(mx,my): return 0
    c1 = pg.Rect(345,75,120,750)
    if c1.collidepoint(mx,my): return 1
    c2 = pg.Rect(470,75,120,750)
    if c2.collidepoint(mx,my): return 2
    c3 = pg.Rect(595,75,120,750)
    if c3.collidepoint(mx,my): return 3
    c4 = pg.Rect(720,75,120,750)
    if c4.collidepoint(mx,my): return 4
    c5 = pg.Rect(845,75,120,750)
    if c5.collidepoint(mx,my): return 5
    c6 = pg.Rect(970,75,120,750)
    if c6.collidepoint(mx,my): return 6
    
    return -1


if __name__ == "__main__":
    start_menu()