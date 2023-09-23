import os
import time
from colorama import Back, Fore, init

#Font Color 
init(autoreset=True)

#Game Conditions
victory = False
wTurn = True
checkmate = False
ans = True

#Board Pieces
wFore = Fore.BLUE
bFore = Fore.BLACK
mBack = Back.RED
bBack = Back.YELLOW
wBack = Back.WHITE
wRook = wFore + "RK"
bRook = bFore + "RK"
wPawn = wFore + "PN"
bPawn = bFore +  "PN"
wBishop = wFore + "BP"
bBishop = bFore + "BP"
wKnight = wFore + "KT"
bKnight = bFore + "KT"
wKing = wFore + "KG"
bKing = bFore + "KG"
wQueen = wFore + "QN"
bQueen = bFore + "QN"

#Messages to Inform Player
wTurn_Mssg = "IT IS WHITE'S TURN"
bTurn_Mssg = "IT IS BLACK'S TURN"
white_Mssg = "White"
black_Mssg = "Black"
bKingCh_Mssg = "THE BLACK'S KING HAS BEEN CHECKED!!"
wKingCh_Mssg = "THE WHITE'S KING HAS BEEN CHECKED!!"
wVictory_Mssg = "CONGRATULATIONS WHITE, YOU WON!!"
bVictory_Mssg = "CONGRATULATIONS BLACK, YOU WON!!"
pieces_Mssg = f"{wRook} = Rook\t{wPawn} = Pawn\t{wKnight} = Knight\n{wBishop} = Bishop\t{wQueen} = Queen\t{wKing} = King\n"
Alert_Mssg = wTurn_Mssg

#For Board Setup
wPieces = [wRook, wKnight, wBishop, wQueen, wKing, wBishop, wKnight, wRook]
bPieces = [bRook, bKnight, bBishop, bKing, bQueen, bBishop, bKnight, bRook]
abc = ['+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', '+']
row = []
board = []

#Memory of King's Illegal Moves
wKing_threat = [0, 0, 0]
bKing_threat = [0, 0, 0]
threatPath = []
bKing_redMoves = {
    "Position" : [4, 1]
}
wKing_redMoves = {
    "Position" : [5, 8]
}

#To Color Board
pieceX = -1
pieceY = -1
moveX = -1
moveY = -1
kingY = -1
kingX = -1

waitTime = 0

def Empty(x, y): #made to easily allow players to call location 
    emp = "{}{}".format(abc[x], y)
    return emp


def setup():
    for i in range(0, 10, 1):
        if i == 2 or i == 7:
            if (i == 2):
                row = [bPawn for j in range(8)]
            else:
                row = [wPawn for j in range(8)]
        elif i == 1 or i == 8:
            if (i == 1):
                row = bPieces.copy()
            else:
                row = wPieces.copy()
        elif i == 9 or i == 0:
            board.append(abc)
            continue
        else:
            row = [Empty(j+1, i) for j in range(8)]
        #print(row)
        row.append(f"{i}")
        row.insert(0, f"{i}")
        board.append(row)


def display():
    os.system('clear')
    print(pieces_Mssg)

    for i in range(10):
        for j in range(10):
            piecePos = j == pieceX and i == pieceY
            movePos = j == moveX and i == moveY
            kingPos = j == kingX and i == kingY

            if j == 9 and i != 9:
                print(" "*(i != 0),board[i][j],"\n",'-'*45,sep='')
            elif j == 9 and i == 9:
                print(board[i][j])
            else:
                if i != 0 and i != 9:
                    if i % 2 == 0 and j != 0 and j % 2 == 0:
                        print(wBack + (piecePos or movePos or kingPos)*mBack + f" {board[i][j]} ","|",sep='',end='')
                    elif i % 2 != 0 and j != 0 and j % 2 != 0:
                        print(wBack + (piecePos or movePos or kingPos)*mBack + f" {board[i][j]} ","|",sep='',end='')
                    else:
                        print((j != 0 and j != 9)*bBack + ((piecePos or movePos or kingPos))*mBack + f"{' '*(j != 0)}{board[i][j]} ","|",sep='',end='')
                else:
                    print(f"{'-'*(j != 0 or ((i != 0 and i != 9) and j != 9))}{board[i][j]}","|",end=' '*(j!=9))

    time.sleep(waitTime)
    print("{}{}".format(' '*round((45-len(Alert_Mssg))/2),Alert_Mssg))
    print("\n", end="")


