import numpy as np
import random
import pygame
import sys
import math


#For the gui 
blue = (0,0,255)
black = (0,0,0)
green = (34, 139, 34)
red = (255,0,0)
rows = 6
columns = 7
#Which Turn
player = 0
AI = 1

empty = 0

#IF the player have places in empty is 1 and if AI it is 2 

player_piece = 1
Ai_Piece = 2

windowsSize = 4

pixSize = 90

width = columns * pixSize
height = (rows+1) * pixSize

size = (width, height)

radius = int(pixSize/2 - 5)

screen = pygame.display.set_mode(size)


turn = random.randint(player, AI)

game_over = False


#create a matrix for connect 4 
def createBoard():
	board = np.zeros((rows,columns))
	return board

def dropPiece(board, row, col, piece):
	board[row][col] = piece

def locationValid(board, col):
	return board[rows-1][col] == 0


def getOpenRow(board, col):
	for row in range(rows):
		if board[row][col] == 0:
			return row


#If player wins
def isWinning(board, piece):
	for c in range(columns-3):
		for r in range(rows):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True
	for c in range(columns):
		for r in range(rows-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	for c in range(columns-3):
		for r in range(rows-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	for c in range(columns-3):
		for r in range(3, rows):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
			

def evalWindow(window, piece):
	score = 0
	opp_piece = player_piece
	if piece == player_piece:
		opp_piece = Ai_Piece

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(empty) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(empty) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(empty) == 1:
		score -= 4
	return score


def scorePos(board, piece):
	
	score = 0
	
	center_column = columns // 2
	center_array = [int(cell) for cell in board[:, center_column]]
	
	
	center_count = center_array.count(piece)
	score += center_count * 3

	for r in range(rows):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(columns-3):
			window = row_array[c:c+windowsSize]
			score += evalWindow(window, piece)

	for c in range(columns):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(rows-3):
			window = col_array[r:r+windowsSize]
			score += evalWindow(window, piece)

	for r in range(rows-3):
		for c in range(columns-3):
			window = [board[r+i][c+i] for i in range(windowsSize)]
			score += evalWindow(window, piece)

	for r in range(rows-3):
		for c in range(columns-3):
			window = [board[r+3-i][c+i] for i in range(windowsSize)]
			score += evalWindow(window, piece)

	return score
#When a player beats another
def gameEnd(board):
	return isWinning(board, player_piece) or isWinning(board, Ai_Piece) or len(getValidPos(board)) == 0









#AI Algorithm

def aiAlgo(board, depth, alpha, beta, isMaximizing):
    if depth == 0 or gameEnd(board):
        if isWinning(board, Ai_Piece):
            return (None, 100000000000000)
        elif isWinning(board, player_piece):
            return (None, -10000000000000)
        else:
            return (None, 0)

    validLocs = getValidPos(board)
    bestColumn = random.choice(validLocs)

    if isMaximizing:
        maxScore = -math.inf
        for column in validLocs:
            row = getOpenRow(board, column)
            boardCopy = board.copy()
            dropPiece(boardCopy, row, column, Ai_Piece)
            score = aiAlgo(boardCopy, depth-1, alpha, beta, False)[1]
            if score > maxScore:
                maxScore = score
                bestColumn = column
            alpha = max(alpha, maxScore)
            if alpha >= beta:
                break
        return bestColumn, maxScore

    else:
        minScore = math.inf
        for column in validLocs:
            row = getOpenRow(board, column)
            boardCopy = board.copy()
            dropPiece(boardCopy, row, column, player_piece)
            score = aiAlgo(boardCopy, depth-1, alpha, beta, True)[1]
            if score < minScore:
                minScore = score
                bestColumn = column
            beta = min(beta, minScore)
            if alpha >= beta:
                break
        return bestColumn, minScore

#Return valid location
def getValidPos(board):
	valid_locations = []
	for col in range(columns):
		if locationValid(board, col):
			valid_locations.append(col)
	return valid_locations

def chooseBestPos(board, piece):

	openPieces = getValidPos(board)
	
	bestScore = -10000

	bestCol = random.choice(openPieces)

	for col in openPieces:

		row = getOpenRow(board, col)
		temp_board = board.copy()
		dropPiece(temp_board, row, col, piece)
		score = scorePos(temp_board, piece)

		if score > bestScore:
			bestScore = score
			bestCol = col

	return bestCol


def drawBoard(board):
	for col in range(columns):
		
		for row in range(rows):
			
			pygame.draw.rect(screen, blue, (col * pixSize, row * pixSize + pixSize, pixSize, pixSize))
			pygame.draw.circle(screen, black, (int(col * pixSize + pixSize / 2), int(row * pixSize + pixSize + pixSize / 2)), radius)
	
	for col in range(columns):
		
		for row in range(rows):	
				
			if board[row][col] == player_piece:
				pygame.draw.circle(screen, green, (int(col * pixSize + pixSize / 2), height - int(row * pixSize + pixSize / 2)), radius)
			elif board[row][col] == Ai_Piece: 
				pygame.draw.circle(screen, red, (int(col * pixSize + pixSize / 2), height - int(row * pixSize + pixSize / 2)), radius)
	
	pygame.display.update()


board = createBoard()
drawBoard(board)


pygame.init()
font = pygame.font.SysFont("Arial", 68)




pygame.display.update()



while not game_over:

	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, black, (0,0, width, pixSize))
			posx = event.pos[0]
			
			if turn == player:
				pygame.draw.circle(screen, green, (posx, int(pixSize/2)), radius)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, black, (0,0, width, pixSize))
			
			if turn == player:
				posx = event.pos[0]
				col = int(math.floor(posx/pixSize))

				if locationValid(board, col):
					row = getOpenRow(board, col)
					dropPiece(board, row, col, player_piece)

					if isWinning(board, player_piece):
						label = font.render("Human wins!", 1, green)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2
					drawBoard(board)



	if turn == AI and not game_over:				


		col, minimax_score = aiAlgo(board, 5, -math.inf, math.inf, True)

		if locationValid(board, col):
			row = getOpenRow(board, col)
			dropPiece(board, row, col, Ai_Piece)

			if isWinning(board, Ai_Piece):
				
				label = font.render("AI wins!", 1, red)
				screen.blit(label, (40,10))
				game_over = True
                    
			drawBoard(board)


			turn += 1
			turn = turn % 2



	if game_over:		
		pygame.time.wait(3000)