import json

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QTextEdit, QTableWidget


class FolderItemQWidget(QWidget):
    def __init__(self, folder):
        super().__init__()

        label = QLabel(folder)
        button = QPushButton('btn')

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button, 1)

        self.setLayout(layout)

        #TODO: make folder icon
        #TODO: subfolders and files inside as an attribute

class FileItemQWidget(QWidget):
    def __init__(self, file):
        super().__init__()

        label = QLabel(file)

        layout = QHBoxLayout()
        layout.addWidget(label)

        self.setLayout(layout)

        #TODO: make some functions and icons for different file types
        #TODO: directory as an attribute (to open files deviant from the opened folder)

class TextEditorWidget(QWidget):
    resized = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.resized.connect(self.resize_widgets)

        self.lcm = 1  # line counter max
        self.lineCounter = QTextEdit(parent)
        self.lineCounter.setGeometry(QtCore.QRect(0, 0, 16, parent.height()))
        self.lineCounter.setReadOnly(True)
        self.lineCounter.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.textEdit = QTextEdit(parent)
        self.textEdit.setGeometry(QtCore.QRect(self.lineCounter.width() - 1, 0,
                                               parent.width() - self.lineCounter.width(), parent.height()))

        self.textEdit.textChanged.connect(self.count_lines)
        self.textEdit.textChanged.connect(self.handle_value_changed)
        self.textEdit.verticalScrollBar().valueChanged.connect(self.handle_value_changed)

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def resize_widgets(self):
        self.lineCounter.resize(9 * self.lcm + 4 if self.lcm != 1 else 16, super().height())
        self.textEdit.setGeometry(QtCore.QRect(self.lineCounter.width() - 1, 0,
                                               super().width() - self.lineCounter.width(), super().height()))

    def count_lines(self):
        cur_text = len(self.textEdit.toPlainText().split('\n'))
        self.lineCounter.setText('\n'.join(map(str, list(range(1, cur_text + 1)))))
        self.lcm = len(str(cur_text))
        self.resize_widgets()

    def handle_value_changed(self):
        self.lineCounter.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().value())

    def setText(self, text):
        self.textEdit.setText(text)

    def toPlainText(self):
        return self.textEdit.toPlainText()


class ImageEditorWidget(QWidget):
    pass


class ListFileWidget(QWidget):
    def __init__(self, parent, text):
        super().__init__(parent)

        self.parent = parent

        self.text = QLabel(parent)
        self.text.move(5, 8)
        self.text.setToolTip(text)

        if len(text) > 10:
            self.text.setText(f'{text[:4]}..{text[-7:]}')
        else:
            self.text.setText(text)

        self.btn = QPushButton(parent)
        self.btn.setText('X')
        self.btn.setGeometry(QtCore.QRect(75, 5, 20, 20))

        self.btn.pressed.connect(self.close)

    def close(self):  # removes itself from a parent tableWidget with a button press
        table = super().parent().parent().parent()

        column = table.indexAt(self.parent.pos()).column()
        table.removeColumn(column)

        with open('data.json', 'r') as f:
            data = json.load(f)
            data['opened_files'].pop(data['opened_files'].index(self.text.toolTip()))

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)


"""
    при нажатии на кнопку надо посылать сигнал олжительскому классу чтобы он там что-то сделал, а то так нет доступа к нескольким переменным
"""