# This Python file uses the following encoding: utf-8

import sys, subprocess, json, re

from PySide2.QtGui import QGuiApplication
from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine
from time import sleep
#from PySide2.QtQuickControls2 import QQuickStyle


commandFiles = ["1.json", "2.json", "3.json", "4.json", "5.json", "6.json"]

# --port /dev/ttyUSB0 #mac: --port /dev/tty.usbserial-0001


commandPrefix = [
'sshpass -pRisset10 ssh -t tarmo@192.168.1.199 \'/home/tarmo/.local/bin/sixleds {command}\' ',
'sshpass -praspberry ssh -t pi@192.168.1.212 \'sixleds {command}\' ',
'sshpass -praspberry ssh -t pi@192.168.1.213 \'sixleds {command}\' ',
'sshpass -pKontrabass8 ssh -t pi@192.168.1.214 \'sixleds {command}\' ',
'sshpass -praspberry ssh -t pi@192.168.1.215 \'sixleds {command}\'',
'sshpass -praspberry ssh -t pi@192.168.1.216 \'sixleds {command}\''

#'sshpass -pRisset10 ssh -t tarmo@192.168.1.199 \'/home/tarmo/.local/bin/sixleds --port /dev/ttyUSB1 {command}\' ',
#'sixleds --port /dev/ttyUSB0 {command}' # central machine
]

# Change these for actual playlists:
schedulePlaylists = [
["AB", "CD"],
["EF", "GH"],
["IJ", "KL"],
["MN", "OP"],
["RS", "TU"],
["VW", "XY"]
]

#define commands by leds, each led has array of dictionaries (objects)
#definitions here for testing
commands = [
[
    {"text":"Käsk1-1", "options": "--leading-fx A --lagging-fx B" },
    {"text":"Käsk1-2", "options": "--display-fx b" },

],
[
    {"text":"Käsk2-1", "options": "" },
    {"text":"Käsk2-2", "options": "" },
],
[
{"text":"Käsk3-1", "options": "" },
{"text":"Käsk3-2", "options": "" },
],
[
{"text":"Käsk4-1", "options": "" },
{"text":"Käsk4-2", "options": "" },],
[
{"text":"Käsk5-1", "options": "" },
{"text":"Käsk5-2", "options": "" },
],

[
{"text":"Käsk6-1", "options": "" },
{"text":"Käsk6-2", "options": "" },
]

] # end commands


def updateCommands():
    for i in range(6):
        fileName = commandFiles[i]
        f = open(fileName)
        data = json.load(f)
        commands[i] = data

        # test:
#        for line in data:
#            print(line)



def split_long_string(text):
    words = re.split(r'\s(?=\w)', text)
    result = []
    current_substring = ""

    for word in words:
        if len(current_substring) + len(word) <= 26:
            if current_substring:
                current_substring += " "
            current_substring += word
        else:
            result.append(current_substring)
            current_substring = word

    if current_substring:
        result.append(current_substring)

    return result


class Bridge(QObject):

    commandsUpdated = Signal()
    consoleOutput = Signal(str)



    def execute_command(self, command, wait=False):
        print(command)
        if not wait:
            command += " &"
        result = subprocess.run(command, shell=True, capture_output=False, text=True) # this kind of works but no reasonable output
        print(result.returncode)
        #resultString="OK\n" if result.returncode==0 else "Error in: "+command+"\n"
        #self.consoleOutput.emit(resultString + result.stdout + result.stderr)
        #self.consoleOutput.emit(resultString)
        return result.returncode
#        try:
#            result = subprocess.run(command, check=True)
#            self.consoleOutput.emit(command + " OK\n");
#            return result.returncode #, result.stdout, result.stderr
#        except Exception as e:
#            print(e)
#            self.consoleOutput.emit("Error: " + str(e));
#            return -1

    @Slot(int, result="QVariant") # QVariant would be right way for getCommands and getOptions. Or rather pass it all as an object...
    def getPlaylist(self, ledIndex):
        return schedulePlaylists[ledIndex]

    @Slot()
    def reload(self):
        updateCommands()
        self.commandsUpdated.emit()
        self.consoleOutput.emit("Käsufailid loetud.")

    @Slot(int, result=str) # needs to return the commands as one string, separator: "||"
    def getCommands(self, ledIndex):
        commandString = ""
        for element in commands[ledIndex]:
            if ("text" in element.keys()):
                commandString += element["text"]+"||"
            else:
                commandString += " || "

        if commandString.endswith("||"):
            commandString = commandString[:-2]
        return commandString

    @Slot(int, result=str) # needs to return the commands as one string, separator: "||"
    def getOptions(self, ledIndex):
        optionsString = ""
        for element in commands[ledIndex]:
                if ("options" in element.keys()):
                    optionsString += element["options"]+"||"
                else:
                    optionsString += " || "

        if optionsString.endswith("||"):
            optionsString = optionsString[:-2]
        return optionsString



#märkmed. Pika käsu loogika:
# sea lehtede sisu ükshaaval
# sched ON: sixleds --set-schedule A --schedule-pages KL --start 0001010000 --end 9912302359
# sched OFF: sixleds --set-schedule A --schedule-pages "" && sixleds --set-default A

    @Slot(int, str)
    def setDefaultPage(self, ledIndex, defaultPage):
        commandLine = commandPrefix[ledIndex].format(command=" --set-default {}".format(defaultPage))
        # TODO: move execute_command to class, send signals from there
        self.execute_command(commandLine)

    @Slot(int, str, str)
    def setSchedule(self, ledIndex, schedule, pages ):
        if (len(pages)>0):
            options = F' --set-schedule {schedule} --schedule-pages {pages} --start 0001010000 --end 9912302359 '
        else:
            options = F' --set-schedule {schedule} --schedule-pages "" '


        commandLine = commandPrefix[ledIndex].format(command=options)
        self.execute_command(commandLine)
        # do we need to set a default page (empty?) after that?

    @Slot(int, str, str, str,result=int)
    def send(self, ledIndex, textToSend, optionsText="", page="A"):
        if len(textToSend) > 210:
            textToSend=textToSend[:210]
            print("Liiga pikk tekst! " + textToSend)
        options = ' {options} --set-page {page} --content "{text}"'.format(text=textToSend, options=optionsText, page=page)
        commandLine = commandPrefix[ledIndex].format(command=options)
        returnCode = self.execute_command(commandLine)
        #if (returnCode==0):
        #    self.setSchedule(ledIndex, "A", page)
        return returnCode

    @Slot(int,result=int)
    def deleteAll(self, ledIndex):
        options = ' --delete-all '
        commandLine = commandPrefix[ledIndex].format(command=options)
        returnCode = self.execute_command(commandLine)
        #test: fill pages:
        #self.fillPages(ledIndex)

        return returnCode

    def fillPages(self, ledIndex):
        for page in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
            self.send(ledIndex, "Leht "+page, "", page)

    @Slot(int)
    def loadPage(self, ledIndex):
        for line in commands[ledIndex]:
            if ("options" in line.keys()):
                options = line["options"]
            else:
                options = ""
            commandContent = ' {options} --set-page {page} --content "{text}"'.format(options=options, text=line["text"], page=line["page"])
            commandLine = commandPrefix[ledIndex].format(command=commandContent)
            self.execute_command(commandLine, wait=True)
            sleep(0.25)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    updateCommands()

    engine = QQmlApplicationEngine()

    # Expose the Python object to QML - this works abd @QmlElement not (maybe something missin in installation)
    context = engine.rootContext()
    bridge = Bridge()
    context.setContextProperty("bridge", bridge)

    qml_file = "main.qml" # Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
