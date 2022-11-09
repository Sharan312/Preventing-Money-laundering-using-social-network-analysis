import pymongo
client = pymongo.MongoClient()
db = client.MoneyLaundering
def mapCustomers():
    try:
        customerMap = {}
        tupleList = []
        transactions = db.bankingTransactions 
        mappedTransactions = db.mappedTransactions
        rowInsert = []

        fromToTuple = transactions.find({},{'nameOrig':1,'nameDest':1,'_id':0})
        count = 0
        for transaction in fromToTuple:

            if transaction['nameOrig'] not in customerMap.keys():
                customerMap[transaction['nameOrig']] = count
                try:
                    rowInsert.append({"customerId": transaction['nameOrig'], "tupleId" : count})
                except:
                    rowInsert = [{"customerId": transaction['nameOrig'], "tupleId" : count}]
                count += 1

            if transaction['nameDest'] not in customerMap.keys():
                customerMap[transaction['nameDest']] = count
                try:
                    rowInsert.append({"customerId": transaction['nameDest'], "tupleId": count})
                except:
                    rowInsert = [{"customerId": transaction['nameDest'], "tupleId": count}]
                count += 1


            
            trans = (customerMap[transaction['nameOrig']],customerMap[transaction['nameDest']])
            try:
                mappedTransactions.insert(rowInsert)
                rowInsert = []
                tupleList.append(trans)
            except:
                tupleList = [trans]

        for keys in customerMap.keys():
            print(keys,customerMap[keys])
        print(tupleList)
        return tupleList
    except:
        print("Error in Mapping !!")
        print("Please check if MongoDb server is On")


class BucketContainer():
    def __init__(self):
        self.bucket = {}
        self.bucketCount = {}


def hashBasedBucketCount(tupleList):
    b = BucketContainer()
    for trans in tupleList:
        bucketIndex = ((trans[0]*10) + trans[1]) % 10
        try:
            if trans not in b.bucket:
                b.bucket[bucketIndex].append(trans)
        except:
            b.bucket[bucketIndex] = [trans]
    #print(b.bucket)
    for keys in b.bucket.keys():
        print("Keys:",keys,b.bucket[keys])
        b.bucketCount[keys] = len(b.bucket[keys])
    for keys in b.bucketCount.keys():
        print(keys,b.bucketCount[keys])
    return b

def actualCount(tupleList):
    actualCount = {}
    for tuple in tupleList:
        if tuple not in actualCount.keys():
            actualCount[tuple] = 1
        else:
            actualCount[tuple] += 1
    return actualCount

def filterOnActualCount(filteredBucketTuples,actualCount,minSupportCount):
    filteredActualCount = {}
    count = 0
    for keys in actualCount.keys():
        if actualCount[keys] > minSupportCount and keys in filteredBucketTuples.keys():
            filteredActualCount[keys] = actualCount[keys]
            count +=1
    print("Number of Transactions based on Actual Frequency : ",count)
    return filteredActualCount

def filterOnBucketCount(tupleList,bucketContainer,minSupportCount):
    itemSetCount = {}
    count = 0
    for tuple in tupleList:
        key = [k for k, v in bucketContainer.bucket.items() if tuple in v]
        if(bucketContainer.bucketCount[key[0]] > minSupportCount):
            itemSetCount[tuple] = bucketContainer.bucketCount[key[0]]
            count += 1
    print("Number of filtered Transactions : ",count)
    return itemSetCount

