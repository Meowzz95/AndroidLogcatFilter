import os
from typing import IO, List
import re

PREFIX = ["V", "D", "I", "W", "E", "A"]
APP_SIGNATURE = "RFID APP 123456789"

result = []  # type: List[str]
pid=None

blockCount=0


def findAppPid(f: IO):
    pidList=[] #type:List[str]
    for line in f:
        if APP_SIGNATURE in line:
            # print(line)
            pid = str(re.search("\(.+\)", line).group(0))
            print("APP PID found = %s" % pid)
            pidList.append(pid)
    print("Found %d pids taking last one %s" % (len(pidList),pidList[len(pidList)-1]))
    return pidList[len(pidList)-1]


def processBlock(block: List[str]):
    global blockCount
    blockCount+=1
    if pid in block[0]:
        #print("Block accepted")
        result.extend(block)
    # else:
    #     print("Block rejected")

def isBlockStart(line:str):
    for p in PREFIX:
        if line.startswith(p+"/"):
            return True
    #print("not block start")
    #print(line)
    return False

def get_log_file()->str:
    fileList = os.listdir(".")
    for f in fileList:
        match=re.search("log.*\.txt",f)
        if match:
            print("Found log file %s"%match.group(0))
            return match.group(0)
def clear_processed_file():
    oldFileName="logProcessed.txt"
    if os.path.isfile(oldFileName):
        os.remove(oldFileName)
        print("old log file removed")
    else:
        print("old log file does not exist")


if __name__=="__main__":

    clear_processed_file()
    with open(get_log_file(), encoding="utf8") as f:
        pid = findAppPid(f)
        f.seek(0)
        lineCount = 0
        block = ["empty"]  # type:List[str]
        for line in f:
            if isBlockStart(line):
                processBlock(block)
                block.clear()
            block.append(line)
            lineCount += 1

        with open("logProcessed.txt", "w") as out:
            for line in result:
                out.write(line)

        print(result)
        print("Result line count=%d" % len(result))
        print("Source Linecount=%d" % lineCount)
        print("Source Blockcount=%d" % blockCount)





