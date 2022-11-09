
import drawGraph as dG


def depthFirstSearch(edgeList,graph,sourceNode):
    dfsStack = []
    exploredStack = [sourceNode]
    while exploredStack != []:
        visitedNode = exploredStack.pop()
        if visitedNode not in dfsStack:
            try:
                dfsStack.append(visitedNode)
            except:
                dfsStack = [visitedNode]
        if visitedNode in graph.keys():
                for val in graph[visitedNode]:
                    try:
                        exploredStack.append(val)
                    except:
                        exploredStack =[val]

    print("Vertices in Graph")
    dfsStack.sort()
    print(dfsStack)
    return dfsStack

def getSourceNodes(indegreeMap):
    print("Source Nodes")
    sourceNodes = []
    for k,v in indegreeMap.items():
        if v == 0:
            try:
                sourceNodes.append(k)
            except:
                sourceNodes = [k]
    print(sourceNodes)
    return sourceNodes

def getDestNodes(outdegreeMap):
    print("Destination Nodes")
    destNodes = []
    for k,v in outdegreeMap.items():
        if v == 0:
            try:
                destNodes.append(k)
            except:
                destNodes = [k]
    print(destNodes)
    return destNodes


def splitEdgeList(edgeList,graph,sourceNodes):
    newEdgeList = []
    for sourceNode in sourceNodes:
        vertexSet = depthFirstSearch(edgeList,graph,sourceNode)
        row = []
        for edge in edgeList:
            if edge[0] in vertexSet and edge[1] in vertexSet:
                try:
                    row.append(edge)
                except:
                    row = [edge]
        try:
            newEdgeList.append(row)
        except:
            newEdgeList =[row]
    print("New Edge Lists after splitting")
    i = 0
    for row in newEdgeList:
        print(row)
        dG.drawGraph(row,"Graph"+str(i)+".png")
        i += 1
    return newEdgeList


