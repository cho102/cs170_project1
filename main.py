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
#checks if the node is in goal state
def checkGoal(node):
    if node[0] == correct: return 1;
    return 0;

#makes a copy of the node(prob) so that changes won't affect the original node
def makeCopy(prob):
    new = [[[0,0,0],[0,0,0], [0,0,0]], 0, 0];
    for x in range(3):
        for y in range(3):
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
    for x in range(3):
        for y in range(3):
            if (prob_child[0][x][y]==0):
                curr_x = x;
                curr_y = y;
                break;

    #create the children nodes of the topNode
    probUp = moveUp(prob_child, curr_x, curr_y, choice);
    #check if node has already been visited or if node is an edge piece. If not, it will be appended to queue
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
    
    #order the queue
    orderPriorityQueue(queue);
    return 0;

#Misplaced Tiles Function: checks how many tiles are in the incorrect position
def misplacedTiles(prob):
    incorrect_pos = 0;
    probNode = prob[0];
    for x in range(3):
        for y in range(3):
            #compare the probNode value to the correctNode value
            if (probNode[x][y]!=correct[x][y]):
                incorrect_pos+=1;
    return(incorrect_pos);

#Manhattan Functions: checks the distance incorrect tiles are from the correct position (excluding 0)
def calManhattan(probMan):
    total_dist = 0;
    for m in range(3):
        for n in range(3):
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
        if len(queue)==0: return "failed";
        #see how big the queue got
        if max_q_size < len(queue): max_q_size = len(queue)
        #take top node which has highest priority/best f(n)
        topNode = queue.pop();
        print("\n\ng(n)=" + str(topNode[1]) + ", h(n)=" + str(topNode[2]))
        print('\n'.join(' '.join('%2d' % x for x in l) for l in topNode[0]));
        #prevent repeated states since it is out of queue
        visited.append(topNode);
        
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


def main():
    # problem = buildPuzzle();
    # problem = [[[1,3,6],[5,0,7],[4,8,2]],0,0];
    problem = [[[1,2,3],[4,5,6],[0,7,8]],0,0];
    search = chooseSearch();

    print("Starting Puzzle: ")
    print('\n'.join(' '.join('%2d' % x for x in l) for l in problem[0]));
    print("\n\nExpanded Nodes: ")
    goal = performSearch(problem, search);
    print("\n\nEnding Puzzle: ")
    print('\n'.join(' '.join('%2d' % x for x in l) for l in goal[0]));
    print("Solution Depth: " + str(goal[1]));
    print("Max Queue Size: " + str(goal[4]));
    print("Total Nodes Visited: " + str(goal[3]))

main();
