import pygame
import time
import pickle

pygame.init()

# size = 5
# board = [[False for x in xrange(size)] for x in xrange(size)]
# board[0][0] = True
# board[0][1] = True

# board[1][0] = True
# board[1][1] = True
# board[1][2] = True

# board[2][1] = True
# board[2][2] = True
# board[2][3] = True


# board[0][0] = True
# board[1][0] = True
# board[0][1] = True
# board[1][1] = True
# board[2][2] = True
# board[3][2] = True
# board[2][3] = True
# board[3][3] = True


block_size = 10

# Draws a window
def draw(board,size):
    #create the screen

    #draw a line - see http://www.pygame.org/docs/ref/draw.html for more
    # pygame.draw.line(window, (255, 255, 255), (0, 0), (30, 50))
    window = pygame.display.set_mode((size*block_size, size*block_size))
    window.fill((255, 255, 255))

    for x in xrange(size):
        # s = ""
        for y in xrange(size):
            if board[x][y]:
                # s += str(1)
                pygame.draw.rect(window, (0, 0, 0),
                    pygame.Rect(x*block_size, y*block_size,
                        block_size, block_size), 0)
    pygame.display.flip()

# step board
def step(board,size):
    new_board = [[False for x in xrange(size)] for x in xrange(size)]
    for x in xrange(size):
        for y in xrange(size):
            n = 0
            for s in [[-1, -1], [0, -1], [1, -1],
                     [-1, 0], [1, 0],
                     [-1, 1], [0, 1], [1, 1]]:
                if 0 <= x+s[0] < size and 0 <= y+s[1] < size:
                    if board[x+s[0]][y+s[1]]:
                        n += 1
            if board[x][y]:
                if n == 0 or n == 1:
                    new_board[x][y] = False
                elif n == 2 or n == 3:
                    new_board[x][y] = True
                elif n >= 2:
                    new_board[x][y] = False
            else:
                if n == 3:
                    new_board[x][y] = True
    return new_board

# print ascii to terminal
def print_board(board,size):
    for x in xrange(size):
        s = ""
        for y in xrange(size):
            if board[x][y]:
                s += str(1)
            else:
                s += str(0)
        print(s)
    print("")

# takes a number and turns it into board
def numberToBoard(i,size):
    b = bin(i).lstrip("0b").rjust(size*size, "0")
    board = [[ b[x*size+y]== "1" for y in xrange(size)] for x in xrange(size)]
    return board

# takes a 5x5 grid number (border) and a 3x3 grid number (center) and combine into a 5x5 board
def numbersToBoard(center,border):
    b_border = bin(border).lstrip("0b").rjust(25, "0")
    b_center = bin(center).lstrip("0b").rjust(9, "0")
    c = [6,7,8,11,12,13,16,17,18]
    b_border = list(b_border)
    for x in range(9):
        b_border[c[x]] = b_center[x]
    b_border = "".join(b_border)
    board = [[ b_border[x*5+y]== "1" for y in xrange(5)] for x in xrange(5)]
    return board

# takes a board and turns into a number
def boardToNumber(board,size):
    b = ""
    for x in xrange(size):
        for y in xrange(size):
            if board[x][y]:
                b += "1"
            else:
                b += "0"
    return int(b,2)

# takes a 5x5 board and returns a number for the 3x3 grid
def midBoardToNumber(board):
    b = ""
    for x in range(1, 3):
        for y in range(1, 3):
            if board[x][y]:
                b += "1"
            else:
                b += "0"
    return int(b, 2)

# tries to find all boards that will step to this board
def bruteforce(board,size):
    for i in xrange(2**(size**2)):
        print i
        newBoard = numberToBoard(i,size)
        steppedBoard = step(newBoard,size)
        same = True
        for x in xrange(size):
            for y in xrange(size):
                if steppedBoard[x][y] != board[x][y]:
                    same = False
                    break
            if not same:
                break
        if same:
            print_board(newBoard,size)

# takes a 3x3 grid and rotates it
def rotateBoard(board):
    new_board = [[False for x in xrange(3)] for x in xrange(3)]
    for x in xrange(3):
        for y in xrange(3):
            new_board[y][2-x] = board[x][y]
    return new_board
    
# flips board over
def flip(board):
    for x in xrange(3):
        a = board[x]
        t = a[0]
        a[0] = a[2]
        a[2] = t
        board[x] = a
    return board

# takes find all 3x3 board steps
def preTrain(a,center,border):
    for c in center:
        for b in border:
            newBoard = numbersToBoard(c,b)
            draw(newBoard,5)
            steppedBoard = step(newBoard,5)
            steppedInt = midBoardToNumber(steppedBoard)
            a[steppedInt][c] += 1
    return a

