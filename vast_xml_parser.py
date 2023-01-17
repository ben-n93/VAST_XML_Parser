"""An application that extracts VAST tag MediaFiles metadata.

Extended Summary
----------------

This application parses a VAST tag (essentially a XML schema)
and extracts metadata.

While there is multiple elements in a VAST tag, this application only
extracts the MediaFiles elements' attributes and values and (if present)
the Creative elements' id and sequence values.

"""

import xml.etree.ElementTree as ET
import webbrowser

import requests
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QWidget):
    """Main window of VAST XML Parser."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("VAST XML Parser")
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.setMinimumWidth(995)
        self.setMinimumHeight(400)
        self.input_field = QtWidgets.QPlainTextEdit()
        self.input_field.setMaximumSize(1000, 80)
        self.process_button = QtWidgets.QPushButton("Process tag")
        self.open_tag_button = QtWidgets.QPushButton("Open tag in browser")
        self.table = QtWidgets.QTableWidget(0, 0)
        self.header_one = QtWidgets.QTableWidgetItem("MediaFile:")
        self.table.setHorizontalHeaderItem(0, self.header_one)
        # Data widgets
        self.creative_id_label = QtWidgets.QLabel("Creative ID:")
        self.creative_id_field = QtWidgets.QLineEdit()
        self.ad_id_label = QtWidgets.QLabel("AdID:")
        self.ad_id_field = QtWidgets.QLineEdit()
        self.sequence_label = QtWidgets.QLabel("Sequence:")
        self.sequence_field = QtWidgets.QLineEdit()
        self.highest_br_label = QtWidgets.QLabel("Highest bitrate:")
        self.highest_br_field = QtWidgets.QLineEdit()
        self.lowest_br_label = QtWidgets.QLabel("Lowest bitrate:")
        self.lowest_br_field = QtWidgets.QLineEdit()
        # Button group box.
        self.button_box = QtWidgets.QGroupBox()
        self.vboxlayout = QtWidgets.QHBoxLayout()
        self.button_box.setLayout(self.vboxlayout)
        # Button layout.
        self.vboxlayout.addWidget(self.process_button)
        self.vboxlayout.addWidget(self.open_tag_button)
        # Data group box.
        self.data_box = QtWidgets.QGroupBox()
        self.data_box_layout = QtWidgets.QGridLayout()
        self.data_box.setLayout(self.data_box_layout)
        # Data layout.
        self.data_box_layout.addWidget(self.creative_id_label, 1, 1)
        self.data_box_layout.addWidget(self.creative_id_field, 1, 2)
        self.data_box_layout.addWidget(self.ad_id_label, 1, 3)
        self.data_box_layout.addWidget(self.ad_id_field, 1, 4)
        self.data_box_layout.addWidget(self.sequence_label, 1, 5)
        self.data_box_layout.addWidget(self.sequence_field, 1, 6)
        self.data_box_layout.addWidget(self.highest_br_label, 2, 1)
        self.data_box_layout.addWidget(self.highest_br_field, 2, 2)
        self.data_box_layout.addWidget(self.lowest_br_label, 2, 3)
        self.data_box_layout.addWidget(self.lowest_br_field, 2, 4)
        # Table layout.
        self.layout.addWidget(self.input_field, 0, 0)
        self.layout.addWidget(self.button_box, 0, 1)
        self.layout.addWidget(self.data_box, 2, 0, 1, 0)
        self.layout.addWidget(self.table, 3, 0, 1, 0)
        # Signals/slots.
        self.process_button.clicked.connect(self.table_population)
        self.open_tag_button.clicked.connect(self.open_browser)

    def table_population(self):
        """Populate the main window table.
        
        Raises
        ------
        requests.exceptions.RequestException
            If no tag or an empty string is provided and the Process Tag
            button is pressed.

        xml.etree.ElementTree.ParseError
            If a non-XML URL is provided and the Process Tag button pressed.

        """

        media_file_dictionary = {}
        bit_rate_list = []
        attribute_list = []
        creative_ad_id = {}

        self.highest_br_field.clear()
        self.lowest_br_field.clear()
        self.creative_id_field.clear()
        self.ad_id_field.clear()
        self.sequence_field.clear()

        URL = self.input_field.toPlainText()

        try:
            response = requests.get(URL)
            tree = ET.fromstring(response.content)
            for child in tree.iter("MediaFile"):
                media_file_dictionary[child.text] = child.attrib
            for child in tree.iter("Creative"):
                creative_ad_id = child.attrib
        except requests.exceptions.RequestException:
            pass
        except xml.etree.ElementTree.ParseError:
            pass


        # Sets table row count based on number of MediaFiles.
        DICT_COUNT = len(media_file_dictionary)
        self.table.setRowCount(DICT_COUNT)

        row_count = 0
        row_height = 0

        # Creates a list of attribute names.
        for dictionary in media_file_dictionary.values():
            for attribute_value in dictionary:
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
            self.table.setItem(row_count, 0, self.key_item)
            self.table.resizeRowsToContents()
            row_count += 1
        row_count = 0

        # Adds attribute values to table.
        for value in media_file_dictionary.values():
            column_count = 1
            for attribute_value in value.values():
                self.attribute_value_item = QtWidgets.QTableWidgetItem(attribute_value)
                self.table.setItem(row_count, column_count, self.attribute_value_item)
                column_count += 1
            row_count += 1
            column_count = 1

        # Finds highest and lowest bitrate in tag.
        for value in media_file_dictionary.values():
            for key, item in value.items():
                if key == "bitrate":
                    bitrate_item = item
                    bitrate_item = int(bitrate_item)
                    bit_rate_list.append(bitrate_item)
                    highest_bit_rate = max(bit_rate_list)
                    lowest_bit_rate = min(bit_rate_list)
                    self.highest_br_field.setText(str(highest_bit_rate))
                    self.lowest_br_field.setText(str(lowest_bit_rate))

        # Inserts Creative and AdID into application.
        for key, item in creative_ad_id.items():
            if key == "id":
                self.creative_id_field.setText(str(item))
            if key == "AdID":
                self.ad_id_field.setText(str(item))
            if key == "sequence":
                self.sequence_field.setText(str(item))

        # Sets row height of MediaFile column.
        for key in media_file_dictionary:
            self.table.setRowHeight(row_height, 20)
            row_height += 1

    def open_browser(self):
        """Open VAST tag in default browswer."""
        URL = self.input_field.toPlainText()
        webbrowser.open(URL)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationDisplayName("VAST XML Parser")
    main_window = MainWindow()
    main_window.show()
    app.exec()
