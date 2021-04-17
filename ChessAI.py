import random
import time

import numpy

pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 5
ENDGAME = False

pieceTable = {
    "p": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [80, 80, 80, 80, 80, 80, 80, 80],
        [40, 40, 40, 40, 40, 40, 40, 40],
        [10, 10, 10, 30, 30, 10, 10, 10],
        [5, 10, 10, 20, 20, 10, 10, 5],
        [5, -5, -10, -5, -5, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "N": [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 25, 25, 15, 5, -30],
        [-30, 0, 15, 25, 25, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ],
    "B": [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 12, 5, 15, 15, 5, 12, -10],
        [-10, 0, 10, 15, 15, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
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
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 30, 30, 30, -10, -30],
        [-30, -10, 30, 30, 30, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -30, 0, 0, 0, 0, -30, -30],
        [-50, -30, -30, -30, -30, -30, -30, -50]
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
    DEPTH = 3


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def sortMoves(move):
    return move.pieceCaptured != "--"


'''
First recursive call
'''


def findBestMove(gs, validMoves):
    random.shuffle(validMoves)
    global nextMove, counter, DEPTH
    nextMove = None
    counter = 0

    pieces = 0
    for pieceType in gs.board:
        pieces += len(gs.board[pieceType])

    if pieces < 10 and not ENDGAME:
        endGame()

    if len(validMoves) == 1:
        return validMoves[0]
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    score = findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1,
                                     time.time())
    if score == CHECKMATE:
        DEPTH -= 2
    # print(counter)
    return nextMove


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, start):
    global nextMove, counter
    counter += 1

    def onlyCapturesandChecks(move):
        if len(gs.moveLog) == 0:
            return False
        gs.makeMove(move)
        flag = move.pieceCaptured != "--" or gs.inCheck()
        gs.undoMove()
        return flag

    if depth == DEPTH - 2 and gs.moveLog[-1].pieceCaptured != "--" and not ENDGAME:
        if len(list(filter(onlyCapturesandChecks, validMoves))) != 0:
            validMoves = list(filter(onlyCapturesandChecks, validMoves))

    elif len(validMoves) == 0 and gs.inCheck():
        return -CHECKMATE
    elif (depth < DEPTH - 1 and not ENDGAME) or len(validMoves) == 0 or depth == 0:
        return turnMultiplier * scoreBoard(gs)
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
    evaluation += opponentKingDistToCenterRank + opponentKingDistToCenterFile

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
    # for r in range(len(gs.board)):
    #     for c in range(len(gs.board[r])):
    #         square = gs.board[r][c]
    #         if square[0] == "w":
    #             score += pieceScore[square[1]] + pieceTable[square[1]][r][c]
    #         elif square[0] == "b":
    #             score -= pieceScore[square[1]] + pieceTable[square[1]][7 - r][c]

    for pieceType in gs.board:
        if pieceType[0] == "w":
            for piece in gs.board[pieceType]:
                score += pieceScore[pieceType[1]] + pieceTable[pieceType[1]][piece[0]][piece[1]]
        else:
            for piece in gs.board[pieceType]:
                score -= pieceScore[pieceType[1]] + pieceTable[pieceType[1]][7 - piece[0]][piece[1]]

    if ENDGAME:
        if score > 0:
            score += forceKingCorner(gs.whiteKingLocation, gs.blackKingLocation)
        else:
            score -= forceKingCorner(gs.blackKingLocation, gs.whiteKingLocation)

    # print("Score: {}".format(score))
    return score

# endGame()
