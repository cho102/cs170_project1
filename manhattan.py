correct =[[1,2,3],[4,5,6],[7,8,0]];

def makeCopy(prob):
    new = [[[0,0,0],[0,0,0], [0,0,0]], 0];
    for x in range(3):
        for y in range(3):
            new[0][x][y] = prob[0][x][y];
    new[1]=prob[1];
    return new;

def moveUp(prob, x, y):
    if x==0:
        return -1;
    else: 
        print("u")
        prob1 = makeCopy(prob);
        val=prob1[0][x-1][y];
        prob1[0][x][y] = val;
        prob1[0][x-1][y] = 0;
        prob1[1]+=1;
        prob1[1] +=calManhattan(prob1);
        return prob1;

def moveDown(prob, x, y):
    if x == 2:
        return -1;
    else:
        print("d")
        prob1 = makeCopy(prob);
        val=prob1[0][x+1][y];
        prob1[0][x][y] = val;
        prob1[0][x+1][y] = 0;
        prob1[1]+=1;
        prob1[1] += calManhattan(prob1);
        return prob1;

def moveLeft(prob, x, y):
    if y==0:
        return -1;
    else:
        print("l")
        prob1 = makeCopy(prob);
        val=prob1[0][x][y-1];
        prob1[0][x][y] = val;
        prob1[0][x][y-1] = 0;
        prob1[1]+=1;
        prob1[1] +=calManhattan(prob1);
        return prob1;

def moveRight(prob, x, y):
    if y==2:
        return -1;
    else:
        print("r")
        prob1 = makeCopy(prob);
        val=prob1[0][x][y+1];
        prob1[0][x][y] = val;
        prob1[0][x][y+1] = 0;
        prob1[1]+=1;
        prob1[1] +=calManhattan(prob1);
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

def getChildren(prob_og, visited):
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
    
    print(queue);


queue =[];
visited = [];
problem = [[[1,2,0],[4,5,3],[7,8,6]],0];
# print(problem[0])
# print(problem[1])
queue.append(problem);
visited.append(problem);
getChildren(problem, visited);