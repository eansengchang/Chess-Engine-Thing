import math
import random
import time

import numpy

pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 1
ENDGAME = False
MIDDLEGAME = False

pieceTable = {
    "p": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [0, 0, -10, 0, 0, -10, 0, 0],
        [-1, 0, 0, -20, -20, 0, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "N": [
        [-50, -15, -30, -30, -30, -30, -15, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 25, 25, 15, 5, -30],
        [-30, 0, 15, 25, 25, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -10, -30, -30, -30, -30, -10, -50]
    ],
    "B": [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 15, 15, 5, 5, -10],
        [-10, 0, 10, 15, 10, 10, 0, -10],
        [-10, 10, 10, 5, 5, 10, 10, -10],
        [-10, 5, 0, 0, 5, 5, 5, -10],
        [-20, -10, -15, -10, -10, -15, -10, -20],
    ],
    "R": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, 0, 5, 5, 5, 4, 0, -1]
    ],
    "Q": [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [5, 0, 5, 5, 5, 5, 0, 5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ],
    "K": [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, -1, -1, 10, 30, 20]
    ]
}


def endGame():
    global DEPTH, ENDGAME, MIDDLEGAME
    pieceTable["K"] = [
        # [-50, -40, -30, -20, -20, -30, -40, -50],
        # [-40, -20, -10, 0, 0, -10, -20, -40],
        # [-30, -10, 20, 30, 30, 20, -10, -30],
        # [-30, -10, 30, 30, 30, 30, -10, -30],
        # [-30, -10, 30, 30, 30, 30, -10, -30],
        # [-30, -10, 20, 30, 30, 20, -10, -30],
        # [-40, -30, 0, 0, 0, 0, -30, -40],
        # [-50, -40, -30, -30, -30, -30, -40, -50]
        [0, 0, 0, -1, -1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, -1, 0, 0, 0],
    ]
    pieceTable["R"] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    pieceTable["Q"] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    ENDGAME = True
    MIDDLEGAME = False
    DEPTH = 2