def saveKing(move):
    global wKing_redMoves, bKing_redMoves, victory, Alert_Mssg, checkmate, wTurn, threatPath, kingY, kingX, moveY, moveX, pieceX, pieceY

    if not checkmate:
        return

    if wTurn:
        king = wKing
        redMoves = wKing_redMoves.values()
    else:
        king = bKing
        redMoves = bKing_redMoves.values()

    while True:

        display()

        heroPiece = checkPiece()

        heroMove = checkMove(heroPiece)

        print(not heroMove[0] in threatPath) and  Empty(heroMove[1], heroMove[2]) != Empty(move[1], move[2]) or (heroPiece[0] == king and (Empty(heroMove[-2], heroMove[-1]) in redMoves or move[0] != heroMove[0]))
        print(bKing_redMoves, wKing_redMoves)

        if ((not heroMove[0] in threatPath) and Empty(heroMove[1], heroMove[2]) != Empty(move[1], move[2])) or (heroPiece[0] == king and (Empty(heroMove[-2], heroMove[-1]) in redMoves or move[0] != heroMove[0])):
            print("Your king is still in check with that move!!")
            ask = str(input("Do you wish to forfeit? (Y/n): ")).upper()
            while ask != "N" and ask != "Y":
                str(input("Do you wish to forfeit? (Y/n): ")).upper()

            if ask == 'Y':
                victory = True
                break

            moveX = -1
            moveY = -1
            pieceY = -1
            pieceX = -1

            continue
        else:
            kingX = -1
            kingY = -1
            moveX = -1
            moveY = -1
            pieceY = -1
            pieceX = -1

            board[heroMove[-1]][heroMove[-2]] = heroPiece[0]
            board[heroPiece[2]][heroPiece[1]] = Empty(heroPiece[1], heroPiece[2])

            if wTurn:
                wTurn = False
            else:
                wTurn = True

            break
    
    checkmate = False


def checkKing(move):
    global Alert_Mssg, kingX, kingY, checkmate, wKing_redMoves, bKing_redMoves, bKingCh_Mssg, wKingCh_Mssg, threatPath, wTurn
    checkmate = False
    redMoves = []

    if not wTurn and len(wKing_redMoves) != 1:
        wKing_redMovesKeys = list(wKing_redMoves.keys())
        del wKing_redMovesKeys[0]

        for i in range (0, len(wKing_redMovesKeys), 1):
            txt = wKing_redMovesKeys[i]
            threat = txt[:txt.find(',')]
            x = int(txt[-2])
            y = int(txt[-1])

            print(wKing_redMovesKeys, x, y)
            
            if board[y][x] != threat:
               del wKing_redMoves[txt]


    elif wTurn and len(bKing_redMoves) != 1:
        bKing_redMovesKeys = list(wKing_redMoves.keys())
        del bKing_redMovesKeys[0]
        
        for i in range (0, len(bKing_redMovesKeys), 1):
            txt = bKing_redMovesKeys[i]
            threat = txt[:txt.find(',')-1]
            print(threat)
            x = int(txt[-2])
            y = int(txt[-1])
            
            if board[y][x] != threat:
                del bKing_redMoves[txt]

    if wTurn:
        king = bKing
        kgX = bKing_redMoves["Position"][0]
        kgY = bKing_redMoves["Position"][1]
        wTurn = False
    else: 
        king = wKing
        kgX = wKing_redMoves["Position"][0]
        kgY = wKing_redMoves["Position"][1]
        wTurn = True

    King_moves = listMoves([king, kgX, kgY])

    if wTurn:
        wTurn = False
    else:
        wTurn = True

    if Empty(kgX, kgY) in bKing_redMoves:
        Alert_Mssg = bKingCh_Mssg
        checkmate = True
        return

    elif Empty(kgX, kgY) in wKing_redMoves:
        Alert_Mssg = wKingCh_Mssg
        checkmate = True
        return

    threat = f"{Empty(move[-2], move[-1])}, {move[-2]}{move[-1]}"
    threatPos = [board[move[-1]][move[-2]], move[-2], move[-1]]
    threatMoves = listMoves(threatPos)
    
    for i in range(0, len(threatMoves), 1):
        if threatMoves[i] == Empty(kgX, kgY):
            kingX = kgX
            kingY = kgY
            checkmate = True

            if threatPos != wKnight and threatPos != bKnight and redMoves != 0:
                print(redMoves)
                threatPath.clear()
                threatPath.append(redMoves[0])
                redMovesStr = str(redMoves[0])
                j = 0
                
                redX = abc.index(redMovesStr[0])
                redY = int(redMovesStr[1])
                pathX = redX - kgX 
                pathY = redY - kgY

                

                while threatPath[j] != Empty(threatPos[1], threatPos[2]):

                    print(pathX, pathY, threatPath, Empty(threatPos[1], threatPos[2]), Empty((redX + pathX), (redY + pathY)))
                    #print(redX, redY, Empty((redX - pathX), (redY - pathY)))
                    #print("Hello")
                    
                    threatPath.append(Empty((redX + pathX), (redY + pathY)))

                    if pathX < 0:
                        pathX -= 1
                    elif pathX > 0:
                        pathX += 1
                    
                    if pathY < 0:
                        pathY -= 1
                    elif pathY > 0:
                        pathY += 1

                    j += 1

            if king == bKing:
                Alert_Mssg = bKingCh_Mssg
                break

            elif king == wKing: 
                Alert_Mssg = wKingCh_Mssg
                break
        
        if King_moves == None:
            continue
       
        if threatMoves[i] in King_moves:        
            King_moves.remove(threatMoves[i])
            redMoves.append(threatMoves[i])
        
        if (i == len(threatMoves)-1):
            continue

        if wTurn:
            wKing_redMoves[threat] = redMoves
        else:
            bKing_redMoves[threat] = redMoves        


