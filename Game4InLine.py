from copy import deepcopy

#Human start and uses 'X' (player 1)
#AI go second and uses 'O' (player 2)

class Game4InLine:
    def __init__ (self,board,placed):
        self.rows = len(board)
        self.cols = len(board[0])
        self.board = deepcopy(board) #matrix representing the board
        self.placed = deepcopy(placed) #store the num of pieces per column
        self.pieces = ['X','O']
        self.turn = 0
        self.round = 0


    def legal_moves(self):
        legal=[]

        for i in range(self.cols):
            if self.placed[i]<self.rows:
                legal.append(i)
        
        return legal


    def childs(self):
        # returns the possible moves
        moves=self.legal_moves()
        children = []

        for col in moves:
            temp=deepcopy(self)
            children.append([temp.play(col),col])

        return children


    def play(self,col:int): #funcion to place pieces based on turn and column
        self.board[self.rows-self.placed[col]-1][col]=self.pieces[self.turn]
        self.placed[col]+=1
        self.round+=1
        self.turn = 1 if self.turn%2==0 else 0 #change turn
        return self


    def isFinished(self,col): #return 2 if game is a draw, True if last move was a winning one , False to keep playing
        played = self.pieces[self.turn-1]
        row = self.rows-self.placed[col]
    
        #Check Vertical    |
        consecutive = 1  # |
        tmprow = row     # |
        while tmprow+1 < self.rows and self.board[tmprow+1][col] == played:
            consecutive+=1
            tmprow+=1
        if consecutive >= 4:
            return True


        # Check horizontal  ----
        consecutive = 1
        tmpcol = col
        while tmpcol+1 < self.cols and self.board[row][tmpcol+1] == played:
            consecutive += 1
            tmpcol += 1
        tmpcol = col
        while tmpcol-1 >= 0 and self.board[row][tmpcol-1] == played:
            consecutive += 1
            tmpcol -= 1
        
        if consecutive >= 4:
            return True


        # Check diagonal   1          \
        consecutive = 1             #  \
        tmprow = row                 #  \
        tmpcol = col                  #  \
        while tmprow+1 < self.rows and tmpcol+1 < self.cols and self.board[tmprow+1][tmpcol+1] == played:
            consecutive += 1
            tmprow += 1
            tmpcol += 1
        tmprow = row
        tmpcol = col
        while tmprow-1 >= 0 and tmpcol-1 >= 0 and self.board[tmprow-1][tmpcol-1] == played:
            consecutive += 1
            tmprow -= 1
            tmpcol -= 1

        if consecutive >= 4:
            return True


        # Check diagonal   2          /
        consecutive = 1           #  /
        tmprow = row             #  /
        tmpcol = col            #  /
        while tmprow-1 >= 0 and tmpcol+1 < self.cols and self.board[tmprow-1][tmpcol+1] == played:
            consecutive += 1
            tmprow -= 1
            tmpcol += 1
        tmprow = row
        tmpcol = col
        while tmprow+1 < self.rows and tmpcol-1 >= 0 and self.board[tmprow+1][tmpcol-1] == played:
            consecutive += 1
            tmprow += 1
            tmpcol -= 1

        if consecutive >= 4:
            return True


        # Check for draw
        if(self.round==(self.rows*self.cols)): #maybe change this to other function
            return 2

        return False


    def heuristic_path(game,col):
        row = game.rows-game.placed[col]
    
        #caso for uma jogada para ganhar
        if game.isFinished(col):
            return -512 if game.turn%2==0 else 512


        #caso for uma jogada para nao perder
        points=0
        #horizontal
        for tpmcol in range(max(0,col-3),col+1):
            if tpmcol+3>game.cols-1: continue
            count_X=0
            count_O=0
            for j in range(4):
                if (game.board[row][tpmcol+j] == "X"):
                    count_X+=1
                if (game.board[row][tpmcol+j] == "O"):
                    count_O+=1
            
            #dar pontos
            h_value = getPoints_path(count_X,count_O)
            if abs(h_value) == 500:
                return -500 if game.turn%2==0 else 500
            elif h_value != 0:
                points=h_value
            
       

        #vertical
        count_X=0
        count_O=0
        for i in range(0,min(4,game.rows-row)):
            if (game.board[row+i][col] == "X"):
                count_X+=1
            if (game.board[row+i][col] == "O"):
                count_O+=1

        #dar pontos
        h_value = getPoints_path(count_X,count_O)
        if abs(h_value) == 500:
            return -500 if game.turn%2==0 else 500
        elif h_value != 0:
            points=h_value              
      
       

        #diagonal 1
        tmpcol = col
        tmprow = row
        i=0
        while(i<3 and tmprow>0 and tmpcol>0):
            tmpcol-=1
            tmprow-=1
            i+=1       
        while i>=0 and tmprow+3<game.rows and tmpcol+3<game.cols:
            i-=1
            count_X=0
            count_O=0
            for h in range(4):
                if (game.board[tmprow+h][tmpcol+h] == "X"):
                    count_X+=1
                if (game.board[tmprow+h][tmpcol+h] == "O"):
                    count_O+=1

            h_value = getPoints_path(count_X,count_O)
            if abs(h_value) == 500:
                return -500 if game.turn%2==0 else 500
            elif h_value != 0:
                points=h_value
            
            tmpcol+=1
            tmprow+=1


        #diagonal 2
        tmpcol = col
        tmprow = row
        i=0
        while i<3 and tmprow<game.rows-1 and tmpcol>0:
            tmpcol-=1
            tmprow+=1
            i+=1       

        while i>=0 and tmprow-3>=0 and tmpcol+3<game.cols:
            i-=1
            count_X=0
            count_O=0
            for h in range(4):
                if (game.board[tmprow-h][tmpcol+h] == "X"):
                    count_X+=1
                if (game.board[tmprow-h][tmpcol+h] == "O"):
                    count_O+=1

            h_value = getPoints_path(count_X,count_O)
            if abs(h_value) == 500:
                return -500 if game.turn%2==0 else 500
            elif h_value != 0:
                points=h_value 

            tmpcol+=1
            tmprow-=1 
    

        return abs(points)*(-1) if game.turn%2==0 else abs(points)


    def heuristic_points(game,col):
        '''

        '''
        points = 16 if game.pieces[game.turn] == 'X' else -16
        #horizontal
        for i in range(game.rows):
            for j in range(game.cols-3):
                count_X=0
                count_O=0
                for h in range(j,j+4):
                    if (game.board[i][h] == "X"):
                        count_X+=1
                    if (game.board[i][h] == "O"):
                        count_O+=1

                h_value = getPoints(count_X,count_O)
                if abs(h_value) == 512:
                    return h_value
                else:
                    points+=h_value
        
        #vertical
        for i in range(game.cols):
            for j in range(game.rows-3):
                count_X=0
                count_O=0                
                for h in range(j,j+4):
                    if (game.board[h][i] == "X"):
                        count_X+=1
                    if (game.board[h][i] == "O"):
                        count_O+=1

                h_value = getPoints(count_X,count_O)
                if abs(h_value) == 512:
                    return h_value
                else:
                    points+=h_value

        #diagonal 1
        for i in range(game.rows-3):
            for j in range(game.cols-3):
                count_X=0
                count_O=0  
                for h in range(4):
                    if (game.board[i+h][j+h] == "X"):
                        count_X+=1
                    if (game.board[i+h][j+h] == "O"):
                        count_O+=1

                h_value = getPoints(count_X,count_O)
                if abs(h_value) == 512:
                    return h_value
                else:
                    points+=h_value                    

        #diagonal 2
        for i in range(game.rows-3):
            for j in range(3,game.cols):
                count_X=0
                count_O=0  
                for h in range(4):
                    if (game.board[i+h][j-h] == "X"):
                        count_X+=1
                    if (game.board[i+h][j-h] == "O"):
                        count_O+=1

                h_value = getPoints(count_X,count_O)
                if abs(h_value) == 512:
                    return h_value
                else:
                    points+=h_value

        return points


    def A_star(self,heuristic):
        '''
        As in this project our A* only looks for its next best play without going in depht for a possible move from its the oponent
        We will use a list to store (heuristic(child),col) and sort it so the best play for 'O' is first and for 'X' is last
        A* will play as 'O' so the lower the score the best (due to our heuristic setup)
        return the col from best child 
        '''
        childs=self.childs()
        points_col=[]  #points_col[k][0] = points | points_col[k][1] = col
        a=[] #eliminar depois de debugg
        for i in range(len(childs)):
            col=childs[i][1]
            points_col.append([heuristic(state=(childs[i][0]),col=col),col])
            #para visualizar pontuacao de cada heuristica
            a.append([Game4InLine.heuristic_points((childs[i][0]),col),Game4InLine.heuristic_path((childs[i][0]),col),col+1]) #eliminar depois de debugg

        points_col.sort() #lowest points first

        #para visualizar pontuacao de cada heuristica
        print(f"h_dada, h_path, col:\n{a}")

        return (points_col[0][1]) if self.pieces[self.turn] == 'O' else (points_col[-1][1])


    def __str__(self): #override the print() method
        return print_board(self.board)






def getPoints(x,o):
    
    if (x == 4 and o == 0):
        return 512
    if (x == 3 and o == 0):
        return 50
    if (x == 2 and o == 0):
        return 10
    if (x == 1 and o == 0):
        return 1
    if (x == 0 and o == 1):
        return -1
    if (x == 0 and o == 2):
        return -10
    if (x == 0 and o == 3):
        return -50
    if (x == 0 and o == 4):
        return -512
    return 0

def getPoints_path(x,o):
    if(x==3 and o==1):
        return -500
    if(x==2 and o==1):
        return -100  
    if(x==1 and o==3):
        return 500
    if(x==1 and o==2):
        return 100 
    return 0


def print_board(board): #transform the game board from matrix to a visual representation
    board_str="|"
    for k in range(1,len(board[0])+1):
        board_str+=f" {k} |"
    board_str+="\n"
    for i in range(len(board)):
        board_str += "| "
        for j in range(len(board[i])):
            #board_str+=board[i][j]
            board_str += f"{board[i][j]} | "
        board_str+="\n"
    return board_str