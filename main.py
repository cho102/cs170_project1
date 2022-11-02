import time;

#matrix of the correct board will be placed here to be compared #default 8-tile
correct =[[1,2,3],[4,5,6],[7,8,0]];
#the size of the board (ex:3x3,4x4,5x5) #default board is 3x3 for 8-tile puzzle
board = 3;
#Input Functions
def buildPuzzle():
    global board;
    global correct;
    correct = [];
    puzzle=[];
    wait = 1;
    while wait:
        print("How many tiles do you want in your puzzle? 8, 15, or 24?")
        tiles = int(input("Input: "))
        if tiles == 8 or tiles == 15 or tiles == 25:wait = 0;
        else: print("Please enter valid number of tiles!")
    if tiles == 15: board=4;
    elif tiles == 24: board=5;
    for i in range(board):
        puzzle.append([]);
        correct.append([]);

    print("Build your own 8-tile puzzle!\nEnter value(0-8) for:")
    num = 1;
    for i in range(board):
        for j in range(board):
            val = int(input("Row " + str(i+1) + ", Column " +str(j+1) + ": "));
            puzzle[i].append(val)
            correct[i].append(num)
            num+=1;
    correct[board-1][board-1] = 0;
    problem =[];
    problem.append(puzzle)
    problem.append(0);
    problem.append(0);
    return problem;

def choosePuzzle(num):
    problemList = [];
    problem = [[[1,2,3],[4,5,6],[7,8,0]],0,0];
    problemList.append(problem);
    problem = [[[1,2,3],[4,5,6],[0,7,8]],0,0];
    problemList.append(problem);
    problem = [[[1,2,3],[5,0,6],[4,7,8]],0,0];
    problemList.append(problem);
    problem = [[[1,3,6],[5,0,2],[4,7,8]],0,0];
    problemList.append(problem);
    problem = [[[1,3,6],[5,0,7],[4,8,2]],0,0];
    problemList.append(problem);
    problem = [[[1,6,7],[5,0,3],[4,8,2]],0,0];
    problemList.append(problem);
    problem = [[[7,1,2],[4,8,5],[6,3,0]],0,0];
    problemList.append(problem);
    problem = [[[0,7,2],[4,6,1],[3,5,8]],0,0];
    problemList.append(problem);
    return problemList[num-1];

def chooseSearch():
    print("Pick a search algorithm: ")
    check = 1;
    while check:
        print("(1) Uniform Cost Search (2)A* with Misplaced Tile Heuristic (3)A* with Manhattan Distance Heuristic")
        val = int(input("Input: "));
        if val in range (1,4):
            check=0;
        else:
            print("Please enter a valid integer from 1-3!")
    return val;


#Basic Search Functions/Operators
#checks if the node is in goal state
def checkGoal(node):
    if node[0] == correct: return 1;
    return 0;

#makes a copy of the node(prob) so that changes won't affect the original node
def makeCopy(prob):
    if board==3: new = [[[0,0,0],[0,0,0], [0,0,0]], 0, 0];
    elif board==4: new = [[[0,0,0,0],[0,0,0,0], [0,0,0,0], [0,0,0,0]], 0, 0];
    else: new = [[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], 0, 0];
    for x in range(board):
        for y in range(board):
            new[0][x][y] = prob[0][x][y];
    new[1]=prob[1];
    return new;

#move operators
def moveUp(prob, x, y, choice):
    #check edge values
    if x==0:
        #cannot be performed
        return -1;
    else: 
        #make copy so prob won't be altered
        prob1 = makeCopy(prob);
        #perform move operation
        val=prob1[0][x-1][y];
        prob1[0][x][y] = val;
        prob1[0][x-1][y] = 0;

        #g(n)+=1
        prob1[1]+=1;
        #calculate h(n) depending on search algorithm chosen
        if choice==3:
            prob1[2] += calManhattan(prob1);
        elif choice==2:
            prob1[2] += misplacedTiles(prob1);
        return prob1;

def moveDown(prob, x, y, choice):
    if x == board-1:
        return -1;
    else:
        prob1 = makeCopy(prob);
        val=prob1[0][x+1][y];
        prob1[0][x][y] = val;
        prob1[0][x+1][y] = 0;
        prob1[1]+=1;
        if choice == 3:
            prob1[2] += calManhattan(prob1);
        elif choice==2:
            prob1[2] += misplacedTiles(prob1);
        return prob1;

def moveLeft(prob, x, y, choice):
    if y==0:
        return -1;
    else:
        prob1 = makeCopy(prob);
        val=prob1[0][x][y-1];
        prob1[0][x][y] = val;
        prob1[0][x][y-1] = 0;
        prob1[1]+=1;
        if choice == 3:
            prob1[2] += calManhattan(prob1);
        elif choice == 2:
            prob1[2] += misplacedTiles(prob1);
        return prob1;

def moveRight(prob, x, y, choice):
    if y==board-1:
        return -1;
    else:
        prob1 = makeCopy(prob);
        val=prob1[0][x][y+1];
        prob1[0][x][y] = val;
        prob1[0][x][y+1] = 0;
        prob1[1]+=1;
        if choice==3:
            prob1[2] += calManhattan(prob1);
        elif choice==2:
            prob1[2] += misplacedTiles(prob1);
        return prob1;

#orders the queue with highest priority at top
def orderPriorityQueue(og):
    for i in range(len(og)):
        for j in range(i+1, len(og)):
            #calculate g(n)+h(n) to get f(n) and reorder queue to priority queue
            if (og[i][1] + og[i][2]) < (og[j][1] + og[j][2]):
                og[i], og[j] = og[j], og[i]