def listMoves(piece):
    moveList = []
    pieceY = int(piece[2])
    pieceX = int(piece[1])

    if wTurn:
        oppositePieces = bPieces
        oppositePawn = bPawn
        redMoves = list(wKing_redMoves.values())
    else:
        oppositePawn = wPawn
        oppositePieces = wPieces
        redMoves = list(bKing_redMoves.values())

    while True:
        if piece[0] == bPawn:
            if board[pieceY+1][pieceX-1] in oppositePieces or board[pieceY+1][pieceX-1] == oppositePawn:
                moveList.append(Empty(pieceX-1, (pieceY+1)))

            if board[pieceY+1][pieceX+1] in oppositePieces or board[pieceY+1][pieceX+1] == oppositePawn:
                moveList.append(Empty(pieceX+1, (pieceY+1)))

            if board[pieceY+1][pieceX] == Empty(pieceX, pieceY+1): 
                moveList.append(Empty(pieceX, (pieceY+1)))

            if pieceY == 2 and board[pieceY+2][pieceX] == Empty(pieceX, pieceY+2):
                moveList.append(Empty(pieceX, (pieceY+2)))

        if piece[0] == wPawn:
            if board[pieceY-1][pieceX-1] in oppositePieces or board[pieceY-1][pieceX-1] == oppositePawn:
                moveList.append(Empty(pieceX-1, (pieceY-1)))

            if board[pieceY-1][pieceX+1] in oppositePieces or board[pieceY-1][pieceX+1] == oppositePawn:
                moveList.append(Empty(pieceX+1, (pieceY-1)))

            if board[pieceY-1][pieceX] == Empty(pieceX, (pieceY-1)): 
                moveList.append(Empty(pieceX, (pieceY-1)))

            if pieceY == 7 and board[pieceY-2][pieceX] == Empty(pieceX, (pieceY-2)):
                moveList.append(Empty(pieceX, (pieceY-2)))

            break

        if piece[0] == wKnight or piece[0] == bKnight:
            if pieceY-2 > 0:
                if board[pieceY-2][pieceX-1] == Empty(pieceX-1, (pieceY-2)) or board[pieceY-2][pieceX-1] in oppositePieces or board[pieceY-2][pieceX-1] == oppositePawn:
                    moveList.append(Empty(pieceX-1, pieceY-2))

                if board[pieceY-2][pieceX+1] == Empty(pieceX+1, pieceY-2) or board[pieceY-2][pieceX+1] in oppositePieces or board[pieceY-2][pieceX+1] == oppositePawn:
                    moveList.append(Empty(pieceX+1, pieceY-2))

            if pieceY+2 < 9:
                if board[pieceY+2][pieceX-1] == Empty(pieceX-1, (pieceY+2)) or board[pieceY+2][pieceX-1] in oppositePieces or board[pieceY+2][pieceX-1] == oppositePawn:
                    moveList.append(Empty(pieceX-1, pieceY+2))

                if board[pieceY+2][pieceX+1] == Empty(pieceX+1, pieceY+2) or board[pieceY+2][pieceX+1] in oppositePieces or board[pieceY+2][pieceX+1] == oppositePawn:
                    moveList.append(Empty(pieceX+1, pieceY+2))

            if pieceX-2 > 0:
                if board[pieceY+1][pieceX-2] == Empty(pieceX-2, (pieceY+1)) or board[pieceY+1][pieceX-2] in oppositePieces or board[pieceY+1][pieceX-2] == oppositePawn:
                    moveList.append(Empty(pieceX-2, pieceY+1))

                if board[pieceY-1][pieceX-2] == Empty(pieceX-2, (pieceY-1)) or board[pieceY-1][pieceX-2] in oppositePieces or board[pieceY-1][pieceX-2] == oppositePawn:
                    moveList.append(Empty(pieceX-2, (pieceY-1)))

            if pieceX+2 < 9:
                if board[pieceY+1][pieceX+2] == Empty(pieceX+2, (pieceY+1)) or board[pieceY+1][pieceX+2] in oppositePieces or board[pieceY+1][pieceX+2] == oppositePawn:
                    moveList.append(Empty(pieceX+2, pieceY+1))

                if board[pieceY-1][pieceX+2] == Empty(pieceX+2, (pieceY-1)) or board[pieceY-1][pieceX+2] in oppositePieces or board[pieceY-1][pieceX+2] == oppositePawn:
                    moveList.append(Empty(pieceX+2, (pieceY-1)))

            break
        
        if piece[0] == wKing or piece[0] == bKing: #Somethings Wrong
            if (board[pieceY+1][pieceX] in oppositePieces or board[pieceY+1][pieceX] == oppositePawn or board[pieceY+1][pieceX] == Empty(pieceX, pieceY+1)) and board[pieceY+1][pieceX] not in redMoves:
                moveList.append(Empty(pieceX, pieceY+1))

            if (board[pieceY+1][pieceX-1] in oppositePieces or board[pieceY+1][pieceX-1] == oppositePawn or board[pieceY+1][pieceX-1] == Empty(pieceX-1, pieceY+1)) and board[pieceY+1][pieceX-1] not in redMoves:
                moveList.append(Empty(pieceX-1, pieceY+1))

            if (board[pieceY+1][pieceX+1] in oppositePieces or board[pieceY+1][pieceX+1] == oppositePawn or board[pieceY+1][pieceX+1] == Empty(pieceX+1, pieceY+1)) and board[pieceY+1][pieceX+1] not in redMoves:
                moveList.append(Empty(pieceX+1, pieceY+1))

            if (board[pieceY-1][pieceX] in oppositePieces or board[pieceY-1][pieceX] == oppositePawn or board[pieceY-1][pieceX] == Empty(pieceX, pieceY-1)) and board[pieceY-1][pieceX] not in redMoves:
                moveList.append(Empty(pieceX, pieceY-1))

            if (board[pieceY-1][pieceX+1] in oppositePieces or board[pieceY-1][pieceX+1] == oppositePawn or board[pieceY-1][pieceX+1] == Empty(pieceX+1, pieceY-1)) and board[pieceY-1][pieceX+1] not in redMoves:
                moveList.append(Empty(pieceX+1, pieceY-1))

            if (board[pieceY-1][pieceX-1] in oppositePieces or board[pieceY-1][pieceX-1] == oppositePawn or board[pieceY-1][pieceX-1] == Empty(pieceX-1, pieceY-1)) and board[pieceY-1][pieceX-1] not in redMoves:
                moveList.append(Empty(pieceX-1, pieceY-1))

            if (board[pieceY][pieceX+1] in oppositePieces or board[pieceY][pieceX+1] == oppositePawn or board[pieceY][pieceX+1] == Empty(pieceX+1, pieceY)) and board[pieceY][pieceX+1] not in redMoves:
                moveList.append(Empty(pieceX+1, pieceY))

            if (board[pieceY][pieceX-1] in oppositePieces or board[pieceY][pieceX-1] == oppositePawn or board[pieceY][pieceX-1] == Empty(pieceX-1, pieceY)) and board[pieceY][pieceX-1] not in redMoves:
                moveList.append(Empty(pieceX-1, pieceY))

            break

        sDown = False #s for Stop so sDown means Stop down
        sUp = False
        sLeft = False
        sRight = False
        sUpLeft = False
        sDLeft = False
        sUpRight = False
        sDRight = False

        for i in range(1, 8, 1):
            up = pieceY-i
            down = pieceY+i
            left = pieceX-i
            right = pieceX+i
            

            if piece[0] == wRook or piece[0] == bRook or piece[0] == bQueen or piece[0] == wQueen:
                if down < 9 and not sDown: #Somethings Wrong
                    if board[down][pieceX] == Empty(pieceX, down):
                        moveList.append(Empty(pieceX, down))
                    elif board[down][pieceX] in oppositePieces or board[down][pieceX] == oppositePawn:
                        moveList.append(Empty(pieceX, down))
                        sDown = True
                    else:
                        sDown = True

                if up > 0 and not sUp:
                    if board[up][pieceX] == Empty(pieceX, up):
                        moveList.append(Empty(pieceX, up))
                    elif board[up][pieceX] in oppositePieces or board[up][pieceX] == oppositePawn:
                        moveList.append(Empty(pieceX, up))
                        sUp = True
                    else:
                        sUp = True

                if left > 0 and not sLeft:
                    if board[pieceY][left] == Empty(left, pieceY):
                        moveList.append(Empty(left, pieceY))
                    elif board[pieceY][left] in oppositePieces or board[pieceY][left] == oppositePawn:
                        moveList.append(Empty(left, pieceY))
                        sLeft = True
                    else:
                        sLeft = True

                if right < 9 and not sRight:
                    if board[pieceY][right] == Empty(right, pieceY):
                        moveList.append(Empty(right, pieceY))
                    elif board[pieceY][right] in oppositePieces or board[pieceY][right] == oppositePawn:
                        moveList.append(Empty(right, pieceY))
                        sRight = True
                    else:
                        sRight = True

            if piece[0] == wBishop or piece[0] == bBishop or piece[0] == bQueen or piece[0] == wQueen:
                if down < 9 and left > 0 and not sDLeft:
                    if board[down][left] == Empty(left, down):
                        moveList.append(Empty(left, down))
                    elif board[down][left] in oppositePieces or board[down][left] == oppositePawn:
                        moveList.append(Empty(left, down))
                        sDLeft = True
                    else:
                        sDLeft = True

                if up > 0 and left > 0 and not sUpLeft:
                    if board[up][left] == Empty(left, up):
                        moveList.append(Empty(left, up))
                    elif board[up][left] in oppositePieces or board[up][left] == oppositePawn:
                        moveList.append(Empty(left, up))
                        sUpLeft = True
                    else:
                        sUpLeft = True

                if right < 9 and down < 9 and not sDRight:
                    if board[down][right] == Empty(right, down):
                        moveList.append(Empty(right, down))
                    elif board[down][right] in oppositePieces or board[down][right] == oppositePawn:
                        moveList.append(Empty(right, down))
                        sDRight = True
                    else:
                        sDRight = True

                if right < 9 and up > 0  and not sUpRight:
                    if board[up][right] == Empty(right, up):
                        moveList.append(Empty(right, up))
                    elif board[up][right] in oppositePieces or board[up][right] == oppositePawn:
                        moveList.append(Empty(right, up))
                        sUpRight = True
                    else:
                        sUpRight = True
        break
    return moveList


