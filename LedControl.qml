import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

Item {
    width: 600
    height: 50
    property int ledNumber: 1
    property var commands: bridge ? bridge.getCommands(ledNumber-1).split("||") : []
    property var options: bridge ? bridge.getOptions(ledNumber-1).split("||") : []
    property int currentIndex: commandNumberSpinBox.value-1

    RowLayout {
        anchors.fill: parent


        Label {
            id: ledNumberLabel
            text: ledNumber.toString() + "."
        }


        SpinBox {
            id: commandNumberSpinBox
            Layout.preferredWidth: 60
            from: 1
            to: commands.length
            value: 1
            editable: true

            onValueChanged: currentIndex = value-1
        }

        TextField {
            id: commandsWidget

            Layout.preferredWidth: 200

            text: commands[currentIndex] || ""

        }

        TextField {
            id: optionsField

            Layout.preferredWidth: 200

            text: options[currentIndex] || ""
        }




        Button {
            id: sendButton
            text: "Saada"
            onClicked: bridge.send(ledNumber-1, commandsWidget.displayText, optionsField.text) //bridge.send(ledNumber-1, currentIndex) // maybe we need also a setter to the´pyhon commands dict?

        }

        Button {
            id: clearButton
            text: "Tühjenda"
            onClicked: bridge.send(ledNumber-1, " ", "")

        }

        Item {Layout.fillWidth: true}


    }


}
