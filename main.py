# This Python file uses the following encoding: utf-8

from pathlib import Path
import sys, subprocess, json

from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle


commandFiles = ["1.json", "2.json", "3.json", "4.json", "5.json", "6.json"]

execute = [
'sixleds --port /dev/ttyUSB0 %options%  --set-page A --content  "%text%"',
'sshpass -praspberry ssh -t pi@192.168.1.211 \'sixleds %options%  --set-page A --content  "%text%" \' ',
'sshpass -praspberry ssh -t pi@192.168.1.212 \'sixleds %options% --set-page A --content  "%text%" \' ',
'sshpass -praspberry ssh -t pi@192.168.1.213 \'sixleds %options% --set-page A --content  "%text%" \' ',
'sshpass -pKontrabass8 ssh -t pi@192.168.1.214 \'sixleds %options% --set-page A --content  "%text%" \' ',
'sshpass -pKontrabass8 ssh -t pi@192.168.1.215 \'sixleds %options% --set-page A --content  "%text%" \' ',

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

#necessary to understand the decorations:
QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1


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
    #result = os.system(command)
    #return result
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


@QmlElement
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



    @Slot(int, int, result=int)
    def send(self, ledIndex, commandIndex, result=int):
        commandLine = execute[ledIndex]
        textToSend = commands[ledIndex][commandIndex]["text"]
        commandLine = commandLine.replace("%text%", textToSend)
        print(commandLine)
        return_code, stdout, stderr = execute_command(commandLine)
        #return_code = execute_command(commandLine)
        print(return_code, stdout, stderr)
        return return_code

    # overload
    @Slot(int, str, str, result=int)
    def send(self, ledIndex, textToSend, optionsText="", result=int):
        commandLine = execute[ledIndex]
        commandLine = commandLine.replace("%text%", textToSend)
        commandLine = commandLine.replace("%options%", optionsText)
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

    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())