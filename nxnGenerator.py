from random import randint, shuffle
import copy


#####-----CLASS START----------------------



#degree of puzzle
n = 3

#initializes n*n by n*n grid of zeros
rows, cols = (n*n), (n*n)
grid = [[-1]*cols for _ in range((rows))]

#solved puzzle
solvedPuzzle = grid

#list of possible numbers
numberList = list(range(1,(n*n)+1))
#print(numberList)

counter = 1

    #creates puzzle
def gen():
    global counter
    fillGrid(grid)
    #print(grid)
    global solvedPuzzle
    solvedPuzzle = list(map(list, grid))
    attempts = 3
    #counter=1
    while attempts > 0:
        #print(grid)
        #Select a random cell that is not already empty
        row = randint(0,((n*n)-1))
        col = randint(0,((n*n)-1))
        while grid[row][col]==0:
            row = randint(0,((n*n)-1))
            col = randint(0,((n*n)-1))
        #backup incase there are more solutions
        backup = grid[row][col]
        grid[row][col]=(-1)
        #Copy the grid
        copyGrid = []
        for r in range(0,(n*n)):
            copyGrid.append([])
            for c in range(0,(n*n)):
                copyGrid[r].append(grid[r][c])
        #Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
        counter = 0
        solveGrid(copyGrid)
        #If the number of solution is different from 1 then the value has to be reverted
        if (counter!=1):
            grid[row][col] = backup
            attempts -= 1 #allows for specific number tries before the puzzle is declared finale
            #print(attempts)

    return(grid)
    #return gridToString(grid)

#turn grid to string
def gridToString(puzzle):
    s = ' '.join([' '.join(map(str, row)) for row in puzzle])
    #s = s.replace(" ","")
    return s


#backtrace function(recursive) thats checks all possible solutions until a single solution is found
def solveGrid(grid):
  global counter
  #Find next empty cell
  for i in range(0,(n**4)):
    row=i//(n*n)
    col=i%(n*n)
    if grid[row][col]==(-1):
      for value in range (1,(n*n + 1)):
        #Check that this value has not already be used on this row
        if not(value in grid[row]):
          #Check that this value has not already be used on this column
          if (not valueInCol(col, value)):
            if (not valueInSquare(row, col, value)):
              grid[row][col]=value
              if checkGrid(grid):
                counter = counter + 1
                #return True
                break
              else:
                if solveGrid(grid):
                  return True
      break
  grid[row][col]=(-1)




#creates full grid of numbers that is a valid sudoku solution
def fillGrid(grid):
  global counter
  #Find next empty cell
  for i in range(0,(n**4)):
    row=i//(n*n)
    col=i%(n*n)
    if grid[row][col]==(-1):
      shuffle(numberList)
      for value in numberList:
        #Check that this value has not already be used on this row
        if not(value in grid[row]):
          #Check that this value has not already be used on this column
          if (not valueInCol(col, value)):
            #Check if value is not in square
            if (not valueInSquare(row, col, value)):
              grid[row][col]=value
              if checkGrid(grid):
                return True
              else:
                if fillGrid(grid):
                  return True
      break
  grid[row][col]=(-1)

#returns true if value is in the column
def valueInCol(col, value):
    for row in grid:
        if(row[col]==value):
            return True
    return False

#returns true if value is in square
def valueInSquare(row, col, value):
    squareRow = row//n
    squareCol = col//n
    square = []
    for i in range(n*n): #row traversal of grid
        if((i <= (squareRow * n)) and (i >= ((squareRow * n) + (n-1)))): #selecting correct rows
            square.append(grid[i][(squareCol * n):((squareCol * n) + (n-1))]) #appending correct slices of the rows to the square

    for row in square:
        if value in row:
            return True
    return False

#check if grid is full
def checkGrid(grid):
    for row in range(0,(n*n)):
        for col in range(0,(n*n)):
            if grid[row][col]==(-1):
                return False

    return True


#####-----CLASS END----------------------

#creates a grid for the solutions to go in with length 3 and width 2
gor,cor = (10000),(2)
gridOfPuzzles = [[""]*cor for _ in range((gor))]

#fills grid of puzzles with all puzzles
for i in range(gor):
    #print("hi")
    r = randint(2,5) # range of n for all puzzles
    print(i, ":", r)
    n = r
    #initializes n*n by n*n grid to zeros
    rows, cols = (n*n), (n*n)
    grid = [[-1]*cols for _ in range((rows))]

    numberList = list(range(1,(n*n)+1))

    gen()
    gridOfPuzzles[i][0] = gridToString(grid)
    gridOfPuzzles[i][1] = gridToString(solvedPuzzle)
    grid = [[-1]*cols for _ in range((rows))]
    solvedPuzzle = [[-1]*cols for _ in range((rows))]

#writing to read_csv
import os
os.remove("nxnData.csv")
f = open("nxnData.csv", "x")

for r in range(len(gridOfPuzzles)):
        f.write(gridOfPuzzles[r][0]+ "," + gridOfPuzzles[r][1] + "\n")

f.close()