def checkMove(piece):
    moveMssg = f"Enter your move: "

    display()

    while True:
        inputMove = str(input(moveMssg)).upper()

        if len(inputMove) != 2:
            print("\n\tInvalid input!!")
            continue

        if (not inputMove[0].isalpha()) or (not inputMove[1].isnumeric()): 
            print("\n\tInvalid input!!")
            continue

        if not (inputMove[0] in abc): 
            print("\n\tInvalid Input!!")
            continue
       
        global moveY, moveX, pieceY, pieceX
        mX = abc.index(inputMove[0]) 
        mY = int(inputMove[1])
        move = [board[mY][mX], mX, mY]

        if wTurn is True:
            samePieces = wPieces
            samePawn = wPawn
        else: 
            samePieces = bPieces
            samePawn = bPawn
        
        if move[0] in samePieces or move[0] == samePawn:
            print("\nYou Can't Move To Your Own Pieces")
            continue
        
        moveList = listMoves(piece)

        if not (Empty(mX, mY) in moveList):
            print("\n\tInvalid Move!!")
            continue

        moveY = mY
        moveX = mX

        display()
        print(f"{Empty(pieceX, pieceY)} = {piece[0]}")
        print(f"{piece[0]} moving to {Empty(moveX, moveY)}")

        ans = str(input("Confirm move (Y/n): ")).upper()
        while ('N' != ans and 'Y' != ans):
            ans = str(input("Confirm Again (Y/n): ")).upper()

        if ('Y' == ans) and not checkmate:
            pieceX = -1
            pieceY = -1
            moveX = -1
            moveY = -1
            board[mY][mX] = piece[0]
            board[piece[2]][piece[1]] = Empty(piece[1], piece[2])

            if piece[0] == wKing:
                wKing_redMoves["Position"] = [mX, mY]
            elif piece[0] == bKing:
                bKing_redMoves["Position"] = [mX, mY]

            return move

        elif checkmate:

            return move
        else:
            moveX = -1
            moveY = -1
            display()
            continue


