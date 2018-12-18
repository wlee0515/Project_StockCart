##########################################################
#   File Name : sortRawTickerDatabase.py
#   Author : W. L.
#   Purpose :
#       This code will sort the database received from https://www.alphavantage.co
#       into a database base on Market
#
##########################################################
import os
import shutil

cInputDatabaseFolder = "db_companylist_raw"
cOutputDatabaseFolder = "db_companylist"

# input csv header:
# symbol,name,type,region,marketOpen,marketClose,timezone,currency,matchScore

def main():
    print("Process Start")

    # Structure:
    #   Market : {
    #              EquityType: {
    #                            TickerSymbol : "CompanyName"
    #                          }
    #            }
    wMarketList = {}

    wInputFolder = os.path.join(os.getcwd(), cInputDatabaseFolder)

    if False == os.path.exists(wInputFolder):
        print( "Input Database <{0}> does not exist".format(wInputFolder))
    else:
        for (wDirPath, wDirList, wFileList) in os.walk(wInputFolder):
            for wFile in wFileList:
                wFilePath = os.path.join(wDirPath, wFile)
                print("Processing File <{0}>".format(wFilePath))
                wFileHandler = open(wFilePath, "r")
                wFileLines = []
                if "r" == wFileHandler.mode:
                    wFileLines = wFileHandler.readlines()
                wFileHandler.close()

                if 1 >= len(wFileLines):
                    print("File <{0}> has less than 2 line. Skipping File".format(wFilePath))
                    continue
                if "{" == wFileLines[0][0]:
                    print("File <{0}> Starts with \"\{\". File is not CSV. Skipping File".format(wFilePath))
                    continue

                for i in range(1, len(wFileLines)):
                    wFiltered = wFileLines[i].strip("\n")
                    wElements = wFiltered.split("\"")
                    wDataList = []
                    for k in range(0, len( wElements)):
                        if k % 2 == 0:
                            wTemp = wElements[k].split(",")
                            for j in range(0, len(wTemp)):
                                if (j == 0) | (j == len(wTemp) - 1):
                                    if "" == wTemp[j]:
                                        continue
                                wDataList.append(wTemp[j])
                        else:
                            wDataList.append(wElements[k])
                    if 4 > len(wDataList):
                        continue

                    if wDataList[3] not in wMarketList:
                        wMarketList[wDataList[3]] = {}
                    if wDataList[2] not in wMarketList[wDataList[3]]:
                        wMarketList[wDataList[3]][wDataList[2]] = {}
                    wMarketList[wDataList[3]][wDataList[2]][wDataList[0]] = wDataList[1]


    wOutputFolder = os.path.join(os.getcwd(), cOutputDatabaseFolder)

    if True == os.path.exists(wOutputFolder):
        shutil.rmtree(wOutputFolder)

    # check if temporary folder exits
    if False == os.path.exists(wOutputFolder):
        # if not exist, create
        os.makedirs(wOutputFolder)


    for wMarketKey, wMarketValue in wMarketList.items():
        if wMarketKey == "":
            continue
        wMarketFolder = os.path.join(cOutputDatabaseFolder, wMarketKey.replace(" ","_"))
        # check if temporary folder exits
        if False == os.path.exists(wMarketFolder):
            # if not exist, create
            os.makedirs(wMarketFolder)

        for wEquityType, wEquityValue in wMarketValue.items():
            wEquityFilePath = os.path.join(wMarketFolder, wEquityType.replace(" ", "_") + ".csv")
            print("Processing File <{0}>".format(wEquityFilePath))

            wFileHandler = open(wEquityFilePath, "w")
            wFileLines = []
            if "w" == wFileHandler.mode:
                # symbol, name, type, region,
                wDataLine = ""
                wDataLine += "{0}".format("region")
                wDataLine += ",{0}".format("type")
                wDataLine += ",{0}".format("symbol")
                wDataLine += ",{0}".format("name")
                wFileHandler.write("{0}\n".format(wDataLine))

                wKeyList = wEquityValue.keys()
                wKeyList = sorted(wKeyList)
                for wCompanyKey in wKeyList:
                    wDataLine = ""
                    wDataLine += "{0}".format(wMarketKey)
                    wDataLine += ",{0}".format(wEquityType)
                    wDataLine += ",{0}".format(wCompanyKey)
                    wDataLine += ",{0}".format("\"" + wEquityValue[wCompanyKey] + "\"")
                    wFileHandler.write("{0}\n".format(wDataLine))
            wFileHandler.close()

    print("Process Complete")


if __name__ == "__main__":
    main()
