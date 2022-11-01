correct =[[1,2,3],[4,5,6],[7,8,0]];

def makeCopy(prob):
    new = [[[0,0,0],[0,0,0], [0,0,0]], 0, 0];
    for x in range(3):
        for y in range(3):
            new[0][x][y] = prob[0][x][y];
    new[1]=prob[1];
    new[2]= 0;
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
        prob1[2] += calManhattan(prob1);
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
        prob1[2] += calManhattan(prob1);
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
        prob1[2] +=calManhattan(prob1);
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
        prob1[2] +=calManhattan(prob1);
        return prob1;

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

def orderPriorityQueue(og):
    for i in range(len(og)):
        for j in range(i+1, len(og)):
            if (og[i][1] + og[i][2]) < (og[j][1] + og[j][2]):
                og[i], og[j] = og[j], og[i]           

def checkGoal(node):
    if node[0] == correct: return 1;
    return 0;

def getChildren(prob_og, queue, visited):
    #locate the location of 0
    prob_child = prob_og
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
    
    orderPriorityQueue(queue);

def a_star_manhattan(man_prob):
    queue =[];
    visited = [];
    queue.append(man_prob);
    while 1:
        if len(queue)==0: 
            return "failed"
        topNode = queue.pop();
        if checkGoal(topNode): return topNode
        visited.append(topNode);

        getChildren(topNode, queue, visited);
        
    
    return 0;



problem = [[[1,6,7],[5,0,3],[4,8,2]],0, 0];
print("start: ");
print(problem);
goal = a_star_manhattan(problem);
print("\nend: ");
print(goal);