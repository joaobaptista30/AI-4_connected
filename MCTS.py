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

        return (self.wins/self.visited) + math.sqrt(2*math.log(self.parent.visited)/self.visited)

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
                return res if res == 2 else 1 if node_state.turn%2==0 else 0 #retorna na vez de quem jogou em ultimo

    def back_propagate(self, node: Node, result):
        reward = 0 #considerar que perdeu/ou/empatou
        if result == self.root.game.turn: #caso tenha ganho
            reward = 1

        while node != None:
            node.visited += 1
            node.wins += reward
            node = node.parent

    def best_move(self):

        max_ucb = self.root.max_UCB()
        max_nodes = [n for n in (self.root.childs) if n[0].UCB1() == max_ucb]

        for n in self.root.childs: #=========== analisar os UCB1 das childs da root
            print(n[0].UCB1(),n[1]+1)

        print("\nmax ")
        print(max_nodes, max_ucb) #================== analisar se selecionou a melhor child corretamente


        best_child = random.choice(max_nodes)
        return best_child[1]
    
    def statistic(self):
        return self.simulations, self.run_time