from SB_environment import Sokoban,Node
from queue import PriorityQueue
import copy
import time
import pygame
import sys



class Agent:

    def __init__(self, sokoban):
        self.sokoban = sokoban
        self.frontier = PriorityQueue()
        self.explored = {}
        self.stack=[]

    def PBCheck(self, boxR,boxC, boxPos, parent,depth):
        board = self.sokoban.board
        goalPos = self.sokoban.goal

        if depth>len(boxPos):
            return True

        hBlocked=None
        vBlocked=None

        # Pakke Wale Status       
        # Horizontal check
        if (board[boxR][boxC-1]==" " and (boxR,boxC-1) not in boxPos) and (board[boxR][boxC+1]==" " and (boxR,boxC+1) not in boxPos):
            return False
        # vertical check
        elif (board[boxR-1][boxC]==" " and (boxR-1,boxC) not in boxPos) and (board[boxR+1][boxC]==" " and (boxR+1,boxC) not in boxPos):
            return False
        
        # checking for wall
        # wall in horizontal dir
        if board[boxR][boxC-1]=="#" or board[boxR][boxC+1]=="#":
            hBlocked=True
        # wall in vertical dir
        if board[boxR-1][boxC]=="#" or board[boxR+1][boxC]=="#":
            vBlocked=True


        # checking for boxes
        # Left or Right position containing box
        if not hBlocked and ((boxR,boxC-1) in boxPos or (boxR,boxC+1) in boxPos):
            
            # Checking if Left box if free or not.
            lbox=rbox=None
            if (boxR,boxC-1) in boxPos:
                if (boxR,boxC-1)==parent:
                    lbox=True
                else:
                    lbox= self.PBCheck(boxR,boxC-1,boxPos,(boxR,boxC),depth+1)
                
            # Checking if Right box if free or not
            if (boxR,boxC+1) in boxPos:
                if (boxR,boxC+1) == parent:
                    rbox=True
                else:
                    rbox = self.PBCheck(boxR,boxC+1,boxPos,(boxR,boxC),depth+1)

            # If both left and right boxes are movable(false) then return false
            # else return true
            # if lbox==False and rbox==False:
            if not (lbox or rbox):
                hBlocked=False
            else:
                hBlocked=True
        
        # box at up or down position
        if not vBlocked and ((boxR-1,boxC) in boxPos or (boxR+1,boxC) in boxPos):
            
            # Checking if upper box if free or not
            ubox=dbox=None
            if (boxR-1,boxC) in boxPos:
                if (boxR-1,boxC)==parent:
                    ubox=True
                else:
                    ubox=self.PBCheck(boxR-1,boxC,boxPos,(boxR,boxC),depth+1)
                
            # Checking if lower(down) box if free or not
            if (boxR+1,boxC) in boxPos:
                if (boxR+1,boxC) == parent:
                    dbox=True
                else:
                    dbox = self.PBCheck(boxR+1,boxC,boxPos,(boxR,boxC),depth+1)

            # If both up and down boxes are movable(false) then return false
            # else return true
            # if lbox==False and rbox==False:
            if not (ubox or dbox):
                vBlocked=False
            else:
                vBlocked=True
            
        # deadlock
        if hBlocked and vBlocked:
            return True
        else:
            return False

    def isGoal(self,node):
        goal=self.sokoban.goal
        boxPos=node.boxPos

        if set(goal)==set(boxPos):
            return True
        else:
            return False

    def heuristic(self,node,goal):
        boxPos=copy.deepcopy(node.boxPos)
        boxPos.sort(key = lambda x: x[0] + x[1])

        cost=0

        for i in range(len(boxPos)):
            cost+=abs(boxPos[i][0]-goal[i][0])+abs(boxPos[i][1]-goal[i][1])

        return cost


    def conf2str(self,node):
        """
           Function to convert boxPos and workerPos to string 
           This function is used for hashing of configuration
        """
        result=""

        srted=set(node.boxPos)

        for r,c in srted:
            result=result+str(r)+str(c)

        result=result+str(node.workerPosX)+str(node.workerPosY)

        return result


    def printPath(self,node,filename):
        
        if(node != None):
            
            result=self.printPath(node.parent,filename)
            result.append(node)

            node.Print(self.sokoban,filename)
            return result

        else:
            return []


    def DFS(self):
        frontier = self.stack
        explored = self.explored
        goal=self.sokoban.goal
    
        frontier.append(self.sokoban.root)
        counter=0

        while len(frontier)>0:
            
            node = frontier.pop(-1)
            # node.Print(self.sokoban)
            if counter%10000==0:
                print(counter)
                
            counter+=1            
            
            # Add current node to explored
            explored[self.conf2str(node)]=None

            # Check if current node is goal node
            if self.isGoal(node):
                return node,counter

            # Find children of current node
            children=self.sokoban.moves(node)

            # Check for deadlock in all children's configuration which are not on goal pos
            # Calculate heuristic value for all valid child
            # Push them to frontier
            for child in children:

                configurationStr = self.conf2str(child)
                if configurationStr not in explored:

                # flag-> false means current configuration has no deadlock and is default behaviour    
                # If any box which is not on goal position and is permanent blocked then there is a deadlock
                    flag=False
                    for boxR,boxC in child.boxPos:
                        if (boxR,boxC) not in goal:
                            if self.PBCheck(boxR,boxC,child.boxPos,(-1,-1),1):
                                
                                flag=True
                                break
                    # deadlock -> prun the branch
                    if flag:
                        del(child)
                        continue

                    frontier.append(child)

                # already visited (infinite loop)
                else:
                    del(child)
                
        return None

    def BFS(self):
        frontier = self.frontier
        explored = self.explored
        goal=self.sokoban.goal
    
        frontier.put(self.sokoban.root)
        counter=0

        while not frontier.empty():
            
            node = frontier.get()
            # node.Print(self.sokoban,"path.txt")
            if counter%10000==0:
                print(counter)
                
            counter+=1            
            
            # Add current node to explored
            explored[self.conf2str(node)]=None

            # Check if current node is goal node
            if self.isGoal(node):
                return node,counter

            # Find children of current node
            children=self.sokoban.moves(node)

            # Check for deadlock in all children's configuration which are not on goal pos
            # Calculate heuristic value for all valid child
            # Push them to frontier
            for child in children:

                configurationStr = self.conf2str(child)
                if configurationStr not in explored:

                # flag-> false means current configuration has no deadlock and is default behaviour    
                # If any box which is not on goal position and is permanent blocked then there is a deadlock
                    flag=False
                    for boxR,boxC in child.boxPos:
                        if (boxR,boxC) not in goal:
                            if self.PBCheck(boxR,boxC,child.boxPos,(-1,-1),1):
                                
                                flag=True
                                break
                            
                    if flag:
                        del(child)
                        continue
                    
                    # if h(x) is included
                    child.cost=self.heuristic(child,goal)+child.level     # cost = h(x) + g(x)
                    # child.cost=child.level
                    frontier.put(child)

                else:
                    del(child)
                
        return None



    def main(self,path):
        board=self.sokoban.board

        BLACK = (0, 0, 0)
        WINDOW_HEIGHT = len(board)*36
        WINDOW_WIDTH = len(board[0])*36

        pygame.display.set_caption('Sokoban')
        print("[+] Initailizing game...")

        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        SCREEN.fill(BLACK)

        print("[+] Rendering graphics...")
        for node in path:
            # print(WINDOW_WIDTH)
            # print(f"    WINDOW_HEIGHT -> {WINDOW_HEIGHT} \n    WINDOW_WIDTH -> {WINDOW_WIDTH}")
            self.drawGrid(node)
            print("[+] Done!")

            pygame.display.update()

            time.sleep(1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("[+] Quiting...")
                    pygame.quit()
                    sys.exit()

    def drawGrid(self,node):
        board=self.sokoban.board
        WINDOW_HEIGHT = len(board)*36
        WINDOW_WIDTH = len(board[0])*36

        display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Load level images
        wall = pygame.image.load(
            'AI Sokoban\\imgs\\wall.png').convert()
        box = pygame.image.load('AI Sokoban\\imgs\\box.png').convert()
        box_on_target = pygame.image.load(
            'AI Sokoban\\imgs\\box_on_target.png').convert()
        player_on_target = pygame.image.load(
            'AI Sokoban\\imgs\\player_on_targe.png').convert()
        space = pygame.image.load('AI Sokoban\\imgs\\grounds.png').convert()
        target = pygame.image.load('AI Sokoban\\imgs\\target.png').convert()
        player = pygame.image.load('AI Sokoban\\imgs\\player.png').convert()

        blockSize = 36  # Set the size of the grid block
        for x in range(0, WINDOW_HEIGHT, blockSize):
            for y in range(0, WINDOW_WIDTH, blockSize):

                # print(f"({x//blockSize},{y//blockSize})    ====>    {mat[x//blockSize][y//blockSize]}")
                if board[x//blockSize][y//blockSize] == "#":
                    display_surface.blit(wall, (y, x))

                if board[x//blockSize][y//blockSize] == " ":
                    display_surface.blit(space, (y, x))

                if (x//blockSize,y//blockSize) in node.boxPos :
                    display_surface.blit(box, (y, x))

                if (x//blockSize,y//blockSize) in self.sokoban.goal:
                    display_surface.blit(target, (y, x))

                if (x//blockSize,y//blockSize) in self.sokoban.goal and (x//blockSize,y//blockSize) in node.boxPos:
                    display_surface.blit(box_on_target, (y, x))

                if (x//blockSize,y//blockSize) == (node.workerPosX,node.workerPosY):
                    display_surface.blit(player, (y, x))
                    if (x//blockSize,y//blockSize) in self.sokoban.goal:
                        display_surface.blit(player_on_target, (y, x))