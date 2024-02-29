from Game4InLine import Game4InLine

BOARD_SIZE_STANDARD=True #make it 'False' if u want to play 4InLine with a board diff from 6x7

def start_board(rows, cols): #start the board with '-' for all entrances
    return [['-' for _ in range(cols)] for _ in range(rows)]

def start_placed(cols): #start a list to record the num of piece per column
    return [0 for _ in range(cols)]




def main(): #loop for the game
    if BOARD_SIZE_STANDARD: game=Game4InLine(board=start_board(6,7),placed=start_placed(7))

    else: 
        r,c=map(int,input("Min board size: 5x5\nBoard size: (rows,cols) ").split())
        if(r<=4 or c<=4): game=Game4InLine(board=start_board(6,7),placed=start_placed(7))
        else: game=Game4InLine(board=start_board(r,c),placed=start_placed(c)) 
    print(game)


    Ai_playing = input("Play with AI [y\\n]: ")


    while True:        
        print(f"player {game.turn%2 +1} ('{game.pieces[game.turn%2]}') turn")

        column_played = int(input("Column to place: ")) - 1
        while (column_played > game.cols-1 or column_played < 0) or game.placed[column_played] >= game.rows :
            print("Impossible move")
            column_played = int(input("Column to place: ")) - 1

        game.play(column_played)
        print(f"player {game.turn%2 +1}:")
        print(game)
        

        ''' temporary code to visualize heuristic and A* playing
        print(game.heuristic_points(column_played))
        print("Childs")
        tmp=game.childs()
        for i in range(len(tmp)):
            print(f"{tmp[i][0]}\n{tmp[i][0].heuristic_points(tmp[i][1])}")
        '''

        #AI play
        if Ai_playing == "y":
            column_played=game.A_star()

            game.play(column_played)
            print("IA play:")
            print(game)


        res=game.isFinished(column_played)
        if res:
            if res==2:
                print(f"Draw")
                break
            else:
                print(f"{game.pieces[game.turn-1]} won")
                break

        

if __name__ == "__main__":
    main()
