import os
import requests
import time
from pathlib import Path


cUserKeyEnvVariable = "ALPHA_VANTAGE_KEY"
cDataBaseFolder = "db_companylist_raw"
cAlphabet = ["", "A", "B", "C",
             "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
             "-"]


def getSearch(iUserKey, iSearch):
    wUrl = "https://www.alphavantage.co/query?"
    wUrl += "function=SYMBOL_SEARCH"
    wUrl += "&apikey=" + iUserKey
    wUrl += "&keywords=" + iSearch
    wUrl += "&datatype=csv"
    wReturn = requests.request("GET", wUrl)
    return wReturn.content.decode('ascii').replace("\r\n","\n")


def saveStringToFile(iFileName, iString):
    wFileHandler = open(iFileName, "w")
    # if file is open for writing
    if "w" == wFileHandler.mode:
        # write json string to file
        wFileHandler.write(iString)
    # Close the file
    wFileHandler.close()
    print("File Name <{0}> is Saved".format(iFileName))


def processSearchTerm(iUserKey, iSearchTerm, iDirectory):
    wFileString = getSearch(iUserKey, iSearchTerm)
    saveStringToFile(os.path.join(iDirectory, iSearchTerm + ".csv"), wFileString)


def searchAllAlphabet(iUserKey, iDirectory,  iPrefix,  iLetterCount, iWaitTime):

    wIndice = []
    for i in range(0, iLetterCount):
        wIndice.append(0)

    print(wIndice)
    while 1:
        wIndice[0] += 1
        for i in range(0, len(wIndice) - 1):
            if wIndice[i] >= len(cAlphabet):
                wIndice[i] = 0
                if i+1 < len(wIndice):
                    wIndice[i+1] += 1

        wSearchTerm = ""
        for i in range(0, iLetterCount):
            wSearchTerm += cAlphabet[wIndice[i]]
            if "" == wSearchTerm:
                break

        if "" != wSearchTerm:
            processSearchTerm(iUserKey, iPrefix + wSearchTerm, iDirectory)
            print("Waiting {0} seconds".format(iWaitTime))
            time.sleep(iWaitTime)

        wCounterFull = True

        for i in range(0, len(wIndice)):
            if wIndice[i] != len(cAlphabet) - 1:
                wCounterFull = False
                break

        if True == wCounterFull:
            break


def main():
    print("Process Start")
    wUserKey = os.environ[cUserKeyEnvVariable]
    wDirectory = os.path.join(os.getcwd(), cDataBaseFolder)

    # check if temporary folder exits
    if False == os.path.exists(wDirectory):
        # if not exist, create
        os.makedirs(wDirectory)

    searchAllAlphabet_2(wUserKey, wDirectory, "", 4, 60)
    print("Process Complete")

if __name__ == "__main__":
    main()
