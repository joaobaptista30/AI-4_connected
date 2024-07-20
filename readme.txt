Files content:

<Connect-4.py>
	Graphic version to play. With the menus to start, rules and board
	Can play PvP or PvIA (IA plays using MCTS algorithm limited to 5 seconds)

<Game4InLine.py>
	Game logic and A* implementation

<MCTS.py>
	Monte Carlo Tree Search implementation

<play.py>
	Terminal interface to play: (5 options)
		1: Human vs Human | or | Human vs IA (you can choose which AI to face, among A* e MCTS)
		2: A* vs A*
		3: MCTS vs MCTS
		4: A* vs MCTS
		5: MCTS vs A*