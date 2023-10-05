import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

ApplicationWindow {
    width: 720
    height: 480
    visible: true
    color: "lightcyan"
    title: qsTr("LED Screen Master")

    Connections {
        target: bridge

        function onCommandsUpdated() {
            console.log("Commands.updated")
            for (let i=0; i<6;i++) {
               repeater.itemAt(i).commands =  bridge.getCommands(i).split("||")
               repeater.itemAt(i).options =  bridge.getOptions(i).split("||")
            }
        }

        function onConsoleOutput(text) {
            console.log("New console output", text)
            consoleArea.append(text)
        }
    }


    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        Label {
            Layout.preferredHeight: 20
            text: "LED Screen Master";
            font.pointSize: 14; font.bold: true
        }

        Column {
            Layout.fillWidth: true
            //Layout.fillHeight: true

            Repeater {
                id: repeater
                model: 6

                LedControl {
                    ledNumber: index+1
                }
            }
        }


        Button {
            text: "Uuenda"
            onClicked: bridge.reload()
        }

        ScrollView {
            Layout.margins: 10
            Layout.fillWidth: true
            Layout.fillHeight: true

            TextArea {
                id: consoleArea

                background: Rectangle {
                    color: "#F7F7F7"
                    border.color: "darkgrey"
                    radius: 3
                }

                placeholderText: "Commands output"


            }
        }


    }

}