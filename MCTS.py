import random
import time
import math
from copy import deepcopy

from Game4InLine import Game4InLine as G4


class Node:

    def __init__(self, game: G4, parent=None):
        self.game=deepcopy(game)
        self.parent=parent
        self.visited=0
        self.wins=0
        self.childs = [] # formato [[node,col]]

    def set_childs(self):
        poss_moves = self.game.legal_moves()
        for col in poss_moves:
            state = deepcopy(self.game)
            self.childs.append([Node(state.play(col), parent=self),col])

    def UCB1(self):
        if self.visited == 0:
            return float('inf')

        return (self.wins/self.visited) + math.sqrt(2) * math.sqrt(2*math.log(self.parent.visited)/self.visited)

    def max_UCB(self):
        max_val = (self.childs[0][0]).UCB1()
        for i in range (1,len(self.childs)):
            max_val = max(max_val, (self.childs[i][0]).UCB1())
        return max_val


class MCTS:

    def __init__(self, root: G4):
        self.root=Node(deepcopy(root))
        self.run_time = 0
        self.simulations = 0
    

    def search(self, time_limit, limit_simulations=22500):
        start_time = time.time()
        simulations = 0
        while time.time() - start_time < time_limit and simulations < limit_simulations:
            node = self.selection()
            result = self.simulate(deepcopy(node.game))
            self.back_propagate(node,result)
            simulations += 1


        self.run_time = time.time() - start_time
        self.simulations = simulations


    def selection(self):
        node = self.root
        col_child = 0 # necessario devido a forma de verificar se chegamos ao estado final

        while len(node.childs) != 0:
            max_ucb = node.max_UCB()
            max_nodes = [n for n in node.childs if n[0].UCB1() == max_ucb]
            best_child = random.choice(max_nodes)
            node = best_child[0]
            col_child = best_child[1]

            if node.visited == 0:
                return node
            
        if self.expand(node,col_child):
            random_child = random.choice(node.childs)
            node = random_child[0]

        return node

    def expand(self, node: Node, col: int):
        if node.game.isFinished(col):
            return False
        
        node.set_childs()
        return True

    def simulate(self, node_state: G4):
        while True:
            col = random.choice(node_state.legal_moves())
            node_state.play(col)
            res = node_state.isFinished(col)
            if res:
                return res if res == 2 else 0 if node_state.turn%2==0 else 1 #retorna na vez de quem jogou em ultimo

    def back_propagate(self, node: Node, result):        
        #result = 2 se empatou, =1 se 'X' ganhou e =0 se 'O' ganhou
        #logo quando result == node.game.turn vai dar reward 1 pois foi o jogador que ganhou a simulacao
        while node != None:
            if result == node.game.turn: #caso seja o turno do jogar que ganhou na simulacao 
                reward = 1
            else: reward = 0
            node.visited += 1
            node.wins += reward
            node = node.parent


    def best_move(self):
        childs = self.root.childs
        print(childs) #====================
        node = childs[0][0]
        best_col = childs[0][1]
        max_win_rate = node.wins/node.visited
        print(f"win: {node.wins}\nvisited: {node.visited}")
        print(f"win/visited: {max_win_rate} col: {best_col+1}")

        for i in range (1,len(childs)):
            node = childs[i][0]
            print(f"win: {node.wins}\nvisited: {node.visited}")
            print(f"win/visited: {node.wins/node.visited} col: {childs[i][1]+1}")
            if max_win_rate < (node.wins/node.visited):
                max_win_rate = (node.wins/node.visited)
            
                best_col = childs[i][1]
        return best_col
    
    def statistic(self):
        return self.simulations, self.run_time