import os
from SB_Agent import Agent
from SB_environment import Sokoban

    

if __name__=="__main__":
    board = [
	    ['#', '#', '#', '#', '#', '#', ' ', ' ', ],
        ['#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ],
        ['#', ' ', ' ', '$', ' ', '#', '#', ' ', ],
        ['#', ' ', '$', '#', '.', '@', '#', '#', ],
        ['#', '#', ' ', ' ', '*', '.', ' ', '#', ],
        [' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ],
        [' ', '#', '#', '#', '#', '#', '#', '#', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ]]
    # board = [
	# [' ', '#','#','#','#','#',' ',' ',],
    # [' ', '#',' ','@',' ','#','#','#',],
    # ['#', '#',' ','#','$',' ',' ','#',],
    # ['#', ' ','*','.',' ','.',' ','#',],
    # ['#', ' ',' ','$','$',' ','#','#',],
    # ['#', '#','#',' ','#','.','#',' ',],
    # [' ', ' ','#',' ',' ',' ','#',' ',],
    # [' ', ' ','#','#','#','#','#',' ',],
    # [' ', ' ',' ',' ',' ',' ',' ',' ',]]
    # board=[
	# [' ',' ','#','#','#','#','#',' '],           
    # ['#','#','#',' ',' ',' ','#',' '],  
    # ['#','.','@','$',' ',' ','#',' '],    
    # ['#','#','#',' ','$','.','#',' '],  
    # ['#','.','#','#','$',' ','#',' '],  
    # ['#',' ','#',' ','.',' ','#','#'],  
    # ['#','$',' ','*','$','$','.','#'],
    # ['#',' ',' ',' ','.',' ',' ','#'],  
    # ['#','#','#','#','#','#','#','#']]

    workerPosX=None
    workerPosY=None
    boxPos =[]
    goalPos= []
    
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == '@':
                workerPosX=x
                workerPosY=y
                board[x][y]=' '
            if board[x][y] == '$':
                boxPos.append((x,y))
                board[x][y]=' '
            if board[x][y] =='.':
                goalPos.append((x,y))
                board[x][y]=' '
            if board[x][y] == '+':
                workerPosX=x
                workerPosY=y
                goalPos.append((x,y))
                board[x][y]=' '
            if board[x][y] == '*':
                boxPos.append((x,y))
                goalPos.append((x,y))
                board[x][y]=' '

    workerPos=(workerPosX,workerPosY)

    SBobj=Sokoban(board,boxPos,goalPos,workerPos)        
    print(" Path by BFS ")
    agnt1=Agent(SBobj)

    resultbfs, counterbsf = agnt1.BFS()

    try:
        os.remove("pathBFS.txt")
    except:
        pass
    path=agnt1.printPath(resultbfs,"pathBFS.txt")

    print("Nodes explored: ", counterbsf)
    print("Path length: ", resultbfs.level)
  
    agnt2 = Agent(SBobj)

    resultdfs, counterdfs = agnt2.DFS()

    try:
        os.remove("path.txt")
    except:
        pass
    pathdfs = agnt2.printPath(resultdfs, "path.txt")
    print(" Path by DFS \n")
    print("Nodes explored: ", counterdfs)
    print("Path length: ", resultdfs.level)

    agnt1.main(path)