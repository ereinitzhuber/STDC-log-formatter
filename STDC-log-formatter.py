from pathlib import Path
import re
import json

def getFileList(path, ext):
    fileList = {}
    for path in Path(path).rglob('*.' + ext):
        fileList[path] = path.name
    return fileList

def getDate(key):
    x = re.search("\B[0-9]{7}", str(key))
    date = str(key)[x.span()[0]-1:x.span()[1]]
    return date

def parseFileName(name):
    fileNameValues = {}
    split = name.split("_")
    fileNameValues["msgNum"] = split[0]
    fileNameValues["channelName"] = str(f"{split[1]} {split[2]} {split[3]}")
    fileNameValues["msgType"] = str(f"{split[4]} {split[5][0:-4]}")
    return fileNameValues

path = input("Enter file path...\n")
files = getFileList(path, "log")

messages = []

for key in files.keys():
    date = getDate(key)
    parsedFileName = parseFileName(files[key])
    univID = date + "-" + parsedFileName["msgNum"]
    message = {'ID': univID, 'date': date}
    for ky, val in parsedFileName.items():
        message[ky] = val
    msgstr = ''
    fileObject = open(key, "r")
    for line in fileObject:
        msgstr += line
    fileObject.close()
    message["message"] = msgstr
    messages.append(message)

handler = open(path + "\\STDC.json", "w")
handler.write(json.dumps(messages, sort_keys=True, indent=4))
handler.close()

handler = open(path + "\\STDC.txt", "w")
for msg in messages:
    strMsg = ''
    for value in msg.values():
        strMsg += value+"\n\n"
    handler.write(strMsg)
    handler.write('\n#########################################################################################################################\n\n')
handler.close()


print("Done!")