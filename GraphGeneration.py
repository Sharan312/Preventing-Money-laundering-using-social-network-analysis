def generateGraph(tupleList):

    print("Generate Graph")
    graph = {}
    for tuple in tupleList:
        if tuple[0] not in graph.keys():
            graph[tuple[0]] = [tuple[1]]
        else:
            graph[tuple[0]].append(tuple[1])
    print(graph)
    return graph

def getVertices(tupleList):
  
    print("Get Vertices of a Graph")
    vertices = []
    for tuple in tupleList:
        if tuple[0] not in vertices:
            try:
                vertices.append(tuple[0])
            except:
                vertices = [tuple[0]]
        if tuple[1] not in vertices:
                vertices.append(tuple[1])
    vertices.sort()
    print(vertices)
    return vertices

def getIndegree(vertices,graph):

    print("Get Indegree of all vertices")
    indegreeMap = {}
    for node in vertices:
        count = 0
        for keys in graph.keys():
            if node in graph[keys]:
                count += 1
        indegreeMap[node] = count
    print(indegreeMap)
    return indegreeMap

def getOutDegree(vertices,graph):

    print("Get OutDegree of all vertices")
    outDegreeMap = {}
    for node in vertices:
        if node in graph.keys():
            outDegreeMap[node] = len(graph[node])
        else:
            outDegreeMap[node] = 0
    print(outDegreeMap)
    return outDegreeMap


def genNodeValues(vertices,sourceNode):

    nodeValues = {}
    for vertex in vertices:
        if vertex == sourceNode:
            nodeValues[vertex] = 0
        else:
            nodeValues[vertex] = -1000
    print(nodeValues)
    return nodeValues
