import os
from SB_Agent import Agent
from SB_environment import Sokoban

    

if __name__=="__main__":
    # board = [
	#     ['#', '#', '#', '#', '#', '#', ' ', ' ', ],
    #     ['#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ],
    #     ['#', ' ', ' ', '$', ' ', '#', '#', ' ', ],
    #     ['#', ' ', '$', '#', '.', '@', '#', '#', ],
    #     ['#', '#', ' ', ' ', '*', '.', ' ', '#', ],
    #     [' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ],
    #     [' ', '#', '#', '#', '#', '#', '#', '#', ],
    #     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ]]
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
    board=[
	[' ',' ','#','#','#','#','#',' '],           
    ['#','#','#',' ',' ',' ','#',' '],  
    ['#','.','@','$',' ',' ','#',' '],    
    ['#','#','#',' ','$','.','#',' '],  
    ['#','.','#','#','$',' ','#',' '],  
    ['#',' ','#',' ','.',' ','#','#'],  
    ['#','$',' ','*','$','$','.','#'],
    ['#',' ',' ',' ','.',' ',' ','#'],  
    ['#','#','#','#','#','#','#','#']]

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

    agnt=Agent(SBobj)

    resultbfs, counterbsf = agnt.BFS()

    try:
        os.remove("pathBFS.txt")
    except:
        pass
    path=agnt.printPath(resultbfs,"pathBFS.txt")
    
    resultdfs, counterdfs = agnt.DFS()
    try:
        os.remove("pathDFS.txt")
    except:
        pass
    pathdfs = agnt.printPath(resultdfs, "pathDSF.txt")


    agnt.main(pathdfs)
    agnt.main(path)

    print("Nodes explored: ",counterdfs)
    print("Path length: ",resultdfs.level)
    
    print("Nodes explored: ",counterbsf)
    print("Path length: ",resultbfs.level)