# This is more like the endgame but not completely endgame, king needs to be more active
def middleGame():
    global DEPTH, MIDDLEGAME
    # pieceTable = {}
    pieceTable["K"] = [
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-40, -20, -10, 0, 0, -10, -20, -40],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 30, 30, 30, -10, -30],
        [-30, -10, 30, 30, 30, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-40, -30, 0, 0, 0, 0, -30, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]
    pieceTable["p"] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [150, 150, 150, 150, 150, 150, 150, 150],
        [30, 50, 50, 50, 50, 50, 50, 30],
        [20, 40, 40, 40, 40, 40, 40, 20],
        [10, 20, 20, 20, 20, 20, 20, 10],
        [10, 10, 10, 10, 10, 10, 10, 10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    pieceTable["R"] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    MIDDLEGAME = True
    DEPTH = 2


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


'''
First recursive call
'''


def findBestMove(gs, validMoves):
    global nextMove, counter, DEPTH
    nextMove = None
    counter = 0
    random.shuffle(validMoves)

    pieces = 0
    for row in gs.board:
        for col in row:
            if col != "--":
                pieces += 1

    if pieces < 20 and not MIDDLEGAME and not ENDGAME:
        middleGame()
    if pieces < 10 and not ENDGAME:
        endGame()

    if len(validMoves) == 1:
        return validMoves[0]
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    score = findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    if score == CHECKMATE:
        DEPTH -= 2
    # print(counter)
    if not any(("wQ" in x or "bQ" in x) for x in gs.board):
        DEPTH = 2

    return nextMove


def sortMovesGS(gs, move):
    # num is higher if its a worth capture or in check

    num = 0
    # gs.makeMove(move)
    if move.pieceCaptured != "--":
        num += 1
        num += pieceScore[move.pieceCaptured[1]] / 100 - pieceScore[move.pieceMoved[1]] / 100
    # this involves generating all possible moves, not sure if its worth
    # if gs.inCheck():
    #     num += 2
    # gs.undoMove()

    return -num  # returns negative because thats just how the stupid sort function works


def searchAllCaptures(gs, alpha, beta, turnMultiplier):
    global counter
    counter += 1
    allMoves = gs.getValidMoves()
    evaluation = turnMultiplier * scoreBoard(gs)
    if evaluation >= beta:
        return beta

    alpha = max(alpha, evaluation)

    def sortMoves(move):
        return sortMovesGS(gs, move)

    def checkCaptures(move):
        # gs.makeMove(move)
        # todo when 3 fold repetition is added, fix this
        flag = move.pieceCaptured != "--"  # or move.isPawnPromotion  # or (not ENDGAME and not MIDDLEGAME and gs.inCheck())
        # gs.undoMove()
        return flag

    captureMoves = allMoves
    if len(allMoves) != 1:
        captureMoves = list(filter(checkCaptures, allMoves))

    # sorts the move based on percieved value for alpha beta pruning
    captureMoves.sort(key=sortMoves)
    # print(len(captureMoves))
    for move in captureMoves:
        gs.makeMove(move)
        evaluation = -searchAllCaptures(gs, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)

    return alpha


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1

    if len(validMoves) == 0 and gs.inCheck():
        return -CHECKMATE

    if len(validMoves) == 0:
        return scoreBoard(gs) * turnMultiplier
    # after the depth is reached, go through all the possible captures
    elif depth == 0:
        return searchAllCaptures(gs, alpha, beta, turnMultiplier)

    def sortMoves(move):
        return sortMovesGS(gs, move)

    # sorts the move based on percieved value for alpha beta pruning
    validMoves.sort(key=sortMoves)
    maxScore = -CHECKMATE
    # loops through all the possible moves and goes one depth deeper
    for move in validMoves:
        # print("DEPTH {}: {}".format(depth, move.getChessNotation()))
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

                print("Evaluated {}: {}".format(move.getChessNotation(), turnMultiplier * maxScore / 100))

        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if beta <= alpha:
            break
    return maxScore


def forceKingCorner(friendlyKingPosition, opponentKingSquare):
    evaluation = 0
    opponentKingRank = opponentKingSquare[0]
    opponentKingFile = opponentKingSquare[1]

    opponentKingDistToCenterFile = max(3 - opponentKingFile, opponentKingFile - 4)
    opponentKingDistToCenterRank = max(3 - opponentKingRank, opponentKingRank - 4)
    # if the king is closer to the corner, its better
    evaluation += math.sqrt(
        2.2 * opponentKingDistToCenterRank + 2 * opponentKingDistToCenterFile)  # touch this if u wanna die

    friendlyKingRank = friendlyKingPosition[0]
    friendlyKingFile = friendlyKingPosition[1]

    # if MIDDLEGAME:
    #     friendlyKingDistToCenterFile = max(3 - friendlyKingFile, friendlyKingFile - 4)
    #     friendlyKingDistToCenterRank = max(3 - friendlyKingRank, friendlyKingRank - 4)
    #     evaluation -= (friendlyKingDistToCenterFile + friendlyKingDistToCenterRank) / 3

    dstBetweenKingsRank = abs(friendlyKingRank - opponentKingRank)
    dstBetweenKingsFile = abs(friendlyKingFile - opponentKingFile)
    dstBetweenKings = abs(dstBetweenKingsRank + dstBetweenKingsFile)
    # if the king is closer to the opponents king, its easier to mate
    evaluation += math.sqrt((14 - dstBetweenKings))

    # print(evaluation * 10)
    return evaluation * 10


'''
positive score is good for white, negative is good for black
'''


def scoreBoard(gs):
    # checks for checkmates and draws
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE

    if gs.stalemate:
        return 0

    score = 0
    # calculates the score of the board based on piece position and value
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            square = gs.board[r][c]
            if square[0] == "w":
                score += pieceScore[square[1]] + pieceTable[square[1]][r][c]
            elif square[0] == "b":
                score -= pieceScore[square[1]] + pieceTable[square[1]][7 - r][c]

    # this only works in the endgame is only done by the winning side
    if ENDGAME:
        if score > 0:
            score += forceKingCorner(gs.whiteKingLocation, gs.blackKingLocation)
        else:
            score -= forceKingCorner(gs.blackKingLocation, gs.whiteKingLocation)

    # score += 30 if gs.currentCastlingRight.wks and gs.currentCastlingRight.wqs else 0
    # score -= 30 if gs.currentCastlingRight.bks and gs.currentCastlingRight.bqs else 0

    # print("Score: {}".format(score))
    return score

# endGame()
