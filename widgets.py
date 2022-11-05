import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QTextEdit, QLineEdit
from PyQt5.QtGui import QPixmap, QFontMetrics, QFont


class FolderItemWidget(QWidget):
    def __init__(self, folder, is_sub=False):
        super().__init__()

        label = QLabel(self)

        if len(folder) > 15:
            label.setText(f'{folder[:13]}...')
        else:
            label.setText(folder)

        label.setToolTip(folder)

        size = label.fontMetrics().boundingRect(label.text()).height()
        pixmap = QPixmap(os.path.join('icons', 'folder.png')).scaled(size, size)

        icon = QLabel(self)
        icon.setPixmap(pixmap)

        layout = QHBoxLayout()

        if is_sub:
            layout.addWidget(QLabel('\\'))
            layout.addWidget(icon, 1)
            layout.addWidget(label, 10)
        else:
            layout.addWidget(icon)
            layout.addWidget(label, 1)

        self.setLayout(layout)


class FileItemWidget(QWidget):
    def __init__(self, file, is_sub=False):
        super().__init__()

        label = QLabel(self)

        if len(file) > 15:
            label.setText(f'{file[:13]}...')
        else:
            label.setText(file)

        label.setToolTip(file)

        size = label.fontMetrics().boundingRect(label.text()).height()
        pixmap = QPixmap(os.path.join('icons', 'file.png')).scaled(size, size)

        icon = QLabel(self)
        icon.setPixmap(pixmap)

        layout = QHBoxLayout()

        if is_sub:
            layout.addWidget(QLabel('\\'))
            layout.addWidget(icon, 1)
            layout.addWidget(label, 10)
        else:
            layout.addWidget(icon)
            layout.addWidget(label, 1)

        self.setLayout(layout)


class ListFileWidget(QWidget):
    def __init__(self, parent, text):
        super().__init__()

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

class TextEditorWidget(QWidget):
    resized = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.resized.connect(self.resize_widgets)

        self.font = QFont('Consolas', 9, QFont.Light)

        self.lcm = 1  # line counter max
        self.lineCounter = QTextEdit(parent)
        self.lineCounter.setGeometry(QtCore.QRect(0, 0, 16, parent.height()))
        self.lineCounter.setReadOnly(True)
        self.lineCounter.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lineCounter.setFont(self.font)

        self.textEdit = QTextEdit(parent)
        self.textEdit.setGeometry(QtCore.QRect(self.lineCounter.width() - 1, 0,
                                               parent.width() - self.lineCounter.width(), parent.height()))
        self.textEdit.setFont(self.font)

        self.textEdit.textChanged.connect(self.count_lines)
        self.textEdit.textChanged.connect(self.handle_value_changed)
        self.textEdit.verticalScrollBar().valueChanged.connect(self.handle_value_changed)

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def resize_widgets(self):
        size_of_one = QFontMetrics(self.font).width('9')
        self.lineCounter.resize(size_of_one * self.lcm + 10, super().height())
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


class ConsoleWidget(QWidget):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.resized.connect(self.resize_widgets)
        self.setWindowTitle('Console')

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def resize_widgets(self):
        self.text.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))

    def print(self, arg):
        self.text.insertPlainText(str(arg))
