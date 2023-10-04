import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

Item {
    width: 600
    height: 50
    property int ledNumber: 1
    property var commands: bridge.getCommands(ledNumber-1).split("||")
    property int currentIndex: commandsWidget.value

    RowLayout {
        anchors.fill: parent


        Label {
            id: ledNumberLabel
            text: ledNumber.toString() + "."
        }


        SpinBox {
            id: commandsWidget
            property var items: commands
            from: 0
            to: items.length - 1
            value: 0
            //editable: true

            Layout.preferredWidth: 200


            textFromValue: function(value) {
                return items[value];
            }

            valueFromText: function(text) {
                for (var i = 0; i < items.length; ++i) {
                    if (items[i].toLowerCase().indexOf(text.toLowerCase()) === 0)
                        return i
                }
                return sb.value
            }

            Label {
                anchors.left: parent.left
                anchors.leftMargin: 3
                anchors.verticalCenter: parent.verticalCenter
                id: counterNumber
                text: (parent.value+1).toString()
            }
        }




        Button {
            id: sendButton
            text: "Saada"
            onClicked: bridge.send(ledNumber-1, currentIndex)

        }

        Button {
            id: clearButton
            text: "Tühjenda"

        }

        Item {Layout.fillWidth: true}


    }


}
