import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    width: 600
    height: 80
    property int ledNumber: 1
    property var commands: bridge ? bridge.getCommands(ledNumber-1).split("||") : []
    property var options: bridge ? bridge.getOptions(ledNumber-1).split("||") : []
    property int currentIndex: commandNumberSpinBox.value-1

    ColumnLayout {
        anchors.fill: parent
        RowLayout {
            Layout.fillWidth: true
            //anchors.fill: parent


            Label {
                id: ledNumberLabel
                text: ledNumber.toString() + "."
            }



            SpinBox {
                id: commandNumberSpinBox
                Layout.preferredWidth: 120
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

            ComboBox {
                id: pageCombobox
                Layout.preferredWidth: 80
                model: ["A", "B", "C", "D", "etc"]
                editable: true
            }




            Button {
                id: sendButton
                text: "Saada"
                onClicked: bridge.send(ledNumber-1, commandsWidget.displayText, optionsField.text, pageCombobox.currentText ) //bridge.send(ledNumber-1, currentIndex) // maybe we need also a setter to the´pyhon commands dict?

            }

            Button {
                id: clearButton
                text: "Tühjenda"
                onClicked: bridge.send(ledNumber-1, " ", "", pageCombobox.currentText)

            }

            Item {Layout.fillWidth: true}


        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 5

            Label {text: "Aktiivne leht: " }

            ComboBox {
                id: defaultPageCombobox
                Layout.preferredWidth: 80
                model: ["A", "B", "C", "D", "etc"]
                editable: true
            }

            Button {
                id: sendDefaultPageButton
                text: "Saada"
                onClicked: bridge.setDefaultPage(ledNumber-1, defaultPageCombobox.currentText)
            }

            Label {text: "Järgnevus:" }

            ComboBox {
                id: scheduleCombobox
                Layout.preferredWidth: 80
                model: ["A", "B", "C", "D", "E"]
            }

            Label {text: "Lehed (tühjistamiseks tühi) :" }

            TextField {
                id: schdulePagesField
                Layout.preferredWidth: 80
                text: ""
            }

            Button {
                text: "Saada"
                onClicked: bridge.setSchedule(ledNumber-1, scheduleCombobox.currentText, schdulePagesField.text )
            }


        }
    }


}
