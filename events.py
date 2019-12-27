import requests
from ics import Calendar, Event
from settings import Settings
from PyQt5 import QtCore, QtGui, QtWidgets
import arrow


class MaibleCalendar(object):
    def __init__(self, app_settings: Settings):
        self.settings = app_settings
        with open(app_settings.calendar_file, 'r') as f:
            self.calendar = Calendar(f.read())

    def import_from_url(self, url: str):
        events = self.calendar.events
        # noinspection PyBroadException
        try:
            data = requests.get(url).text
        except Exception:  # NOQA
            return
        if not data:
            return
        new_calendar = Calendar(data)
        for event in new_calendar.events:
            events.add(event)
        self.calendar.events = events
        self.save()

    def events_between(self, start, end):
        events = []
        for event in self.calendar.timeline.start_after(start):
            if event.begin > end:
                return events
            events.append(event)
        return events

    def count_between(self, start, end):
        return len(self.events_between(start, end))

    @classmethod
    def events_html(cls, events: list):
        events_content = ""
        if events:
            for event in events:
                start = event.begin.strftime("%H:%M")
                end = event.end.strftime("%H:%M")
                name = event.name
                location = event.location
                events_content += f"<p>{start}-{end} {name} @ {location}</p>"
            return events_content
        return "<p>No Events</p>"

    def add_event(self, event):
        events = self.calendar.events
        events.add(event)
        self.calendar.events = events
        self.save()

    def save(self):
        with open(self.settings.calendar_file, 'w') as f:
            f.write(str(self.calendar))


class EventsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, event_manager=None, app_settings=None, start=None, end=None):
        super().__init__(parent)
        self.main_parent = parent
        self.event_manager = event_manager
        self.app_settings = app_settings
        self.start = start
        self.end = end
        return self.setupUi(self)

    def setupUi(self, EventsDialog):
        EventsDialog.setObjectName("EventsDialog")
        EventsDialog.resize(771, 635)
        self.buttonBox = QtWidgets.QDialogButtonBox(EventsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(420, 590, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Close
        )
        self.buttonBox.setObjectName("buttonBox")
        self.eventTable = QtWidgets.QTableWidget(EventsDialog)
        self.eventTable.setGeometry(QtCore.QRect(10, 10, 751, 361))
        self.eventTable.setObjectName("eventTable")
        self.eventTable.setColumnCount(5)
        events = self.event_manager.events_between(self.start, self.end)
        self.eventTable.setRowCount(len(events))
        counter = 0
        item = QtWidgets.QTableWidgetItem()
        self.eventTable.setHorizontalHeaderItem(0, item)
        item.setText("event")
        item = QtWidgets.QTableWidgetItem()
        self.eventTable.setHorizontalHeaderItem(1, item)
        item.setText("start")
        item = QtWidgets.QTableWidgetItem()
        self.eventTable.setHorizontalHeaderItem(2, item)
        item.setText("end")
        item = QtWidgets.QTableWidgetItem()
        self.eventTable.setHorizontalHeaderItem(3, item)
        item.setText("location")
        item = QtWidgets.QTableWidgetItem()
        self.eventTable.setHorizontalHeaderItem(4, item)
        item.setText("duration")
        for event in events:
            item = QtWidgets.QTableWidgetItem()
            self.eventTable.setVerticalHeaderItem(counter, item)
            item.setText(f"{counter}")
            # name
            item = QtWidgets.QTableWidgetItem()
            self.eventTable.setItem(counter, 0, item)
            item.setText(event.name)
            # start
            item = QtWidgets.QTableWidgetItem()
            self.eventTable.setItem(counter, 1, item)
            item.setText(event.begin.strftime("%H:%M"))
            # end
            item = QtWidgets.QTableWidgetItem()
            self.eventTable.setItem(counter, 2, item)
            item.setText(event.end.strftime("%H:%M"))
            # location
            item = QtWidgets.QTableWidgetItem()
            self.eventTable.setItem(counter, 3, item)
            item.setText("A")
            # duration
            item = QtWidgets.QTableWidgetItem()
            self.eventTable.setItem(counter, 4, item)
            item.setText(str(event.duration))
            counter += 1
        self.newEventName = QtWidgets.QTextEdit(EventsDialog)
        self.newEventName.setGeometry(QtCore.QRect(20, 380, 741, 41))
        self.newEventName.setObjectName("newEventName")
        self.startDateLabel = QtWidgets.QLabel(EventsDialog)
        self.startDateLabel.setGeometry(QtCore.QRect(150, 430, 58, 18))
        self.startDateLabel.setObjectName("startDateLabel")
        self.endDateLabel = QtWidgets.QLabel(EventsDialog)
        self.endDateLabel.setGeometry(QtCore.QRect(560, 430, 58, 18))
        self.endDateLabel.setObjectName("endDateLabel")
        self.startDateTimeEdit = QtWidgets.QDateTimeEdit(EventsDialog)
        self.startDateTimeEdit.setGeometry(QtCore.QRect(20, 460, 341, 32))
        self.startDateTimeEdit.setObjectName("startDateTimeEdit")
        self.startDateTimeEdit.setCalendarPopup(True)
        self.startDateTimeEdit.setDateTime(self.start.datetime)
        self.endDateTimeEdit = QtWidgets.QDateTimeEdit(EventsDialog)
        self.endDateTimeEdit.setGeometry(QtCore.QRect(410, 460, 341, 32))
        self.endDateTimeEdit.setObjectName("endDateTimeEdit")
        self.endDateTimeEdit.setCalendarPopup(True)
        self.endDateTimeEdit.setDateTime(self.start.datetime)
        self.allDayCheckBox = QtWidgets.QCheckBox(EventsDialog)
        self.allDayCheckBox.setGeometry(QtCore.QRect(20, 500, 88, 22))
        self.allDayCheckBox.setObjectName("allDayCheckBox")
        self.locationName = QtWidgets.QTextEdit(EventsDialog)
        self.locationName.setGeometry(QtCore.QRect(20, 530, 741, 41))
        self.locationName.setObjectName("locationName")

        self.retranslateUi(EventsDialog)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(EventsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EventsDialog)

    def retranslateUi(self, EventsDialog):
        _translate = QtCore.QCoreApplication.translate
        EventsDialog.setWindowTitle(_translate("EventsDialog", "Events"))
        __sortingEnabled = self.eventTable.isSortingEnabled()
        self.eventTable.setSortingEnabled(True)
        self.eventTable.setSortingEnabled(__sortingEnabled)
        self.newEventName.setPlaceholderText(_translate("EventsDialog", "Add new event"))
        self.startDateLabel.setText(_translate("EventsDialog", "Start"))
        self.endDateLabel.setText(_translate("EventsDialog", "End"))
        self.allDayCheckBox.setText(_translate("EventsDialog", "All day"))
        self.locationName.setPlaceholderText(_translate("EventsDialog", "Location"))

    def accept(self):
        event_name = self.newEventName.toPlainText()
        is_all_day = self.allDayCheckBox.isChecked()
        location = self.locationName.toPlainText()
        start_time = self.startDateTimeEdit.dateTime().toPyDateTime()
        end_time = self.endDateTimeEdit.dateTime().toPyDateTime()
        if event_name:
            event = Event(
                name=event_name, begin=arrow.get(start_time), end=arrow.get(end_time),
                location=location
            )
            if is_all_day:
                event.make_all_day()
            self.event_manager.add_event(event)
        super().accept()