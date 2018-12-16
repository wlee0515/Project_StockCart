import os
import requests
import time
from pathlib import Path


cUserKeyEnvVariable = "ALPHA_VANTAGE_KEY"
cDataBaseFolder = "db_companylist_raw"
cAlphabet = ["A", "B"] #, "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
#             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
#             "-"]


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
    for wLetter in cAlphabet:
        processSearchTerm(iUserKey, iPrefix + wLetter, iDirectory)
        print("Waiting {0} seconds".format(iWaitTime))
        time.sleep(iWaitTime)
    if 1 < iLetterCount:
        for wLetter in cAlphabet:
            searchAllAlphabet(iUserKey, iDirectory,  iPrefix + wLetter,  iLetterCount - 1, iWaitTime)
            time.sleep(iWaitTime)


def main():
    print("Process Start")
    wUserKey = os.environ[cUserKeyEnvVariable]
    wDirectory = os.path.join(os.getcwd(), cDataBaseFolder)

    # check if temporary folder exits
    if False == os.path.exists(wDirectory):
        # if not exist, create
        os.makedirs(wDirectory)

    searchAllAlphabet(wUserKey, wDirectory, "", 2, 2)
    print("Process Complete")

if __name__ == "__main__":
    main()
