import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: ledControl
    width: 600
    height: 100
    property int ledNumber: 1
    property var commands: bridge ? bridge.getCommands(ledNumber-1).split("||") : []
    property var options: bridge ? bridge.getOptions(ledNumber-1).split("||") : []
    property int currentIndex: commandNumberSpinBox.value-1

    property var pages: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
    "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


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



            ScrollView {
                id: view
                Layout.preferredWidth: 400
                Layout.preferredHeight: 60
                Layout.alignment: Qt.AlignTop
                TextArea {
                    id: commandsWidget
                    wrapMode: TextEdit.WordWrap
                    text: commands[currentIndex] || ""
                    background: Rectangle { color: "white"; border.color: "darkgrey"; radius: 4  }

                }

            }





            TextField {
                id: optionsField

                Layout.preferredWidth: 200

                text: options[currentIndex] || ""
            }

            ComboBox {
                id: pageCombobox
                Layout.preferredWidth: 80
                model: pages
                editable: true
            }




            Button {
                id: sendButton
                text: "Saada"
                onClicked: bridge.send(ledNumber-1, commandsWidget.text, optionsField.text, pageCombobox.currentText ) //bridge.send(ledNumber-1, currentIndex) // maybe we need also a setter to the´pyhon commands dict?

            }

            Button {
                id: clearButton
                text: "Tühjenda"
                onClicked: bridge.send(ledNumber-1, " ", "", pageCombobox.currentText)

            }

            Button {
                id: resetButton
                text: "Factory reset"
                onClicked: bridge.deleteAll(ledNumber-1)

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
                model: pages
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

            Button {
                text: "Peata"
                onClicked: {
                    schdulePagesField.text = ""
                    bridge.setSchedule(ledNumber-1, scheduleCombobox.currentText, "" )
                }
            }

            Item {Layout.preferredWidth: 20}

            Button {
                text: "Lae lehed"
                onClicked: bridge.loadPage(ledNumber-1)
            }


        }
    }


}
