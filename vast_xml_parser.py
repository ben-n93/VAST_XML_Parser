import xml.etree.ElementTree as ET

import requests
from PyQt5 import QtWidgets

media_file_dictionary =  {}

class MainWindow(QtWidgets.QWidget):
    """ Main window of VAST XML Parser."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VAST XML Parser')
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.setMinimumWidth(995)
        self.setMinimumHeight(400)
        self.input_field = QtWidgets.QPlainTextEdit()
        self.input_field.setMaximumSize(1000,80)
        self.process_button = QtWidgets.QPushButton('Process tag')
        self.table = QtWidgets.QTableWidget(0,0)
        self.header_one = QtWidgets.QTableWidgetItem('MediaFile:')
        self.table.setHorizontalHeaderItem(0, self.header_one)
        self.layout.addWidget(self.input_field,0,0)
        self.layout.addWidget(self.process_button,0,1)
        self.layout.addWidget(self.table,1,0,1,0)
        self.process_button.clicked.connect(self.table_population)

    def table_population(self):
        """ Populates main window table."""

        attribute_list = []

        URL = self.input_field.toPlainText()

        try:
            response = requests.get(URL)
            tree = ET.fromstring(response.content)
            for child in tree.iter('MediaFile'):
                media_file_dictionary[child.text] = child.attrib
        except requests.exceptions.RequestException:
            pass

        # Sets table row count based on number of MediaFiles.
        dict_count = len(media_file_dictionary.keys())
        self.table.setRowCount(dict_count)

        row_count = 0
        row_height = 0

        # Creates a list of attribute names
        for dictionary in media_file_dictionary.values():
            for attribute_value in dictionary.keys():
                attribute_list.append(attribute_value)

        # Creates unique list of attribute names and sets column headers
        # with these attribute names.
        oset = dict.fromkeys(attribute_list).keys()
        oset_count = len(oset)

        column_count = 1 + oset_count
        self.table.setColumnCount(column_count)
        self.table.setHorizontalHeaderItem(0, self.header_one)
        header_count = 1
        for item in oset:
            widget_item = QtWidgets.QTableWidgetItem(item)
            self.table.setHorizontalHeaderItem(header_count, widget_item)
            header_count += 1

        # Adds MediaFile tag values (e.g. media files) to column 0.
        for key in media_file_dictionary:
            self.key_item = QtWidgets.QTableWidgetItem(key)
            self.table.setItem(row_count,0,self.key_item)
            self.table.resizeRowsToContents()
            row_count += 1
        row_count = 0

        # Adds attribute values to table.
        for value in media_file_dictionary.values():
            column_count = 1
            for attribute_value in value.values():
                self.attribute_value_item = QtWidgets.QTableWidgetItem(attribute_value)
                self.table.setItem(row_count,column_count,self.attribute_value_item)
                column_count += 1
            row_count += 1
            column_count = 1

        # Sets row height of MediaFile column.
        for key in media_file_dictionary:
            self.table.setRowHeight(row_height,20)
            row_height += 1

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationDisplayName('VAST XML Parser')
    main_window = MainWindow()
    main_window.show()
    app.exec()