# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.main_parent = parent
        self.settings = settings
        self.setupUi(self)

    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(407, 435)
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(50, 390, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.clockTheme = QtWidgets.QComboBox(Settings)
        self.clockTheme.setGeometry(QtCore.QRect(140, 10, 241, 32))
        self.clockTheme.setObjectName("clockTheme")
        self.theme_text = QtWidgets.QLabel(Settings)
        self.theme_text.setGeometry(QtCore.QRect(10, 20, 91, 18))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.theme_text.setFont(font)
        self.theme_text.setObjectName("theme_text")
        self.url_text = QtWidgets.QLabel(Settings)
        self.url_text.setGeometry(QtCore.QRect(10, 60, 91, 18))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.url_text.setFont(font)
        self.url_text.setObjectName("url_text")
        self.calendarUrl = QtWidgets.QLineEdit(Settings)
        self.calendarUrl.setGeometry(QtCore.QRect(140, 50, 241, 32))
        self.calendarUrl.setInputMask("")
        self.calendarUrl.setObjectName("calendarUrl")
        self.background_text = QtWidgets.QLabel(Settings)
        self.background_text.setGeometry(QtCore.QRect(10, 100, 81, 18))
        self.background_text.setObjectName("background_text")
        self.hour_text = QtWidgets.QLabel(Settings)
        self.hour_text.setGeometry(QtCore.QRect(10, 140, 91, 18))
        self.hour_text.setObjectName("hour_text")
        self.minute_text = QtWidgets.QLabel(Settings)
        self.minute_text.setGeometry(QtCore.QRect(10, 180, 91, 18))
        self.minute_text.setObjectName("minute_text")
        self.second_text = QtWidgets.QLabel(Settings)
        self.second_text.setGeometry(QtCore.QRect(10, 220, 91, 18))
        self.second_text.setObjectName("second_text")
        self.shadow_text = QtWidgets.QLabel(Settings)
        self.shadow_text.setGeometry(QtCore.QRect(10, 260, 91, 18))
        self.shadow_text.setObjectName("shadow_text")
        self.helper_text = QtWidgets.QLabel(Settings)
        self.helper_text.setGeometry(QtCore.QRect(10, 300, 91, 18))
        self.helper_text.setObjectName("helper_text")
        self.helper_background_text = QtWidgets.QLabel(Settings)
        self.helper_background_text.setGeometry(QtCore.QRect(10, 340, 121, 18))
        self.helper_background_text.setObjectName("helper_background_text")
        self.helperBackgroundColor = QtWidgets.QComboBox(Settings)
        self.helperBackgroundColor.setGeometry(QtCore.QRect(140, 330, 241, 32))
        self.helperBackgroundColor.setObjectName("helperBackgroundColor")
        self.backgroundColorSelect = QtWidgets.QComboBox(Settings)
        self.backgroundColorSelect.setGeometry(QtCore.QRect(140, 90, 241, 32))
        self.backgroundColorSelect.setObjectName("backgroundColorSelect")
        self.hourColorSelect = QtWidgets.QComboBox(Settings)
        self.hourColorSelect.setGeometry(QtCore.QRect(140, 130, 241, 32))
        self.hourColorSelect.setObjectName("hourColorSelect")
        self.minuteColorSelect = QtWidgets.QComboBox(Settings)
        self.minuteColorSelect.setGeometry(QtCore.QRect(140, 170, 241, 32))
        self.minuteColorSelect.setObjectName("minuteColorSelect")
        self.secondColorSelect = QtWidgets.QComboBox(Settings)
        self.secondColorSelect.setGeometry(QtCore.QRect(140, 210, 241, 32))
        self.secondColorSelect.setObjectName("secondColorSelect")
        self.shadowColorSelect = QtWidgets.QComboBox(Settings)
        self.shadowColorSelect.setGeometry(QtCore.QRect(140, 250, 241, 32))
        self.shadowColorSelect.setObjectName("shadowColorSelect")
        self.helperColorSelect = QtWidgets.QComboBox(Settings)
        self.helperColorSelect.setGeometry(QtCore.QRect(140, 290, 241, 32))
        self.helperColorSelect.setObjectName("helperColorSelect")

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.clockTheme.setAccessibleName(_translate("Settings", "clock theme"))
        self.theme_text.setText(_translate("Settings", "Clock Theme"))
        self.url_text.setText(_translate("Settings", "Calendar URL"))
        self.calendarUrl.setText(_translate("Settings", "https://"))
        self.background_text.setText(_translate("Settings", "Background"))
        self.hour_text.setText(_translate("Settings", "Hour Color"))
        self.minute_text.setText(_translate("Settings", "Minute Color"))
        self.second_text.setText(_translate("Settings", "Second Color"))
        self.shadow_text.setText(_translate("Settings", "Shadow Color"))
        self.helper_text.setText(_translate("Settings", "Helper Color"))
        self.helper_background_text.setText(_translate("Settings", "Helper Background"))

    def closeEvent(self, event):
        self.main_parent.hide()
        self.main_parent.setWindowFrame(not self.main_parent.withFrame)
        self.main_parent.show()
        super().closeEvent(event)

    def accept(self):
        print("accept")
        self.close()

    def reject(self):
        self.destroy()