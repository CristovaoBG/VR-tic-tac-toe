from enum import Enum
from copy import deepcopy

class State(Enum):
    IDLE = 0
    PLAYING = 1
    LOST = 2
    WON = 3
    VELHA = 4
    DEFENDED = 5
    PLACE_BORDER = 6
    PLACE_MIDDLE = 7
    PLACE_SIDES = 8

class Board:
    
    def __init__(self, playerChar, oponentChar):
        self.playerChar = playerChar
        self.oponentChar = oponentChar
        self.emptyChar = '\''
        self.board = [['\'', '\'', '\''], ['\'', '\'', '\''], ['\'', '\'', '\'']]

    def place(self, char, posX, posY):
        self.board[posX][posY] = char

    def isFree(self,posX,posY):
        return self.board[posY][posX]=="\'"

    def print(self):
        for x in range(3):
            s = ''
            for y in range(3):
                s += self.board[x][y]+'|'
            print(s[:-1])
        print("\n")

    def getColumn(self, id):
        return [k[id] for k in self.board]

    def setColumn(self, id, column):
        for i in range(3):
            self.board[i][id] = column[i]

    def getRow(self, id):
        return self.board[id]

    def setRow(self, id, row):
        self.board[id] = row

    def tryToFinish(self):
        #linhas e colunas
        for i in range(3):
            #columns
            hasSpace = self.emptyChar in self.getColumn(i)
            isWin = self.getColumn(i).count(self.playerChar) == 2
            if hasSpace and isWin:
                self.setColumn(i, [self.playerChar, self.playerChar, self.playerChar])
                return True
            #linhas
            hasSpace = self.emptyChar in self.board[i]
            isWin = self.board[i].count(self.playerChar) == 2
            if hasSpace and isWin:
                self.board[i] = [self.playerChar, self.playerChar, self.playerChar]
                return True
        principal = []
        secondary = []
        #diagonal principal
        for i in range(3):
            principal.append(self.board[i][i])
        hasSpace = self.emptyChar in principal
        isWin = principal.count(self.playerChar) == 2
        if hasSpace and isWin:
            self.board[0][0] = self.board[1][1] = self.board[2][2] = self.playerChar
            return True
        #diagonal secundaria
        for i in range(3):
            secondary.append(self.board[i][2-i])
        hasSpace = self.emptyChar in secondary
        isWin = secondary.count(self.playerChar) == 2
        if hasSpace and isWin:
            self.board[0][2] = self.board[1][1] = self.board[2][0] = self.playerChar
            return True
        return False

    def defend(self):
        #linhas e colunas
        for i in range(3):
            #columns
            hasSpace = self.emptyChar in self.getColumn(i)
            isLose = self.getColumn(i).count(self.oponentChar) == 2
            if hasSpace and isLose:
                #self.setColumn(i,[self.playerChar,self.playerChar,self.playerChar])
                pos = self.getColumn(i).index(self.emptyChar)
                self.board[pos][i] = self.playerChar
                return True
            #linhas
            hasSpace = self.emptyChar in self.board[i]
            isLose = self.board[i].count(self.oponentChar) == 2
            if hasSpace and isLose:
                self.board[i] = [self.playerChar if self.board[i][idx] ==
                                                 self.emptyChar else self.oponentChar for idx in range(3)]
                return True
        principal = []
        secondary = []
        #diagonal principal
        for i in range(3):
            principal.append(self.board[i][i])
        hasSpace = self.emptyChar in principal
        isLose = principal.count(self.oponentChar) == 2
        if hasSpace and isLose:
            self.board[0][0] = self.board[0][0] if self.board[0][0] == self.oponentChar else self.playerChar
            self.board[1][1] = self.board[1][1] if self.board[1][1] == self.oponentChar else self.playerChar
            self.board[2][2] = self.board[2][2] if self.board[2][2] == self.oponentChar else self.playerChar
            return True
        #diagonal secundaria
        for i in range(3):
            secondary.append(self.board[i][2-i])
        hasSpace = self.emptyChar in secondary
        isLose = secondary.count(self.oponentChar) == 2
        if hasSpace and isLose:
            self.board[0][2] = self.board[0][2] if self.board[0][2] == self.oponentChar else self.playerChar
            self.board[1][1] = self.board[1][1] if self.board[1][1] == self.oponentChar else self.playerChar
            self.board[2][0] = self.board[2][0] if self.board[2][0] == self.oponentChar else self.playerChar
            return True
        return False
    
    def tryMiddle(self):
        if self.board[1][1] == self.emptyChar:
            self.board[1][1] = self.playerChar
            return True
        return False

    def tryBorders(self):
        if self.board[0][0] == self.emptyChar:
            self.board[0][0] = self.playerChar
            return True
        if self.board[2][0] == self.emptyChar:
            self.board[2][0] = self.playerChar
            return True
        if self.board[0][2] == self.emptyChar:
            self.board[0][2] = self.playerChar
            return True
        if self.board[2][2] == self.emptyChar:
            self.board[2][2] = self.playerChar
            return True
        return False

    def trySides(self):
        if self.board[1].count(self.emptyChar) == 2:
            for i in range(3):
                if self.board[1][i] == self.emptyChar:
                    self.board[1][i] = self.playerChar
                    return True
            return True
        col = self.getColumn(1)
        if col.count(self.emptyChar) == 2:
            for i in range(3):
                if self.board[i][1] == self.emptyChar:
                    self.board[i][1] = self.playerChar
                    return True
        return False
            
    def tryAny(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == self.emptyChar:
                    self.board[i][j] = self.playerChar
                    return True
        return False


    # IDLE = 0
    # PLAYING = 1
    # LOST = 2
    # WON = 3
    # VELHA = 4
    # DEFENDED = 5
    # PLACE_BORDER = 6
    # PLACE_MIDDLE = 7
        

    def iteration(self):
        state = State.IDLE
        if self.tryToFinish(): return State.WON
        if self.defend(): return State.DEFENDED
        if self.tryMiddle(): return State.PLACE_MIDDLE
        #if self.tryBorders(): return State.PLACE_BORDER
        if self.board[1][1] == self.oponentChar:
            if self.tryBorders(): return State.PLACE_BORDER
        else:
            if self.trySides(): return State.PLACE_SIDES
        if self.tryAny(): return State.PLAYING
        return state.VELHA
    
    def nextMove(self):
        oldBoard = deepcopy(self.board)
        state = self.iteration()
        for i in range(3):
            for j in range(3):
                if oldBoard[i][j] != self.board[i][j]:
                    return state,i,j
        return State.VELHA,-1,-1

# board = Board('O', 'X')

# state = State.PLAYING

# while state != State.IDLE and state != State.WON and state != State.LOST and state != State.VELHA:
    

#     y = int(input())
#     x = int(input())
#     board.place(board.oponentChar, x, y)
#     state = board.iteration()
#     print("STATE: "+str(state))
#     board.print()

