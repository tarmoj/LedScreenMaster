# This Python file uses the following encoding: utf-8

import sys, subprocess, json, re

from PySide2.QtGui import QGuiApplication
from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine
#from PySide2.QtQuickControls2 import QQuickStyle


commandFiles = ["1.json", "2.json", "3.json", "4.json", "5.json", "6.json"]

# --port /dev/ttyUSB0 #mac: --port /dev/tty.usbserial-0001
execute = [
'sixleds  {options}  --set-page {page} --content  "{text}"',
'sshpass -praspberry ssh -t pi@192.168.1.211 \'/home/pi/src/sixleds-0.5.0/sixleds/sixleds %options%  --set-page A --content  "%text%" \' ',
'sshpass -praspberry ssh -t pi@192.168.1.212 \'/home/pi/src/sixleds-0.5.0/sixleds/sixleds %options% --set-page A --content  "%text%" \' ',
'sshpass -praspberry ssh -t pi@192.168.1.213 \'/home/pi/src/sixleds-0.5.0/sixleds/sixleds %options% --set-page A --content  "%text%" \' ',
'sshpass -pKontrabass8 ssh -t pi@192.168.1.214 \'sixleds %options% --set-page A --content  "%text%" \' ',
'sshpass -pKontrabass8 ssh -t pi@192.168.1.215 \'sixleds %options% --set-page A --content  "%text%" \' ',
]

commandPrefix = [
'sixleds --port /dev/tty.usbserial-0001',
'sshpass -praspberry ssh -t pi@192.168.1.211',
'sshpass -praspberry ssh -t pi@192.168.1.212',
'sshpass -praspberry ssh -t pi@192.168.1.213'
'sshpass -praspberry ssh -t pi@192.168.1.214'
'sshpass -praspberry ssh -t pi@192.168.1.215'
'sshpass -praspberry ssh -t pi@192.168.1.216'

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

def execute_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

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

        if commandString.endswith("||"):
            commandString = commandString[:-2]
        return commandString

    @Slot(int, result=str) # needs to return the commands as one string, separator: "||"
    def getOptions(self, ledIndex):
        optionsString = ""
        for element in commands[ledIndex]:
                if ("options" in element.keys()):
                    optionsString += element["options"]+"||"

        if optionsString.endswith("||"):
            optionsString = optionsString[:-2]
        return optionsString



#märkmed. Pika käsu loogika:
# sea lehtede sisu ükshaaval
# sched ON: sixleds --set-schedule A --schedule-pages KL --start 0001010000 --end 9912302359
# sched OFF: sixleds --set-schedule A --schedule-pages "" && sixleds --set-default A

    @Slot(int, str)
    def setDefaultPage(self, ledIndex, defaultPage):
        commandLine = commandPrefix[ledIndex] + " --set-default {}".format(defaultPage)
        # TODO: move execute_command to class, send signals from there
        execute_command(commandLine)

    @Slot(int, str, str)
    def setSchedule(self, ledIndex, schedule, pages ):
        #TODO: later use 'sixleds {commandContent}'.format(commandContent=...)
        if (len(pages)>0):
            commandLine = commandPrefix[ledIndex] + F" --set-schedule {schedule} --schedule-pages {pages} --start 0001010000 --end 9912302359 "
        else:
            commandLine = commandPrefix[ledIndex] + F" --set-schedule {schedule} --schedule-pages '' "

        execute_command(commandLine)
        # do we need to set a default page (empty?) after that?

    @Slot(int, str, str, str,result=int)
    def send(self, ledIndex, textToSend, optionsText="", page="A", result=int):
        commandLine = ""
        if (len(textToSend)>=26):
            messageParts = split_long_string(textToSend)
            print(messageParts)
            firstPage = "K"
            commandLine = 'sixleds  {} '.format(optionsText)
            playList = ""
            for index in range(len(messageParts)):
                print(messageParts[index])
                page = chr(ord(firstPage) + index)
                playList += page
                # TODO -  test the command -  if it can set several pages in one sixleds command
                # set text of page to messagePart[index]
                #temporary test!
                commandLine += ' --set-page {page} --content {text} '.format(page=page, text=messageParts[index])
            #set preset, run the preset
            # how to deal that it runs only once?
            print(commandLine)
            print(playList)
            commandLine += ' && --set-schedule A && sixleds --schedule-pages {} '.format(playList)
            print(commandLine)
            return -1
        commandLine = execute[ledIndex]
        commandLine = commandLine.format(text=textToSend, options=optionsText, page=page)
        #commandLine = commandLine.replace("%options%", optionsText)
        print(commandLine)
        return_code, stdout, stderr = execute_command(commandLine)
        #return_code = execute_command(commandLine)
        print(return_code)
        self.consoleOutput.emit(stdout + stderr)
        return return_code


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
