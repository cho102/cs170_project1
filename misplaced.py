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

def getChildren(prob_op, queue):
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
    if probUp!= -1: 
        legal_moves+=1;
        queue.append(probUp);

    probDown = moveDown(prob_cp, curr_x, curr_y);
    if probDown != -1: 
        legal_moves+=1;
        queue.append(probDown);

    probLeft = moveLeft(prob_cp, curr_x, curr_y);
    if probLeft!= -1: 
        legal_moves+=1;
        queue.append(probLeft);

    probRight = moveRight(prob_cp, curr_x, curr_y);
    if probRight!= -1: 
        legal_moves+=1;
        queue.append(probRight);
    append_priority(queue);
    return 0;



def a_star_misplaced(a_star_prob):
    #make a queue
    queue = [];
    queue.append(a_star_prob);
    checker = 1;
    depth_count=0;
    while checker:
        if len(queue)==0: 
            return "failed"
        #get top of node (front of queue)
        topNode = queue.pop();
        print("depth_count: " + str(depth_count));
        print(topNode);
        #check if it is goal state
        if misplacedTiles(topNode)==0: return topNode;
        getChildren(topNode, queue);
        depth_count+=1;
    return 0;


problem = [[1,2,3],[4,5,6],[0, 7, 8]];
goal = a_star_misplaced(problem);
print("\n\nend: ");
print(goal);
