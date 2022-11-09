import pymongo
import openpyxl

def LoadData(excelSheet,sheetName,numberOfRecords):

    print("Loading Data")
    client = pymongo.MongoClient('localhost',27017)
    db = client.MoneyLaundering
    try:
        db.bankingTransactions.insert({
            "hour": 1,
            "type": "PAYMENT",
            "amount": 9839.64,
            "nameOrig": "C1231006815",
            "oldBalanceOrig": 170136.0,
            "newBalanceOrig": 160296.36,
            "nameDest": "M1979787155",
            "oldBalanceDest": 0.0,
            "newBalanceDest": 0.0,
            "isFraud": 0,
            "isFlaggedFraud": 0,})
        print("Insertion Successful")
    except:
        print("Insertion Unsuccessful!")


    wb = openpyxl.load_workbook(excelSheet)
    sheet = wb.get_sheet_by_name(sheetName)
    row = []
    row_list = []
    for i in range(2,numberOfRecords):
        row = []
        for j in range(1,11):
            row.append(sheet.cell(row=i, column=j).value)
        row_list.append(row)
    document = {
                "hour":0,
                "type":"",
                "amount":0.0,
                "nameOrig":"",
                "oldBalanceOrig":0.0,
                "newBalanceOrig":0.0,
                "nameDest": "",
                "oldBalanceDest":0.0,
                "newBalanceDest":0.0,
                "isFraud":0,
                "isFlaggedFraud":0
                }
    keys = []
    for key in document.keys():
        keys.append(key)
    bulkData = []
    for row in row_list:
        index = 0
        for col in row:
                document[keys[index]] = col
                index +=1
        bulkData.append(document.copy())
    db.bankingTransactions.insert_many(bulkData)
    print("All Data successfully Inserted")