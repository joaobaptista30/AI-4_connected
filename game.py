from copy import deepcopy
from time import sleep

BOARD_SIZE_STANDARD=True #make it 'False' if u want to play 4InLine with a board diff from 6x7

#Human start and uses 'X' (player 1)
#AI go second and uses 'O' (player 2)

class Game4InLine:
    def __init__ (self,board,placed):
        self.rows = len(board)
        self.cols = len(board[0])
        self.board = deepcopy(board) #matrix representing the board
        self.placed = deepcopy(placed) #list with the num of pieces per column
        self.pieces = ['X','O']
        self.turn = 0
        self.round=0


    def play(self,col:int): #funcion to place pieces based on turn and column
        
        if self.turn%2==0: #Human  turn
            self.board[self.rows-self.placed[col]-1][col]=self.pieces[self.turn]
            self.placed[col]+=1
            self.turn=1
            self.round+=1
            return self
        
        elif self.turn%2!=0: #AI turn

            if(self.placed[col]>=self.rows): #true when column is full
                return None #este if faz mais sentido para criar as childs

            self.board[self.rows-self.placed[col]-1][col]=self.pieces[self.turn]
            self.placed[col]+=1
            self.turn=0
            self.round+=1
            return self

    def isFinished(self,col): #return 2 if game is a draw, True if last move was a winning on , False to keep playing
        played = self.pieces[self.turn-1]
        row = self.rows-self.placed[col]
    
        #Check Vertical
        if(self.placed[col]>=4):
            if(self.board[row][col]==played and self.board[row+1][col]==played and self.board[row+2][col]==played and self.board[row+3][col]==played):
                return True

        # Check horizontal
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

        # Check diagonal right-left
        consecutive = 1
        tmprow = row
        tmpcol = col
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

        # Check diagonal left-right
        consecutive = 1
        tmprow = row
        tmpcol = col
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
        if(self.round==(self.rows*self.cols)):
            return 2

        return False

        
    
    def __str__(self): #override the print() method
        return print_board(self.board)



def start_board(rows, cols): #start the board with '-' for all entrances
    return [['-' for _ in range(cols)] for _ in range(rows)]

def start_placed(cols): #start a list to record the num of piece per column
    return [0 for _ in range(cols)]

def print_board(board): #transform the game board from matrix to a visual representation
    board_str="|"
    for k in range(len(board[0])):
        board_str+=f" {k} |"
    board_str+="\n"
    for i in range(len(board)):
        board_str += "| "
        for j in range(len(board[i])):
            board_str+=board[i][j]
            board_str += " | "
        board_str+="\n"
    return board_str




def main(): #loop for the game
    if BOARD_SIZE_STANDARD: game=Game4InLine(board=start_board(6,7),placed=start_placed(7))

    else: 
        r,c=map(int,input("Min board size: 5x5\nBoard size: (rows,cols) ").split())
        if(r<=4 or c<=4): game=Game4InLine(board=start_board(6,7),placed=start_placed(7))
        else: game=Game4InLine(board=start_board(r,c),placed=start_placed(c)) 

    print(game)

    while True:
        if(game.turn%2==0): print("player 1 ('X') turn")
        else: print("player 2 ('O') turn")

        column_played = int(input("Column to place: "))
        if (column_played > game.cols-1 or column_played < 0):
            print("Column out of range")
            continue
        elif game.placed[column_played] >= game.rows :
            print("Column is full")
            continue
        else:
            game.play(column_played)
            print(game)
            print(game.placed)
        res=game.isFinished(column_played)
        if res:
            if res==99:
                print(f"Draw")
                break
            else:
                print(f"{game.pieces[game.turn-1]} won")
                break

        
if __name__ == "__main__":
    main()
