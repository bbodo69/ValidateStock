import module.excel_collection as excel_collection

def loadConfig():
    df = excel_collection.readExcelToDataFrame('input/Master.xlsx', 'Config')
    dic = {}

    for idx, row in df.iterrows():
        dic[row['name']] = row['value']

    return dic