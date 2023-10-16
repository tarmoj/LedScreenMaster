import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    width: 1200
    height: 920
    visible: true
    color: "lightcyan"
    title: qsTr("LED Screen Master") + " " +version
    property string version: "0.2.6"

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
            console.log("New console output")
            consoleArea.append(text)
        }
    }


    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        Label {
            Layout.preferredHeight: 30
            text: "LED Screen Master " + version;
            font.pointSize: 14; font.bold: true
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 20

            Repeater {
                id: repeater
                model: 6

                LedControl {
                    ledNumber: index+1
                    Layout.preferredHeight: 100
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
