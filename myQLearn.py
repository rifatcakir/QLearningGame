# -*- coding: utf-8 -*-
"""
Created on Tue May  4 14:20:33 2021

@author: RIFAT
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import array as arr
import random
import time
from runnerClass import Runner

## Create Map
map = np.array([[ 0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [ 0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [ 0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0]])

mapCordinateAdress = np.array([[ 0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [ 0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [ 0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0],
       [0,  0,  0, 0,  0, 0,  0,  0,  0,  0,  0, 0,  0]])


def appendAgents():
    map[5][5]=-1
    map[3][11]=1
    map[7][11]=2
    
chaser1Score=0
chaser2Score=0


def convertedMap(i):
    if(i==0):
        return '-'
    if(i==-1):
        return 'R'
    if(i==1):
        return 'C1'
    if(i==2):
        return 'C2'
    if(i==9):
        return 'X'
    return i

def printBoard():
  lines = []
  # represent original map more simple
  mapForUI = map
  i = len(mapForUI)
  for row in mapForUI:
    lines.append(str((i))+" "+'   '.join(str(convertedMap(mapForUI)) for mapForUI in row))
    i-=1

  charset="  "
  for i in range(13):
    charset+=(chr(97+i)+"   ")
  lines.append(charset)
  print('\n'.join(lines))
  
  
# Map object list into tuples to create valid paths
def createBoardList():
    unique_list = []
    for i in range(len(map)):
      for j in range(len(map[i])):
        # check for all directions 
        # Note added +1 for all i 
        # otherwise there is wrong mapping for x=0 y= 10 => 010 and x=1 y=0 => 10
        nodeF=str(i+1)+str(j)
        if( j+1<len(map) and map[i][j+1] != 9 and map[i][j] != 9  ):
            nodeS=str(i+1)+str(j+1)
            mtuple=(int(nodeF),int(nodeS))
            unique_list.append(mtuple)
        if( j-1>-1 and map[i][j-1] != 9 and map[i][j] != 9  ):
            nodeS=str(i+1)+str(j-1)
            mtuple=(int(nodeF),int(nodeS))
            unique_list.append(mtuple)
    
        if( i-1>-1 and map[i-1][j] != 9 and map[i][j] != 9 ):
            nodeS=str(i+1-1)+str(j)
            mtuple=(int(nodeF),int(nodeS))
            unique_list.append(mtuple)
        if( i+1<len(map) and map[i+1][j] != 9 and map[i][j] != 9 ):
            nodeS=str(i+1+1)+str(j)
            mtuple=(int(nodeF),int(nodeS))
            unique_list.append(mtuple)
        global mapCordinateAdress
        mapCordinateAdress[i][j]=nodeF
    return unique_list
  
def createGraph(boardList):
    G = nx.Graph()
    G.add_edges_from(boardList)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos)
    nx.draw_networkx_edges(G,pos)
    nx.draw_networkx_labels(G,pos)
    #plt.show() uncomment to see how graph is created
    return G

    
def initializeRewardMatrix(G,targetPos):
    R = np.matrix(np.zeros(shape=(820,820)))
    for a in G[targetPos]:
       R[a,targetPos]=100
    return R
       
def initializeQMatrix(G):
    Q = np.matrix(np.zeros(shape=(820,820)))
    Q-=100
    for node in G.nodes:
      for a in G[node]:
        Q[node,a]=0
        Q[a,node]=0
    return Q

def randomCellOfMap():
    # unique tuples
    xRange =list(range(8))
    yRange = list(range(13))
    rndX= random.choice(xRange)
    rndY= random.choice(yRange)
    return mapCordinateAdress[rndX,rndY]

def next_number(start,er,G,Q):
  random_value = randomCellOfMap()
  if random_value<er:
      sample=G[start]
  else:
      sample=np.where(Q[start,] == np.max(Q[start,]))[1]
  next_node = int(np.random.choice(sample,1))
  return next_node

def updateQ(node1,node2,lr,discount,Q,R):
  max_index = np.where(Q[node2,] == np.max(Q[node2,]))[1]
  if max_index.shape[0] > 1:
    max_index = int(np.random.choice(max_index,size=1))
  else:
    max_index = int(max_index)
  max_value=Q[node2,max_index]
  Q[node1,node2] = int((1-lr)*Q[node1,node2]+lr*(R[node1,node2]+discount*max_value))

def learner(er,lr,discount,boardList,G,Q,R):
  for i in range(5000):
    rnd = random.choice(boardList)
    start = rnd[0]
    next_node = next_number(start,er,G,Q)
    updateQ(start,next_node,lr,discount,Q,R)



def shortest_path(begin,end,Q):
  path=[begin]
  next_node = np.argmax(Q[begin,])
  path.append(next_node)
  next_node = np.argmax(Q[next_node,])
  path.append(next_node)
  return path
  # while next_node !=end:
  #   next_node = np.argmax(Q[next_node,])
  #   path.append(next_node)
  #   print(next_node)
  # return path

    
def allocateBlockOnMap(numberOfBlock):
    splittedInput = numberOfBlock.split(" ")
    y=ord(splittedInput[0])-97
    x=8-int(splittedInput[1])
    if(map[x,y]==0):
        map[x,y]=9
        return True
    else:
        return False
    
def convertStringPositionToCordination(position):
    splittedInput = position.split(" ")
    y=ord(splittedInput[0])-97
    x=8-int(splittedInput[1])
    positionList=[]
    positionList.append(x)
    positionList.append(y)
    return positionList

def randomBlocksOnMap(numberOfBlock):
   # unique tuples
   xRange =list(range(8))
   yRange = list(range(13))
   i = 0
   while i < numberOfBlock:
      rndX= random.choice(xRange)
      rndY= random.choice(yRange)
      if(map[rndX,rndY]==0):
          map[rndX,rndY]=9
          i+=1


   
def changePiecePosition(x,y,target):
    x=x[0]
    y=y[0]
    targetX=target[0]
    targetY=target[1]
    currentOpjectOnPossition = map[x][y]
    # free space
    map[x][y]=0
    # assign it into new possition
    map[targetX][targetY]=currentOpjectOnPossition
    print("Runner moved ("+str(x)+","+str(y)+") to ("+str(targetX)+","+str(targetY)+")")
    
## Define runner    
runner = Runner()
winner = 0
def trainModel(chaserType):
    # Get runner position
    r_pos = np.where(map == -1)
    x, y = r_pos[0], r_pos[1]
    x=x[0]
    y=y[0]
    targetPos = str(x)+str(y)
    targetPos = mapCordinateAdress[x][y]
    boardList=createBoardList()
    
    R = initializeRewardMatrix(G,targetPos)
    Q = initializeQMatrix(G)
    # Learn different for any chasers
    if(chaserType==1):
    # exploration rate, learning rate, discount factor of learning
        learner(0.8,0.8,0.8,boardList,G,Q,R)
    else:
        learner(0.5,0.8,0.8,boardList,G,Q,R)
    return Q

def takeOtherChaserPosition(chaserType):
    if(chaserType==1):
        return np.where(map == 2)
    else:
        return np.where(map == 1)

def addPoint(point,chaserType):
    if(chaserType==1):
        global chaser1Score
        chaser1Score += point
    else:
        global chaser2Score
        chaser2Score+=point

# calculate manathen distance and add points
def calculateEarnedPoint(x1,y1,x2,y2,chaserType):
    distance = abs(x1 - y1) + abs(x2 - y2)
    if(distance==2):
        addPoint(1,chaserType)
    elif(distance==1):
        addPoint(2,chaserType)
        

def playChaser(chaserType):
    # Get runner position
    # Train model based on the chaserType
    trainedModel = trainModel(chaserType)
    r_pos = np.where(map == -1)
    x, y = r_pos[0], r_pos[1]
    x=x[0]
    y=y[0]
    startX= x
    startY = y
    targetPos = str(x)+str(y)
    targetPos = mapCordinateAdress[x][y]
    # Get chaser position
    r_pos = np.where(map == chaserType)
    x, y = r_pos[0], r_pos[1]
    dontChangecurrentPiece = False
    if(x.size == 0): # chasers are on the same place and this one not found
        # take other chaser's position
        #print("Chaser not found!")
        dontChangecurrentPiece= True
        r_pos = takeOtherChaserPosition(chaserType)
        x, y = r_pos[0], r_pos[1]
    x=x[0]
    y=y[0]
    startPos = str(x)+str(y)
    startPos = mapCordinateAdress[x][y]
    pathm = shortest_path(startPos,targetPos,trainedModel)
    # whole path 
    # Set free current chaser position
    if(dontChangecurrentPiece==False):
        map[x][y]=0
    nextStep = pathm[1]
    r_pos = np.where(mapCordinateAdress == nextStep)
    x, y = r_pos[0], r_pos[1]
    x=x[0]
    y=y[0]
    moveLog = "Chaser -> "+str(chaserType)
    moveLog +=  " moved: ("+str(startX)+","+str(startY)+") "
    moveLog +=  "("+str(x)+","+str(y)+")"
    print(moveLog)
    # Calculate Points
    calculateEarnedPoint(startX,startY,x,y,chaserType)
    if(map[x][y]==-1):
        global winner
        winner = chaserType
    map[x][y]=chaserType

       

def playRunner(runnerControllMethod):
    r_pos = np.where(map == -1)
    x, y = r_pos[0], r_pos[1]
    if(runnerControllMethod=="p"):
        runnerDecision = runner.play(map)
        changePiecePosition(x,y,runnerDecision)
    else:
        printBoard()
        print("Enter new position of R:\n Example: a 5\n")
        targetPos = convertStringPositionToCordination(input())
        changePiecePosition(x,y,targetPos)

def isGameOver():
    if(winner!=0):
       print("Chaser"+str(winner)+" won the game!")
       return True
    return False

# work()
# colorPath()
# printBoard()
#G = createGraph(createBoardList())


## MAIN MENU 
def mainMenu():
    print("Do you wanna set initial Runner and chasers position? [y/n]")
    initialPositionDecisition=input()
    if(initialPositionDecisition=='n'):
        appendAgents()
    else:
        global map
        print("Enter the runner position? Ex:a 1")
        position = convertStringPositionToCordination(input())
        map[position[0]][position[1]]=-1
        print("Enter the chaser1 position? Ex:a 1")
        position = convertStringPositionToCordination(input())
        map[position[0]][position[1]]=1        
        print("Enter the chaser2 position? Ex:a 1")
        position = convertStringPositionToCordination(input())
        map[position[0]][position[1]]=2
    print("Enter the number of turns :")
    turns=int(input())
    print("Enter the number of black cells on the board:")
    blackCellNumber=int(input())
    print("Are the cells going to be determined randomly or manually [r/m]:")
    cellCreateMethod=input()
    if(cellCreateMethod=="r"):
        randomBlocksOnMap(int(blackCellNumber))
    else:
        i = 1
        while i <= int(blackCellNumber):
            print("Enter the position of the "+str(i)+"th black cell:")
            if(allocateBlockOnMap(input())):
                i+=1
            else:
                print("Space allocated try again!")
    ## İs runner going to be controlled manuel or automatic? u-> user p-> programatic
    print("is the runner going to be controlled by the user or by a separate program [u/p]:")        
    runnerControllMethod=input()
    
    # Create path graph
    global G
    G = createGraph(createBoardList())
    i = 1
    while int(turns)>=i:   
        print("-------------TURN: "+str(i)+"------------------")

        playRunner(runnerControllMethod)
         
        # Note that chaser's has different learning rates based on chaser types
        # Therefore, they have different models
        playChaser(1)
        if(isGameOver()):
            printBoard()
            break
        playChaser(2)
        if(isGameOver()):
            printBoard()
            break
        global chaser1Score
        global chaser2Score
        print("Chaser 1 Score: "+ str(chaser1Score)+" || Chaser 2 Score: "+ str(chaser2Score))
        printBoard()
        #print(mapCordinateAdress) This shows the mapped path 
        print("-------------------------------")
        if(winner!=0):
            print("Chaser"+str(winner)+" won the game!")
            break
        i+=1
        ## Manuel sleep for 2 seconds to see controll flow on console
        time.sleep(2)
    if(winner==0):
        if(chaser1Score==chaser1Score):
            print("There is no winner in the Game!")
        else:
            if(chaser1Score>chaser2Score):
                print("Chaser1 won the game!")
            else:
             print("Chaser2 won the game!")

mainMenu()
