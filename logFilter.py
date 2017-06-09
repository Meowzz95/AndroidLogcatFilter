from typing import IO, List
import re

PREFIX = ["V", "D", "I", "W", "E", "A"]
APP_SIGNATURE = "RFID APP 123456789"

result = []  # type: List[str]
pid=None

blockCount=0


def findAppPid(f: IO):
    for line in f:
        if APP_SIGNATURE in line:
            # print(line)
            pid = str(re.search("\(\d+\)", line).group(0))
            print("APP PID found = %s" % pid)
            return pid



def processBlock(block: List[str]):
    global blockCount
    blockCount+=1
    if pid in block[0]:
        print("Block accepted")
        result.extend(block)
    else:
        print("Block rejected")

def isBlockStart(line:str):
    for p in PREFIX:
        if line.startswith(p+"/"):
            return True
    #print("not block start")
    #print(line)
    return False


with open("log.txt", encoding="utf8") as f:
    pid = findAppPid(f)
    f.seek(0)
    lineCount=0
    block=[] #type:List[str]
    for line in f:
        if isBlockStart(line):
            processBlock(block)
            block.clear()
        block.append(line)
        lineCount+=1

    with open("logProcessed.txt","w") as out:
        for line in result:
            out.write(line)

    print(result)
    print("Result line count=%d"%len(result))
    print("Source Linecount=%d"%lineCount)
    print("Source Blockcount=%d"%blockCount)