#performs the move operations
def getChildren(prob_op, queue, visited, choice):
    prob_child = prob_op
    curr_x = 0;
    curr_y = 0;
    #find the position of 0 in the puzzle
    for x in range(board):
        for y in range(board):
            if (prob_child[0][x][y]==0):
                curr_x = x;
                curr_y = y;
                break;

    #create the children nodes of the topNode
    probUp = moveUp(prob_child, curr_x, curr_y, choice);
    #check if node has already been visited or if node is an edge piece. If not, it will be appended to queue
    if probUp!= -1 and visited.count(probUp[0])==0:
        queue.append(probUp);
    probDown = moveDown(prob_child, curr_x, curr_y, choice);
    if probDown != -1 and visited.count(probDown[0])==0: 
        queue.append(probDown);
    probLeft = moveLeft(prob_child, curr_x, curr_y, choice);
    if probLeft!= -1 and visited.count(probLeft[0])==0: 
        queue.append(probLeft);
    probRight = moveRight(prob_child, curr_x, curr_y, choice);
    if probRight!= -1 and visited.count(probRight[0])==0: 
        queue.append(probRight);
    
    #order the queue
    orderPriorityQueue(queue);
    return 0;

#Misplaced Tiles Function: checks how many tiles are in the incorrect position
def misplacedTiles(prob):
    incorrect_pos = 0;
    probNode = prob[0];
    for x in range(board):
        for y in range(board):
            # print("prob: " + str(probNode[x][y]))
            # print("c: " +str(correct[x][y]))
            #compare the probNode value to the correctNode value
            if (probNode[x][y]!=correct[x][y]):
                incorrect_pos+=1;
    return(incorrect_pos);

#Manhattan Functions: checks the distance incorrect tiles are from the correct position (excluding 0)
def calManhattan(probMan):
    total_dist = 0;
    for m in range(board):
        for n in range(board):
            #will not check manhattan distance if it is 0 or already in the right spot
            if correct[m][n] == probMan[0][m][n] or probMan[0][m][n]==0:
                continue;
            else:
                node = probMan[0][m][n];
                for j in range(3):
                    for k in range(3):
                        #find the position of the correct node
                        if node == correct[j][k]:
                            #calculate the y distance and add to total
                            total_dist += abs(j-m);
                            #calculate the x distance and add to total 
                            total_dist += abs(k-n);
    return total_dist;

#General Search Algorithm
def performSearch(prob, choice):
    #keeps track of nodes that have been visited to prevent loops
    visited = [];
    #queue to hold node and its children
    queue = [];
    queue.append(prob);
    max_q_size = 0;
    while 1:
        #no solutions found
        if len(queue)==0: return 0;
        #see how big the queue got
        if max_q_size < len(queue): max_q_size = len(queue)
        #take top node which has highest priority/best f(n)
        topNode = queue.pop();
        print("\ng(n)=" + str(topNode[1]) + ", h(n)=" + str(topNode[2]))
        print('\n'.join(' '.join('%2d' % x for x in l) for l in topNode[0]));
        #prevent repeated states since it is out of queue
        visited.append(topNode[0]);
        #checks if node is in goal state
        if choice == 2: #For Misplaced
            #so main() can print how many nodes have been visited and max queue size
            topNode.append(len(visited));
            topNode.append(max_q_size);
            #checks if there are any misplaced tiles, if not, it reached goal state
            if misplacedTiles(topNode)==0: return topNode;
        else:
            #For Manhattan and Uniform
            topNode.append(len(visited));
            topNode.append(max_q_size);
            #checks if node is in goal state and exit out of function
            if checkGoal(topNode): return topNode;
        
        #if not yet reached goal state, expand the node to get its children nodes
        getChildren(topNode, queue, visited, choice);

#main function of the program
def main():
    choice = 1;
    while choice:
        print("(1) Build your own n-tile puzzle? (2) Generate existing 8-tile puzzle (3) Exit");
        val = int(input("Input: "));
        if val in range (1,4):
            if val==3:
                choice=0;
                return;
            elif val==2:
                check = 1;
                while check:
                    print("Pick a number between 1-8")
                    val1 = int(input("Input: "));
                    if val1 in range (1,8):
                        problem = choosePuzzle(val1);
                        check=0;
                    else:
                        print("Please enter a valid integer from 1-3!")
            else:
                problem = buildPuzzle();
            search = chooseSearch();
            if (search==1): print("Uniform Cost Chosen")
            elif (search==2): print("A* with Misplaced Tiles Chosen")
            else : print("A* with Manhattan Distance Chosen")

            print("Starting Puzzle: ")
            print('\n'.join(' '.join('%2d' % x for x in l) for l in problem[0]));
            print("\nExpanded Nodes: ")
            start_time=time.time()
            goal = performSearch(problem, search);
            end_time = time.time() - start_time
            print("\nEnding Puzzle: ")
            if goal==0: print("Failed to find a Solution")
            else:
                print('\n'.join(' '.join('%2d' % x for x in l) for l in goal[0]));
                print("Solution Depth: " + str(goal[1]));
                print("Max Queue Size: " + str(goal[4]));
                print("Total Nodes Visited: " + str(goal[3]))
                print("Total time elapsed(in seconds): " + str(end_time)+ "\n\n")
        else:
            print("Please enter a valid integer from 1-3!")
    

main();