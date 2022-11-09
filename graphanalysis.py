from collections import defaultdict
import GraphGeneration as gg
import FrequentTransactions as ft
import DisconnectedGraphs as dg
import pymongo

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)  
        self.V = vertices 
    def addEdge(self, u, v):
        self.graph[u].append(v)
    def topologicalSortUtil(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)
        stack.insert(0, v)
    def topologicalSort(self):
        print("Topological Sort")
        visited = [False] * self.V
        stack = []
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)
        print(stack)
        return stack

def initializeGraph(edgeList):

    g = Graph(len(edgeList))
    for edges in edgeList:
        g.addEdge(edges[0],edges[1])
    print(g.graph)
    return g

def mapTopologicalStack(g):
    print("Mapping Nodes")
    mapOfNodes = {}
    count = 0
    for k,v in g.graph.items():
        mapOfNodes[k] = count
        count += 1
    print(mapOfNodes)
    return mapOfNodes

def genEdgeWeights(g):
    print("Assigning Edge Weights  ")
    edgeWeights = []
    for k,v in  g.graph.items():
        if v != []:
            edgeWeight = {}
            for vertices in v:
                edgeWeight[vertices] = 1
            try:
                edgeWeights.append(edgeWeight)
            except:
                edgeWeights = [edgeWeight]
    print(edgeWeights)
    return edgeWeights

def longestDistance(nodeValues,mapOfNodes,g):
    longestPathEdges = {}
    edgeWeights = genEdgeWeights(g)
    print(edgeWeights)

    print("Longest Distance Function : ")
    for node in nodeValues.keys():
        try:
            print(node,edgeWeights[mapOfNodes[node]].keys())

            for key in edgeWeights[mapOfNodes[node]].keys():
                nodeVal = nodeValues[node] 
                edgeWt = edgeWeights[mapOfNodes[node]][key] 
                newNodeVal = nodeVal + edgeWt 
                if nodeValues[key] < newNodeVal:
                    nodeValues[key] = newNodeVal
                    try:
                        longestPathEdges[key].append(node,key)
                    except:
                        longestPathEdges[key] = [node,key]
        except:
            print("Exception!!!")
    print(nodeValues)
    print(longestPathEdges)
    return longestPathEdges

def getlongestPath(longestPathEdges,destNode,sourceNode):

    longestPath = [longestPathEdges[destNode]]
    prevNode = longestPathEdges[destNode][0]
    while prevNode != sourceNode:
        longestPath.append(longestPathEdges[prevNode])
        prevNode = longestPathEdges[prevNode][0]

    print(longestPath)
    return longestPath

def getTransactionInformation(longestPath):
    transactionList = []
    client = pymongo.MongoClient()
    db = client.MoneyLaundering
    mappedTransactions = db.mappedTransactions
    print("Transactions involved in longest Path : \n")
    for path in longestPath:
        transactionInfo  = {}
        orig = mappedTransactions.find({'tupleId' : path[0]}, {'customerId': 1,'_id': 0})
        dest = mappedTransactions.find({'tupleId' : path[1]}, {'customerId': 1,'_id': 0})

        transactionInfo["nameOrig"] = orig[0]['customerId']
        transactionInfo["nameDest"] = dest[0]['customerId']

        transactInfo = db.bankingTransactions.find({'nameOrig' : orig[0]['customerId'],'nameDest' : dest[0]['customerId']})

        for info in transactInfo:
            for k,v in info.items():
                transactionInfo[k] = v
        try:
            transactionList.append(transactionInfo)
        except:
            transactionList = [transactionInfo]
    return transactionList

def getCustomerId(node):
    client = pymongo.MongoClient()
    db = client.MoneyLaundering
    customer = db.mappedTransactions.find({'tupleId' : node},{'customerId':1,'_id':0})
    customerId = None
    for info in customer:
        for k,v in info.items():
            print(v)
            customerId = v
    return customerId

def main():

    print("Tuple List")
    tupleList = ft.mapCustomers()
    print("Total Number of Transactions : ", len(tupleList))

    print("Actual Frequency of Transactions : ")
    actualTransFreq = ft.actualCount(tupleList)

    print("Hash Based Bucket Count : ")
    bucketContainer = ft.hashBasedBucketCount(tupleList)

    print("Filtered transactions(On Basis of Bucket Count) : ")
    filteredBucketTuples = ft.filterOnBucketCount(tupleList, bucketContainer, 50)

    print("Filtered Transactions(On Basis of actual Frequency) : ")
    actualCount = ft.filterOnActualCount(filteredBucketTuples, actualTransFreq, 0)
    print(actualCount)

    edgeList = [(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(3,6),(4,5),(4,6),(5,6),(7,8),(8,9),(8,10),(9,10),(11,12),(11,13),(12,14),(13,14)]
    print("Edge List")
    print(edgeList)

    g = initializeGraph(edgeList)
    graph = gg.generateGraph(edgeList)
    vertices = gg.getVertices(edgeList)
    indegreeMap = gg.getIndegree(vertices,graph)
    outdegreeMap = gg.getOutDegree(vertices,graph)
    sourceNodes = dg.getSourceNodes(indegreeMap)
    newEdgeList = dg.splitEdgeList(edgeList,graph,sourceNodes)

    print("Vertex Set after splitting")
    vertexSet = []
    count = 0
    for edgeList in newEdgeList:
        try:
            vertexSet.append(dg.depthFirstSearch(edgeList,graph,sourceNodes[count]))
        except:
            vertexSet = [dg.depthFirstSearch(edgeList,graph,sourceNodes[count])]
        count += 1

    print("New Node Values after splitting")
    newNodeValues = []
    count = 0
    for vertices in vertexSet:
        try:
            newNodeValues.append(gg.genNodeValues(vertices,sourceNodes[count]))
        except:
            newNodeValues = [gg.genNodeValues(vertices,sourceNodes[count])]
        count += 1

    count = 0
    for edgeList in newEdgeList:
        print("Edge List")
        print(edgeList)
        getTransactionInformation(edgeList)
        g = initializeGraph(edgeList)
        g.topologicalSort()
        mapOfNodes = mapTopologicalStack(g)
        longestDistance(newNodeValues[count],mapOfNodes,g)
        count += 1

    print("Longest Path for dest = %d and source = %d" %(10,7))
    longestPath = getlongestPath({8: [7, 8], 9: [8, 9], 10: [9, 10]},10,7)
    getTransactionInformation(longestPath)

    print("Longest Path for dest = %d and source = %d" % (6, 1))
    longestPath  = getlongestPath({2: [1, 2], 3: [2, 3], 4: [3, 4], 5: [4, 5], 6: [5, 6]}, 6, 1)
    getTransactionInformation(longestPath)