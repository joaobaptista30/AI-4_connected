from Game4InLine import Game4InLine as G4Line

BOARD_SIZE_STANDARD=True #make it 'False' if u want to play 4InLine with a board diff from 6x7

def start_board(rows, cols): #start the board with '-' for all entrances
    return [['-' for _ in range(cols)] for _ in range(rows)]

def start_placed(cols): #start a list to record the num of piece per column
    return [0 for _ in range(cols)]

def result(game,col):
    res=game.isFinished(col)
    if res:
        if res==2:
            print(f"Draw")
        else:
            print(f"{game.pieces[game.turn-1]} won")
        return True
    return False



def main(): #func for the game
    #in case user decides to play with a different board size from 6x7
    if BOARD_SIZE_STANDARD: game=G4Line(board=start_board(6,7),placed=start_placed(7))
    else: 
        r,c=map(int,input("Min board size: 5x5\nBoard size: (rows,cols) ").split())
        if(r<=4 or c<=4): game=G4Line(board=start_board(6,7),placed=start_placed(7))
        else: game=G4Line(board=start_board(r,c),placed=start_placed(c)) 
    print(game)
    
    #if user want to play vs AI (and which AI, when MCTS is implemented)
    Ai_playing = input("Play with AI [y\\n]: ")
    while Ai_playing!='y' and Ai_playing!='n':
        Ai_playing = input(f"Invalid choice\nPlay with AI [y\\n]: ")


    #main loop
    while True:        
        print(f"player {game.turn%2 +1} ('{game.pieces[game.turn%2]}') turn")

        column_played = int(input("Column to place: ")) - 1
        while (column_played > game.cols-1 or column_played < 0) or game.placed[column_played] >= game.rows :
            print("Impossible move")
            column_played = int(input("Column to place: ")) - 1

        game.play(column_played)
        print(f"player {game.turn%2 +1}:")
        print(game)
        
        
        if result(game,column_played):
            break

        ''' temporary code to visualize heuristic and A* playing
        print(game.heuristic_points(column_played))
        print("Childs")
        tmp=game.childs()
        for i in range(len(tmp)):
            print(f"{tmp[i][0]}\n{tmp[i][0].heuristic_points(tmp[i][1])}")
        '''

        #AI play
        if Ai_playing == "y":
            column_played=game.A_star(lambda state,col: G4Line.heuristic_points(state,col)+ G4Line.heuristic_path(state,col))

            game.play(column_played)
            print("IA play:")
            print(game)


        if result(game,column_played):
            break

        

if __name__ == "__main__":
    main()