def checkPiece():
    pieceMssg = "Enter your moving piece position: "

    if wTurn is True:
        oppositePieces = bPieces
        oppositePawn = bPawn
    else: 
        oppositePieces = wPieces
        oppositePawn = wPawn

    while True:
        
        inputPiece = str(input(pieceMssg)).upper()

        if len(inputPiece) != 2:
            print("\n\tInvalid input!!")
            continue            
        
        if (not inputPiece[0].isalpha()) or (not inputPiece[1].isnumeric()): 
            print("\n\tInvalid Input!!")
            continue
            
        if not (inputPiece[0] in abc): 
            print("\n\tInvalid Input!!")
            continue

        global pieceY, pieceX
        pX = abc.index(inputPiece[0]) 
        pY = int(inputPiece[1])
        Piece = [board[pY][pX], pX, pY]

        if Piece[0] in oppositePieces or Piece[0] == oppositePawn:
            print("\n\tOpposite Piece!!")
            continue
        elif Piece[0] == Empty(pX, pY):
            print("\n\tEmpty Space!!")
            continue
        elif (len(listMoves(Piece)) == 0):
            print("\n\tPiece didn't have any valid moves")
            continue

        pieceY = pY
        pieceX = pX

        display()
        print(f"Input: {inputPiece} = {Piece[0]}")
        
        ans = str(input("Confirm Piece (Y/n): ")).upper()
        while ('N' != ans and 'Y' != ans):
            ans = str(input("Confirm Again (Y/n): ")).upper()
        if ('N' == ans):
            pieceY = -1
            pieceX = -1
            display()
            continue
        
        return Piece   


def play():
    global wTurn, pieceX, pieceY, moveX, moveY, Alert_Mssg, checkmate
    
    while True:
        
        display()

        Piece = checkPiece()

        Move = checkMove(Piece)

        checkKing(Move)

        if wTurn:
            wTurn = False
        else:
            wTurn = True

        saveKing(Move)

        if victory:
            break

        if not wTurn:
            Alert_Mssg = "IT IS BLACK'S TURN"
        else:
            Alert_Mssg = "IT IS WHITE'S TURN"


while True:
    setup()   
    play()

    if not wTurn:
        print("\n", wVictory_Mssg, sep='')
    else:
        print("\n", bVictory_Mssg, sep='')

    ans = str(input("Another Game?: ")).upper
    while ('N' != ans and 'Y' != ans):
        ans = str(input("Confirm Again (Y/n): ")).upper()

    if ('N' == ans):
        break
