"""
Handling the AI moves.
"""
import random
from typing import Counter

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]
                        }

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 0

# put next move to a queue and it will be get in main when machine turn is called
def findBestMove(game_state, valid_moves, return_queue, difficult):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    global DEPTH
    if difficult == 1: 
    #    DEPTH = 2
    #    if game_state.white_to_move :
    #       findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE,CHECKMATE)
    #    else :
    #       findMoveNegaMinAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE,CHECKMATE)
          
    #    return_queue.put(next_move)
        findGreedyMove(game_state, valid_moves)
        return_queue.put(next_move)
        
    elif difficult == 2:
        DEPTH = 3
          
    elif difficult == 3:
        DEPTH = 4
    
    if game_state.white_to_move:
          findMoveMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE,CHECKMATE)
    else:
          findMoveMinAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE,CHECKMATE)
          
    return_queue.put(next_move)
         


# return score and show next move
def findMoveMinAlphaBeta(game_state, valid_moves, depth, alpha, beta):
    global next_move
    # global count_move
    # count_move = count_move + 1
    if depth == 0:
        return scoreBoard(game_state)
    min_score = CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = findMoveMaxAlphaBeta(game_state, next_moves, depth - 1, alpha, beta)
        if score < min_score:
            if depth == DEPTH:
                next_move = move 
            min_score = score
        game_state.undoMove()
        if min_score < beta:
            beta = min_score
        if min_score <= alpha: # prunning
            break
                      
    return min_score

def findMoveMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta):
    global next_move
    # global count_move
    # count_move = count_move + 1
    if depth == 0:
        return scoreBoard(game_state)
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = findMoveMinAlphaBeta(game_state, next_moves, depth - 1, alpha, beta)
        if score > max_score:
            if depth == DEPTH:
                next_move = move
            max_score = score
        game_state.undoMove()

        if max_score > alpha:
            alpha = max_score 
            
        if max_score >= beta:#prunning
            break
            
    return max_score
  
  


# # score for each move : white's score and black's
def scoreBoard(game_state):
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    # duyet ca bang
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score




def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)



# greedy algorithm

def findGreedyMove(game_state, valid_moves):
    global next_move
    turnMultiplier = 1 if game_state.white_to_move else -1
    maxScore = -CHECKMATE
    bestMove = None
    for playerMove in valid_moves:
        game_state.makeMove(playerMove)
        if game_state.checkmate:
            score = CHECKMATE
        elif game_state.stalemate:
            score = STALEMATE
        else:
            score = turnMultiplier * scoreMaterial(game_state.board)
        if score > maxScore:
            maxScore = score
            next_move = playerMove
        game_state.undoMove()
    return maxScore

def scoreMaterial (board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score