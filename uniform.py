correct =[[1,2,3],[4,5,6],[7,8,0]];

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

def moveUp(prob, x, y):
    if x==0:
        return -1;
    else: 
        # print("u")
        prob1 = makeCopy(prob);
        val=prob1[0][x-1][y];
        prob1[0][x][y] = val;
        prob1[0][x-1][y] = 0;
        prob1[1]+=1;
        return prob1;

def moveDown(prob, x, y):
    if x == 2:
        return -1;
    else:
        # print("d")
        prob1 = makeCopy(prob);
        val=prob1[0][x+1][y];
        prob1[0][x][y] = val;
        prob1[0][x+1][y] = 0;
        prob1[1]+=1;
        return prob1;

def moveLeft(prob, x, y):
    if y==0:
        return -1;
    else:
        # print("l")
        prob1 = makeCopy(prob);
        val=prob1[0][x][y-1];
        prob1[0][x][y] = val;
        prob1[0][x][y-1] = 0;
        prob1[1]+=1;
        return prob1;

def moveRight(prob, x, y):
    if y==2:
        return -1;
    else:
        # print("r")
        prob1 = makeCopy(prob);
        val=prob1[0][x][y+1];
        prob1[0][x][y] = val;
        prob1[0][x][y+1] = 0;
        prob1[1]+=1;
        return prob1;

def append_priority(og):
    #append children by priority
    for i in range(len(og)):
        for j in range(i+1, len(og)):
            if (og[i][1]) < (og[j][1]):
                og[i], og[j] = og[j], og[i]  

def getChildren(prob_op, queue, visited):
    prob_child = prob_op
    curr_x = 0;
    curr_y = 0;
    for x in range(3):
        for y in range(3):
            if (prob_child[0][x][y]==0):
                curr_x = x;
                curr_y = y;
                break;

    probUp = moveUp(prob_child, curr_x, curr_y);
    if probUp!= -1 and visited.count(probUp)==0:
        queue.append(probUp);

    probDown = moveDown(prob_child, curr_x, curr_y);
    if probDown != -1 and visited.count(probDown)==0: 
        queue.append(probDown);

    probLeft = moveLeft(prob_child, curr_x, curr_y);
    if probLeft!= -1 and visited.count(probLeft)==0: 
        queue.append(probLeft);

    probRight = moveRight(prob_child, curr_x, curr_y);
    if probRight!= -1 and visited.count(probRight)==0: 
        queue.append(probRight);
    append_priority(queue);
    return 0;

def uniform(uniform_prob):
    visited = [];
    queue = [];
    queue.append(uniform_prob);
    while 1:
        if len(queue)==0: return "failed"
        topNode = queue.pop();
        visited.append(topNode);
        if checkGoal(topNode): return topNode
        getChildren(topNode, queue, visited);
    return 0;



problem = [[[1,2,3],[4,5,6],[0,7,8]],0,0];
problem = [[[1,2,3],[5,0,6],[4,7,8]],0,0];
problem = [[[1,3,6],[5,0,2],[4,7,8]],0,0];
print("start: ");
print(problem);
goal = uniform(problem);
print("\nend: ");
print(goal);
