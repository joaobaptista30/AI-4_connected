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
        childs=[]


    def play(self,col:int): #funcion to place pieces based on turn and column
        self.board[self.rows-self.placed[col]-1][col]=self.pieces[self.turn]
        self.placed[col]+=1
        self.round+=1
        self.turn = 1 if self.turn%2==0 else 0 #change turn


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


    def A_star():
        



        ...


    def __str__(self): #override the print() method
        return print_board(self.board)




def print_board(board): #transform the game board from matrix to a visual representation
    board_str="|"
    for k in range(1,len(board[0])+1):
        board_str+=f" {k} |"
    board_str+="\n"
    for i in range(len(board)):
        board_str += "| "
        for j in range(len(board[i])):
            board_str+=board[i][j]
            board_str += " | "
        board_str+="\n"
    return board_str