class SaveManager:

    def __init__(self):
        pass

    def save(self, path, sigDict):
        file = open(path, 'w+')

        for key in sigDict.keys():
            writeMessage = str(key) + '::' + sigDict[key][0] + '::'
            for item in sigDict[key][2]:
                writeMessage += str(item) + '::'
            writeMessage = writeMessage[:len(writeMessage) - 2]
            file.write(writeMessage)

    def load(self, path):
        file = open(path, 'r')

        data = file.readlines()

        retData = list()
        for line in data:
            retData += [line.split("::")]

        return retData
