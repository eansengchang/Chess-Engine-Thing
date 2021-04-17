import random
import time

import numpy

pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 1
ENDGAME = False

pieceTable = {
    "p": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [80, 80, 80, 80, 80, 80, 80, 80],
        [40, 40, 40, 40, 40, 40, 40, 40],
        [10, 10, 10, 30, 30, 10, 10, 10],
        [5, 10, 15, 20, 20, 10, 10, 5],
        [5, 0, 5, 5, 5, -5, 0, 5],
        [5, 5, 0, -5, -5, 5, 5, 5],
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
        [-10, 10, 10, 0, 5, 10, 10, -10],
        [-10, 5, 0, 0, 5, 0, 5, -10],
        [-20, -10, -15, -10, -10, -15, -10, -20],
    ],
    "R": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
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
        [20, 30, 10, 0, 0, 10, 30, 20]
    ]
}


def endGame():
    global DEPTH, ENDGAME
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
    ENDGAME = True
    DEPTH = 4


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

    if pieces < 10 and not ENDGAME:
        endGame()

    if len(validMoves) == 1:
        return validMoves[0]
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    score = findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1,
                                     time.time())
    if score == CHECKMATE:
        DEPTH -= 2
    print(counter)
    return nextMove


def sortMovesGS(gs, move):
    num = 0
    if move.pieceCaptured != "--":
        num += 1
        num += pieceScore[move.pieceCaptured[1]] - pieceScore[move.pieceMoved[1]]
    return -num


def searchAllCaptures(gs, alpha, beta, turnMultiplier):
    global counter
    counter += 1
    evaluation = turnMultiplier * scoreBoard(gs)
    if evaluation >= beta:
        return beta

    alpha = max(alpha, evaluation)
    allMoves = gs.getValidMoves()

    def sortMoves(move):
        return sortMovesGS(gs, move)

    def checkCaptures(move):
        gs.makeMove(move)
        flag = move.pieceCaptured != "--" or gs.inCheck()
        gs.undoMove()
        return flag

    captureMoves = list(filter(checkCaptures, allMoves))
    captureMoves.sort(key=sortMoves)
    for move in captureMoves:
        gs.makeMove(move)
        evaluation = -searchAllCaptures(gs, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)

    return alpha


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, start):
    global nextMove, counter
    counter += 1

    if len(validMoves) == 0 and gs.inCheck():
        return -CHECKMATE

    if len(validMoves) == 0:
        return scoreBoard(gs) * turnMultiplier
    elif depth == 0:
        return searchAllCaptures(gs, alpha, beta, turnMultiplier)

    def sortMoves(move):
        return sortMovesGS(gs, move)

    validMoves.sort(key=sortMoves)
    maxScore = -CHECKMATE
    for move in validMoves:
        # print("DEPTH {}: {}".format(depth, move.getChessNotation()))
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier, start)
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
    evaluation += 2 * (opponentKingDistToCenterRank + opponentKingDistToCenterFile)

    friendKingRank = friendlyKingPosition[0]
    friendlyKingFile = friendlyKingPosition[1]

    dstBetweenKingsRank = abs(friendKingRank - opponentKingRank)
    dstBetweenKingsFile = abs(friendlyKingFile - opponentKingFile)
    dstBetweenKings = abs(dstBetweenKingsRank + dstBetweenKingsFile)
    evaluation += (14 - dstBetweenKings)

    # print(evaluation * 10)
    return evaluation * 10


'''
positive score is good for white, negative is good for black
'''


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE

    if gs.stalemate:
        return 0

    score = 0
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            square = gs.board[r][c]
            if square[0] == "w":
                score += pieceScore[square[1]] + pieceTable[square[1]][r][c]
            elif square[0] == "b":
                score -= pieceScore[square[1]] + pieceTable[square[1]][7 - r][c]

    if ENDGAME:
        if score > 0:
            score += forceKingCorner(gs.whiteKingLocation, gs.blackKingLocation)
        else:
            score -= forceKingCorner(gs.blackKingLocation, gs.whiteKingLocation)

    score += 30 if gs.currentCastlingRight.wks else 0
    score += 30 if gs.currentCastlingRight.wqs else 0
    score -= 30 if gs.currentCastlingRight.bks else 0
    score -= 30 if gs.currentCastlingRight.bqs else 0

    # print("Score: {}".format(score))
    return score

# endGame()
