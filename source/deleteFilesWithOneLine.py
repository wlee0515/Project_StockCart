import os


def main():
    print("Process Start")

    for (wDirPath, wDirList, wFileList) in os.walk(os.getcwd()):
        for wFile in wFileList:
            wFilePath = os.path.join(wDirPath, wFile)
            print("Processing File <{0}>".format(wFilePath))
            wFileHandler = open(wFilePath, "r")
            wDeleteFile = False
            if "r" == wFileHandler.mode:
                wFileLines = wFileHandler.readlines()
                if 1 >= len(wFileLines):
                    wDeleteFile = True
            wFileHandler.close()
            if True == wDeleteFile:
                print("Deleting File <{0}>".format(wFilePath))
                os.remove(wFilePath)

    print("Process Complete")

if __name__ == "__main__":
    main()
