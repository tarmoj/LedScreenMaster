import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

ApplicationWindow {
    width: 640
    height: 480
    visible: true
    color: "lightcyan"
    title: qsTr("LED Screen Master")

    // does not work -  type unknown
//    Bridge {
//            id: bridge
//    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Label {
            Layout.preferredHeight: 20
            text: "LED Screen Master";
            font.pointSize: 14; font.bold: true
        }

        Column {
            Layout.fillWidth: true
            Layout.fillHeight: true

            //Rectangle {width: 20; height: 20; color: bridge.getColor("red") }

            Repeater {
                model: 6

                LedControl {
                    ledNumber: index+1
                }
            }
        }


        Button {
            text: "Test"
            onClicked: console.log( bridge.getCommands(0))
        }

        Item {Layout.fillHeight: true}


    }

}
