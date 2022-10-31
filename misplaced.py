correct =[[1,2,3],[4,5,6],[7,8,0]];

def makeCopy(prob):
    new = [[0,0,0],[0,0,0], [0,0,0]];
    for x in range(3):
        for y in range(3):
            new[x][y] = prob[x][y];
    return new;

def misplacedTiles(prob):
    incorrect_pos = 0;
    for x in range(3):
        for y in range(3):
            if (prob[x][y]!=correct[x][y]):
                incorrect_pos+=1;
    return(incorrect_pos);

def moveUp(prob, x, y):
    if x==0:
        return -1;
    else: 
        prob1 = makeCopy(prob);
        val=prob1[x-1][y];
        prob1[x][y] = val;
        prob1[x-1][y] = 0;
        return prob1;

def moveDown(prob, x, y):
    if x == 2:
        return -1;
    else:
        prob1 = makeCopy(prob);
        val=prob1[x+1][y];
        prob1[x][y] = val;
        prob1[x+1][y] = 0;
        return prob1;

def moveLeft(prob, x, y):
    if y==0:
        return -1;
    else:
        prob1 = makeCopy(prob);
        val=prob1[x][y-1];
        prob1[x][y] = val;
        prob1[x][y-1] = 0;
        return prob1;

def moveRight(prob, x, y):
    if y==2:
        return -1;
    else:
        prob1 = makeCopy(prob);
        val=prob1[x][y+1];
        prob1[x][y] = val;
        prob1[x][y+1] = 0;
        return prob1;

def append_priority(og):
    #append children by priority
    for i in range(len(og)):
        for j in range(i+1, len(og)):
            if misplacedTiles(og[i]) < misplacedTiles(og[j]):
                # print("og["+ str(i) +"] = " + str(misplacedTiles(og[i])) + " < og["+ str(i) +"] = " + str(misplacedTiles(og[i])));
                og[i], og[j] = og[j], og[i]

def getChildren(prob_op, queue, visited):
    prob_cp=prob_op;
    curr_x = 0;
    curr_y = 0;
    legal_moves = 0;
    for x in range(3):
        for y in range(3):
            if (prob_op[x][y]==0):
                curr_x = x;
                curr_y = y;
                break;

    probUp = moveUp(prob_cp, curr_x, curr_y);
    if probUp!= -1 and visited.count(probUp)==0: 
        legal_moves+=1;
        queue.append(probUp);

    probDown = moveDown(prob_cp, curr_x, curr_y);
    if probDown != -1 and visited.count(probDown)==0: 
        legal_moves+=1;
        queue.append(probDown);

    probLeft = moveLeft(prob_cp, curr_x, curr_y);
    if probLeft!= -1 and visited.count(probLeft)==0: 
        legal_moves+=1;
        queue.append(probLeft);

    probRight = moveRight(prob_cp, curr_x, curr_y);
    if probRight!= -1 and visited.count(probRight)==0: 
        legal_moves+=1;
        queue.append(probRight);
    append_priority(queue);
    return 0;



def a_star_misplaced(a_star_prob):
    #make a queue
    visited = [];
    queue = [];
    queue.append(a_star_prob);
    checker = 1;
    depth_count=0;
    while checker:
        if len(queue)==0: 
            return "failed"
        #get top of node (front of queue)
        topNode = queue.pop();
        visited.append(topNode);
        # print("depth_count: " + str(depth_count));
        # print(topNode);
        #check if it is goal state
        if misplacedTiles(topNode)==0: 
            # print("visited: ")
            # print(visited)
            return topNode;
        getChildren(topNode, queue, visited);
        depth_count+=1;
    return 0;


# probMan = [[1,2,3],[4,5,6],[0, 7, 8]];
probMan = [[1,3,6],[5,0,7],[4,8,2]];
goal = a_star_misplaced(probMan);
print("\n\nend: ");
print(goal);
