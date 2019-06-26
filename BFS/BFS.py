from MyQueue import FIFO_Queue
import time

# Takes a node as [n1, n2, ..., nm] and a file to print to.
def PrintGameBoard(node, outputfile):
    gameSize = len(node)

    # This will loop through each position in the given node. If it encounters a position where
    # a queen is located, it prints a Q, or else it prints a ".".
    for row in range(0, gameSize):
        for column in range(0, gameSize):
            if node[row] == column:
                outputFile.write("Q ")
                # print('Q', end=" ")
            else:
                outputFile.write(". ")
                # print('.', end=" ")
        # print(" ")
        outputFile.write("\n")
    outputFile.write("\n")

# Takes a node as [n1, n2, ..., nm] and two of it's positions to check against each other.
def CheckPosition(node, checkPos, comparePos):
    # If the change in x or the change in y is equal to 0, this means that 
    # two queens lay on the same axis as each other.
    deltaX = checkPos - comparePos
    deltaY = node[checkPos] - node[comparePos]
    # The above can be expanded to include diagonal clashes; if the change in x
    # and the change in y are equal to each other (using absolute values to disallow negatives)
    # then that means both axes have changed by the same amount and therefore two queens lay on the same diagonal.
    return deltaX == 0 or deltaY == 0 or (abs(deltaX) == abs(deltaY))

# Takes a node as [n1, n2, ..., nm] as well as the size of the game that is being played (i.e., the amount of queens).
def IsGoalState(node, gameSize):
    # If the amount of queens that have been placed don't add up to the size of the board being played, 
    # then it cannot be a goal state.
    if len(node) < gameSize:
        return False

    # For each queen in the node, it will be checked against ALL the other queens in the node.
    # Except for itself. 
    for checkPos in range(0, len(node)):
        for comparePos in range(0, len(node)):
            if checkPos != comparePos:
                attack = CheckPosition(node, checkPos, comparePos)
                # If there is an attack between any of the queens, it is not a goal state and therefore we return false.
                if attack == True:
                    return False
    # If the function successfully reaches this point, then there have been no attacks. Therefore, it is a goal state.
    return True

# Takes a node, parentNode, as [n1, n2, ..., nm] and an action. 
# An action is a value from 0 to n.
def GenerateChildNode(parentNode, action):
    # Copy the contents of the parent node to the child.
    childNode = list(parentNode)[:]
    # We check to see if action is not already in the node as a form of pruning.
    # "Actions" work as columns in the board. As we don't want to put a queen on the same
    # column as another, we only put one down if that column isn't occupied.
    if action not in childNode:
        childNode.append(action)
    # Return the child as a tuple.
    return tuple(childNode)

# The main algorithm. Takes a gameSize, n.
def BreadthFirstSearch(gameSize):
    solutionsFound = 0
    childrenGenerated = 0
    solutionDictionary = {}
    # Starting node, no queens.
    node = ()
    # The frontier is all of the nodes that are generated, but yet to be explored.
    # First in first out format.
    frontier = FIFO_Queue()
    frontier.Push(node)
    # If we have checked a node before, just discarded it so we don't get stuck in a loop.
    exploredStates = []

    while True:
        # If the frontier is empty, we have nothing else to explore.
        if frontier.IsEmpty():
            return solutionsFound, solutionDictionary, childrenGenerated

        parentNode = frontier.Pop()
        exploredStates.append(parentNode)
        # print("current node is:", parentNode)
        
        # An action is a value from 0 to n.
        # As queens are placed on the board one row at a time, there will be no more "actions" to take place.
        # In other words, an action is placing a new queen on the board in a new row.
        for action in range(0, gameSize):
            childNode = GenerateChildNode(parentNode, action)
            childrenGenerated += 1
            # If it's a new child we've never seen before, check if it is a goal state.
            if (childNode not in exploredStates) and (frontier.Contains(childNode) == False):
                if IsGoalState(childNode, gameSize) == True:
                    # If it is a goal state, record it.
                    if gameSize <= 6:
                        solutionDictionary[solutionsFound] = childNode
                    solutionsFound += 1
                frontier.Push(childNode)
            
# This just loops through n = 1 -> n = 20 (or as far as it can go).
# It will record the information it found to a text file.
for i in range(1, 21):
    outputFile = open("output.txt", "a+")
    startTime = time.time()
    solutionsFound, solutionDictionary, childrenGenerated = BreadthFirstSearch(i)
    endTime = time.time()
    outputFile.write("In %f seconds there were %d solutions found for %d queens and %d children generated.\n" % ((endTime - startTime), solutionsFound, i, childrenGenerated))
    if i <= 6:
        for node in solutionDictionary.keys():
            PrintGameBoard(solutionDictionary[node], outputFile)
    outputFile.close()
