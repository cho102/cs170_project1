correct =[[1,2,3],[4,5,6],[7,8,0]];
#Input Functions
def buildPuzzle():
    puzzle = [[],[],[]];
    print("Build your own 8-tile puzzle!\nEnter value(0-8) for:")
    for i in range(3):
        for j in range(3):
            val = int(input("Row " + str(i+1) + ", Column " +str(j+1) + ": "));
            puzzle[i].append(val)
    problem =[];
    problem.append(puzzle)
    problem.append(0);
    problem.append(0);
    return problem;

def chooseSearch():
    print("Pick a search algorithm: ")
    check = 1;
    while check:
        print("(1) Uniform Cost Search\n(2)A* with Misplaced Tile Heuristic\n(3)A* with Manhattan Distance Heuristic")
        val = int(input("Input: "));
        if val in range (1,4):
            check=0;
        else:
            print("Please enter a valid integer from 1-3!")
    return val;


#Basic Search Functions/Operators
def checkGoal(node):
    if node[0] == correct: return 1;
    return 0;

def makeCopy(prob):
    new = [[[0,0,0],[0,0,0], [0,0,0]], 0, 0];
    for x in range(3):
        for y in range(3):
            new[0][x][y] = prob[0][x][y];
    new[1]=prob[1];
    return new;

def moveUp(prob, x, y, choice):
    if x==0:
        return -1;
    else: 
        # print("u")
        prob1 = makeCopy(prob);
        val=prob1[0][x-1][y];
        prob1[0][x][y] = val;
        prob1[0][x-1][y] = 0;
        prob1[1]+=1;
        if choice==3:
            prob1[2] += calManhattan(prob1);
        elif choice==2:
            prob1[2] += misplacedTiles(prob1);
        return prob1;

def moveDown(prob, x, y, choice):
    if x == 2:
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
        # print("l")
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
    if y==2:
        return -1;
    else:
        # print("r")
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

def orderPriorityQueue(og):
    for i in range(len(og)):
        for j in range(i+1, len(og)):
            if (og[i][1] + og[i][2]) < (og[j][1] + og[j][2]):
                og[i], og[j] = og[j], og[i]

def getChildren(prob_op, queue, visited, choice):
    prob_child = prob_op
    curr_x = 0;
    curr_y = 0;
    for x in range(3):
        for y in range(3):
            if (prob_child[0][x][y]==0):
                curr_x = x;
                curr_y = y;
                break;

    probUp = moveUp(prob_child, curr_x, curr_y, choice);
    if probUp!= -1 and visited.count(probUp)==0:
        queue.append(probUp);

    probDown = moveDown(prob_child, curr_x, curr_y, choice);
    if probDown != -1 and visited.count(probDown)==0: 
        queue.append(probDown);

    probLeft = moveLeft(prob_child, curr_x, curr_y, choice);
    if probLeft!= -1 and visited.count(probLeft)==0: 
        queue.append(probLeft);

    probRight = moveRight(prob_child, curr_x, curr_y, choice);
    if probRight!= -1 and visited.count(probRight)==0: 
        queue.append(probRight);
    orderPriorityQueue(queue);
    return 0;

#Misplaced Tiles Functions
def misplacedTiles(prob):
    incorrect_pos = 0;
    probNode = prob[0];
    for x in range(3):
        for y in range(3):
            if (probNode[x][y]!=correct[x][y]):
                incorrect_pos+=1;
    return(incorrect_pos);

#Manhattan Functions
def calManhattan(probMan):
    total_dist = 0;
    for m in range(3):
        for n in range(3):
            if correct[m][n] == probMan[0][m][n] or probMan[0][m][n]==0:
                continue;
            else:
                node = probMan[0][m][n];
                for j in range(3):
                    for k in range(3):
                        if node == correct[j][k]:
                            total_dist += abs(j-m);
                            total_dist += abs(k-n);
    return total_dist;

def performSearch(prob, choice):
    visited = [];
    queue = [];
    queue.append(prob);
    max_q_size = 0;
    while 1:
        if len(queue)==0: return "failed";
        if max_q_size < len(queue): max_q_size = len(queue)
        topNode = queue.pop();
        print("topNode");
        print(topNode)
        visited.append(topNode);
        
        if choice == 2: #For Misplaced
            topNode.append(len(visited));
            topNode.append(max_q_size);
            if misplacedTiles(topNode)==0: return topNode;
        else:
            #For Manhattan and Uniform
            topNode.append(len(visited));
            topNode.append(max_q_size);
            if checkGoal(topNode): return topNode;
        
        getChildren(topNode, queue, visited, choice);


# problem = buildPuzzle();
problem = [[[1,2,3],[4,0,6],[7,5,8]],0,0];
search = chooseSearch();

print("Starting Puzzle: ")
print(problem);
goal = performSearch(problem, search);
print("Ending Puzzle: ")
print(goal)
# print("Solution Depth: " + str(goal[1]));
# print("Max Queue Size: " + str(goal[4]));
# print("Total Nodes Visited: " + str(goal[3]))