def findAllSimular(a):
    for i in range(512):
        a[i] = findSimular(a,i)
    for i in range(512):
        a[i] = findSimular(a,i)

def findSimular(a,x):
    if a[x] > x:
        a[x] = x
        print str(x)+" to "+str(x)
        newBoard = numberToBoard(x,3)
        rotated = newBoard
        for i in xrange(3):
            rotated = rotateBoard(rotated,3)
            rotatedInt = boardToNumber(rotated,3)
            print rotatedInt
            if rotatedInt > x :
                a[rotatedInt] = x
        rotated = flip(rotated)
        for i in xrange(4):
            rotated = rotateBoard(rotated,3)
            rotatedInt = boardToNumber(rotated,3)
            print rotatedInt
            if rotatedInt > x :
                a[rotatedInt] = x
        return x
    else:
        n = a[x]
        if a[n] == n:
            return n
        else:
            return findSimular(a,n)

def listSimular(a, x):
    x = a[x]
    s = []
    for i in xrange(512):
        if a[i] == x :
            s.append(i)
    return s

def listBase(a):
    b = []
    for i in range(512):
        if a[i] == i:
            b.append(i)
    return b

def listAround():
    a = []
    c = [6,7,8,11,12,13,16,17,18]
    for i in xrange(2**(5**2)):
        if i % 1000 == 0:
            print i
        b = bin(i).lstrip("0b").rjust(25, "0")
        if sum([int(b[x]) for x in c]) == 0:
            a.append(i)
    return a

# returns a string of how to rotate and flip to get from board a to b
def movement(a,b):
    if a == b:
        return "" 
    newBoard = numberToBoard(a,3)
    
    m = ""
    rotated = newBoard
    for i in xrange(3):
        m += "r"
        rotated = rotateBoard(rotated)
        rotatedInt = boardToNumber(rotated,3)
        if rotatedInt == b: 
            return m 


    newBoard = numberToBoard(a,3)
    m = "f"
    rotated = flip(newBoard)
    for i in xrange(4):
        m += "r"
        rotated = rotateBoard(rotated)
        rotatedInt = boardToNumber(rotated,3)
        if rotatedInt == b:
            return m 
    
    return "n"

def doMovement(a,m):
    for c in m:
        if c == "r":
            a = rotateBoard(a)
        if c == "f":
            a = flip(a)
    return a



# findAllSimular(a)
# print a
# s = listSimular(a,3)
# b = listBase(a)

# for i in s:
#     print i
#     draw(numberToBoard(i))
#     time.sleep(1)

# c = listAround()

# pickle.dump( a, open( "a.dat", "wb" ) )
# pickle.dump( c, open( "c.dat", "wb" ) )

# a = pickle.load( open( "a.dat", "rb" ) )
# print a
# for i in range(512):
#     print str(i) + ": " + movement(i,a[i])
# b = listBase(a)

# a_board = numberToBoard(a[13])
# print_board(a_board)
# c = pickle.load( open( "c.dat", "rb" ) )
# print c[0]


# a = [[0 for y in xrange(2**9)] for x in xrange(2**9)]
# preTrain(a,b,c)
# print a
# pickle.dump( a, open( "preTrain.dat", "wb" ) )
a = pickle.load( open( "preTrain.dat", "rb" ) )
# print a
b = {}
for i in range(len(a)):
    perdiction = a[i] 
    b[i] = {}
    for j in range(len(perdiction)):
        if perdiction[j] != 0:
            print str(i) + " " + str(j) + " count: " + str(perdiction[j])
            b[i][j] = perdiction[j]
print b

# numbersToBoard(c[0])

# print ""
# c_board = numberToBoard(c[13])
# print_board(c_board)


# numbersToBoard(,border)

# for i in b:
#     print i
#     draw(numberToBoard(i,3),3)
#     time.sleep(0.1)

# for i in b:
#     print i
#     draw(numbersToBoard(i,c[0]),5)
#     time.sleep(0.1)



# a = [[0 for y in xrange(2**9)] for x in xrange(2**9)]
# preTrain(a)
# print a

# with open('preTrain.obj', 'wb') as output:
#     pickle.dump(a, output, pickle.HIGHEST_PROTOCOL)

# bruteforce(board)
# draw(board)

# for x in xrange(1, 4):
#     time.sleep(1)
#     board = rotateBoard(board)
#     draw(board)

# time.sleep(1)
# board = flip(board)
# draw(board)

# for x in xrange(1, 4):
#     time.sleep(1)
#     board = rotateBoard(board)
#     draw(board)