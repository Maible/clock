# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import re
import sys


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, event_manager=None, app_settings=None):
        super().__init__(parent)
        self.main_parent = parent
        self.event_manager = event_manager
        self.app_settings = app_settings
        return self.setupUi(self)

    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(407, 435)
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(210, 390, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save
        )
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
        self.appQuitButton = QtWidgets.QPushButton(Settings)
        self.appQuitButton.setGeometry(QtCore.QRect(10, 390, 88, 34))
        self.appQuitButton.setObjectName("appQuitButton")

        # add clock theme options
        self.clockTheme.addItems(["weekdays", "analog"])
        self.backgroundColorSelect.addItems(["default", "white", "black"])
        self.helperBackgroundColor.addItems(["default", "white", "black"])
        self.hourColorSelect.addItems(["default", "white", "black", "red"])
        self.minuteColorSelect.addItems(["default", "white", "black", "red"])
        self.secondColorSelect.addItems(["default", "white", "black", "red"])

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        self.appQuitButton.clicked.connect(Settings.quit_app)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.clockTheme.setAccessibleName(_translate("Settings", "clock theme"))
        self.theme_text.setText(_translate("Settings", "Clock Theme"))
        self.url_text.setText(_translate("Settings", "ICS URL"))
        self.calendarUrl.setText(_translate("Settings", "https://"))
        self.background_text.setText(_translate("Settings", "Background"))
        self.hour_text.setText(_translate("Settings", "Hour Color"))
        self.minute_text.setText(_translate("Settings", "Minute Color"))
        self.second_text.setText(_translate("Settings", "Second Color"))
        self.shadow_text.setText(_translate("Settings", "Shadow Color"))
        self.helper_text.setText(_translate("Settings", "Helper Color"))
        self.helper_background_text.setText(_translate("Settings", "Helper Background"))
        self.appQuitButton.setText(_translate("Settings", "Quit App"))

    def closeEvent(self, event):
        self.main_parent.hide()
        self.main_parent.setWindowFrame(not self.main_parent.withFrame)
        self.main_parent.show()
        return event.accept()

    def quit_app(self, event):
        sys.exit(0)

    def accept(self):
        # check url
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        if re.match(regex, self.calendarUrl.text()) is not None:
            self.event_manager.import_from_url(self.calendarUrl.text())
        # clock theme
        self.app_settings.clock = self.clockTheme.currentText()
        # colors
        self.app_settings.background_color = self.convert_color(
            self.backgroundColorSelect.currentText(), base="background"
        )
        self.app_settings.helper_color = self.convert_color(
            self.helperBackgroundColor.currentText(), base="helper"
        )
        self.app_settings.hour_color = self.convert_color(
            self.hourColorSelect.currentText(), base="hour"
        )
        self.app_settings.minute_color = self.convert_color(
            self.minuteColorSelect.currentText(), base="minute"
        )
        self.app_settings.second_color = self.convert_color(
            self.secondColorSelect.currentText(), base="second"
        )
        # update main app
        self.main_parent.setup_main_settings(self.app_settings)
        # save settings
        self.app_settings.save()
        self.close()

    def reject(self):
        self.close()

    @staticmethod
    def convert_color(color_name, base):
        bases = {
            "background": [100, 100, 100, 220],
            "helper": [211, 211, 211, 75],
            "hour": [150, 114, 114, 220],
            "minute": [64, 64, 64, 200],
            "second": [96, 96, 105, 200]
        }
        colors = {
            "white": [255, 255, 255, 220],
            "black": [0, 0, 0, 220],
            "red": [255, 0, 0, 220]
        }
        if color_name in colors:
            return colors[color_name]
        # default
        return bases[base]
