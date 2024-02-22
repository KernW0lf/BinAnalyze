#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QScrollArea, QDesktopWidget, QLineEdit
from PyQt5.QtCore import Qt
import subprocess
import pyfiglet
import hexdump
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QTextCursor, QTextDocument

class FileDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BINALYZE")
        self.setWindowIcon(QIcon("icon.ico"))  
        layout = QVBoxLayout(self)

        # Banner
        banner_label = QLabel()
        font = QFont("Monospace")
        font.setPointSize(12)
        banner_label.setFont(font)
        banner_label.setAlignment(Qt.AlignCenter)
        banner_text = pyfiglet.figlet_format("BINALYZE", font="digital")
        banner_label.setText(banner_text)
        layout.addWidget(banner_label)

        author_label = QLabel()
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setText("by KernW0lf")
        layout.addWidget(author_label)

        upload_layout = QHBoxLayout()
        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.browse_file)
        upload_layout.addWidget(self.upload_button)
        upload_layout.addStretch(1) 
        layout.addLayout(upload_layout)

        self.label = QLabel("Drag and drop a binary file here or click 'Upload' to select.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.set_font()
        self.text_edit.setStyleSheet("background-color: white; color: black;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.text_edit)
        layout.addWidget(scroll_area)

        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search Hexdump")
        self.search_box.returnPressed.connect(self.search_hexdump)
        search_layout.addWidget(self.search_box)
        self.search_box.setVisible(False) 
        layout.addLayout(search_layout)

        buttons_layout = QHBoxLayout()

        self.header_button = QPushButton("Header")
        self.header_button.clicked.connect(self.display_header)
        self.header_button.setVisible(True)
        buttons_layout.addWidget(self.header_button)

        self.l_button = QPushButton("Program Headers")
        self.l_button.clicked.connect(self.display_l)
        self.l_button.setVisible(True)
        buttons_layout.addWidget(self.l_button)

        self.S_button = QPushButton("Section Headers")
        self.S_button.clicked.connect(self.display_S)
        self.S_button.setVisible(True)
        buttons_layout.addWidget(self.S_button)

        self.s_button = QPushButton("Symbol Table")
        self.s_button.clicked.connect(self.display_s)
        self.s_button.setVisible(True)
        buttons_layout.addWidget(self.s_button)

        self.hexdump_button = QPushButton("Colorful Hexdump")
        self.hexdump_button.clicked.connect(self.display_hexdump)
        self.hexdump_button.setVisible(True)
        buttons_layout.addWidget(self.hexdump_button)

        layout.addLayout(buttons_layout)

        self.setAcceptDrops(True)
        self.filepath = None
        self.hexdump_text = ""

    def set_font(self):
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("FiraCode-Retina.ttf")
        font_family = font_db.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 12)
        self.text_edit.setFont(font)

    def display_header(self):
        self.search_box.setVisible(False)
        if self.filepath:
            output = self.run_readelf_header(self.filepath)
            self.text_edit.setPlainText(output)

    def display_l(self):
        self.search_box.setVisible(False)
        if self.filepath:
            output = self.run_readelf_l(self.filepath)
            self.text_edit.setPlainText(output)

    def display_S(self):
        self.search_box.setVisible(False)
        if self.filepath:
            output = self.run_readelf_S(self.filepath)
            self.text_edit.setPlainText(output)

    def display_s(self):
        self.search_box.setVisible(False)
        if self.filepath:
            output = self.run_readelf_s(self.filepath)
            self.text_edit.setPlainText(output)

    def display_hexdump(self):
        if self.filepath:
            self.hexdump_text = self.colorful_hexdump(self.filepath)
            self.text_edit.setPlainText(self.hexdump_text)

    def run_readelf_header(self, filepath):
        try:
            output = subprocess.check_output(["readelf", "-h", filepath], universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            return f"Error running readelf: {e.output}"

    def run_readelf_l(self, filepath):
        try:
            output = subprocess.check_output(["readelf", "-l", filepath], universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            return f"Error running readelf: {e.output}"

    def run_readelf_S(self, filepath):
        try:
            output = subprocess.check_output(["readelf", "-S", filepath], universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            return f"Error running readelf: {e.output}"

    def run_readelf_s(self, filepath):
        try:
            output = subprocess.check_output(["readelf", "-s", filepath], universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            return f"Error running readelf: {e.output}"

    def colorful_hexdump(self, filepath):
        self.search_box.setVisible(True)
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                output = hexdump.hexdump(data, result='return')
                return output
        except FileNotFoundError:
            return "File not found"
        except PermissionError:
            return "Permission denied"
        except Exception as e:
            return f"Error: {e}"

    def search_hexdump(self):
        search_text = self.search_box.text()
        if search_text:
            cursor = self.text_edit.textCursor()
            cursor.setPosition(0)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.find(search_text, QTextDocument.FindWholeWords)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.filepath = url.toLocalFile()
            self.label.setText(f"Selected file: {self.filepath}")
            self.update_buttons_visibility()
            break

    def update_buttons_visibility(self):
        self.hexdump_button.setVisible(True)
        self.header_button.setVisible(True)
        self.l_button.setVisible(True)
        self.S_button.setVisible(True)
        self.s_button.setVisible(True)

    def browse_file(self):
        self.filepath, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Executable Files (*)")
        if self.filepath:
            self.label.setText(f"Selected file: {self.filepath}")
            self.update_buttons_visibility()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        self.center_window()
        super().showEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = FileDropWidget()
    widget.resize(1000, 900)
    widget.show()
    sys.exit(app.exec_())
