import sys
import json
import os
import widgets

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QAbstractItemView
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QWidget, QLabel

CustomObjectRole = QtCore.Qt.UserRole + 1


class MyWidget(QMainWindow):
    resized = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.setMinimumWidth(self.listWidget.width())
        self.setMinimumHeight(self.tableWidget.height() * 3)

        self.textEditor = widgets.TextEditorWidget(self.widget)
        self.status_bar = self.statusBar()

        with open('data.json', 'r') as f:
            self.data = json.load(f)

        self.resized.connect(self.resize_widgets)

        self.actionNew_file.triggered.connect(self.new_file)
        self.actionOpen_file.triggered.connect(self.open_file)
        self.actionOpen_folder.triggered.connect(self.open_folder)
        self.actionSave_file.triggered.connect(self.save_file)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionDelete_file.triggered.connect(self.delete_file)

        self.listWidget.doubleClicked.connect(self.choose_item)
        self.lineEdit.returnPressed.connect(self.change_folder_name)
        self.tableWidget.cellClicked.connect(self.open_file_from_list)
        self.textEditor.textEdit.cursorPositionChanged.connect(self.update_status_bar)

        self.opened_file = ''
        self.opened_files = []

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(len(self.data['opened_files']))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.open_folder(self.data['cur_folder'])
        self.update_file_list()

    def resizeEvent(self, event):
        self.resized.emit()
        return super().resizeEvent(event)

    def resize_widgets(self):
        self.listWidget.resize(self.listWidget.width(), super().height() - self.lineEdit.height() - 43)
        self.tableWidget.resize(super().width() - self.lineEdit.width() - 1, self.tableWidget.height())
        self.widget.resize(super().width() - self.listWidget.width(), super().height() - self.tableWidget.height() - 43)
        self.textEditor.resize(super().width() - self.listWidget.width(), super().height() - self.tableWidget.height() - 43)

    def new_file(self):
        file_name, ok = QInputDialog.getText(self, 'New file', 'Enter file name:')

        if not ok:
            return

        if os.path.isfile(os.path.join(self.data['cur_folder'], file_name)):
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Oh no!')
            dlg.setText(f'File "{file_name}" already exists')
            dlg.exec()
        else:
            open(os.path.join(self.data['cur_folder'], file_name), 'a').close()
            self.open_folder(self.data['cur_folder'])

            for i in range(self.listWidget.count()):
                if file_name == self.listWidget.item(i).data(CustomObjectRole):
                    self.listWidget.setCurrentItem(self.listWidget.item(i))
                    self.textEditor.setText('')
                    break

    def open_file(self, file='', folder=''):
        if not file:
            file, ok = QFileDialog.getOpenFileName(self, 'Open file', self.data['cur_folder'])

            if not ok:
                return

        if not folder:
            folder = self.data['cur_folder']

        if os.path.isfile(os.path.join(folder, file)):
            with open('data.json', 'r') as f:
                self.data = json.load(f)

            with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
                self.textEditor.setText(f.read())
                self.opened_file = os.path.join(folder, file)

            if file in self.data['opened_files']:
                self.tableWidget.setCurrentCell(0, self.data['opened_files'].index(file))
            else:
                self.data['opened_files'].append(file)

                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4)

            self.update_status_bar(file)
            self.update_file_list()


    def open_folder(self, opened=''):
        if not opened:
            folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', self.data['cur_folder'], QFileDialog.ShowDirsOnly)
        else:
            folder = opened

        if not folder:
            return

        self.data['cur_folder'] = folder
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

        self.lineEdit.setText(self.data['cur_folder'].split('/')[-1])
        self.textEditor.setText('')
        self.listWidget.clear()

        # folders
        for fld in [i for i in os.listdir(folder) if os.path.isdir(os.path.join(folder, i))]:
            item = QListWidgetItem(self.listWidget)
            item_widget = widgets.FolderItemQWidget(fld)
            item.setSizeHint(item_widget.sizeHint())
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, item_widget)
            item.setData(CustomObjectRole, fld)

        # files
        for file in [i for i in os.listdir(folder) if os.path.isfile(os.path.join(folder, i))]:
            item = QListWidgetItem(self.listWidget)
            item_widget = widgets.FileItemQWidget(file)
            item.setSizeHint(item_widget.sizeHint())
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, item_widget)
            item.setData(CustomObjectRole, file)

    def save_file(self):
        if not os.path.isfile(self.opened_file):
            self.save_as()
            return

        with open(self.opened_file, 'w', encoding='utf-8') as f:
            f.write(self.textEditor.toPlainText())

    def save_as(self):
        name, ok = QFileDialog.getSaveFileName(self, 'Save file', self.data['cur_folder'])

        if not ok:
            return

        with open(name, 'w') as f:
            f.write(self.textEditor.toPlainText())

        self.open_folder(self.data['cur_folder'])

    def delete_file(self):
        file = self.listWidget.currentItem().data(CustomObjectRole)

        dlg = QMessageBox(self)
        dlg.setWindowTitle('Delete file')
        dlg.setText(f'Are you sure you want to delete {file}?')
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn = dlg.exec()

        if btn == QMessageBox.Yes:
            if os.path.isfile(os.path.join(self.data['cur_folder'], file)):
                os.remove(os.path.join(self.data['cur_folder'], file))

            self.open_folder(self.data['cur_folder'])
            self.textEditor.setText('')

    def choose_item(self):
        self.open_file(self.listWidget.currentItem().data(CustomObjectRole))


    def change_folder_name(self):
        if self.data['cur_folder'].split('/')[-1] == self.lineEdit.text():
            return
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle(self.data['cur_folder'].split('/')[-1] + ' => ' + self.lineEdit.text())
        dlg.setText('Are you sure you want to change current folder name?')
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn = dlg.exec()

        if btn == QMessageBox.Yes:
            destination = '/'.join(self.data['cur_folder'].split('/')[:-1] + [self.lineEdit.text()])
            os.rename(self.data['cur_folder'], destination)
            self.data['cur_folder'] = destination
            self.open_folder(self.data['cur_folder'])

    def update_file_list(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(len(self.data['opened_files']))
        self.opened_files.clear()

        for i, file in enumerate(self.data['opened_files']):
            widget = QWidget()
            obj = widgets.ListFileWidget(widget, file)

            self.opened_files.append(obj)
            self.opened_files[i].btn.clicked.connect(self.remove_file_from_list)

            self.tableWidget.setCellWidget(0, i, widget)

    def remove_file_from_list(self):
        col = self.tableWidget.indexAt(self.sender().parent().pos()).column()
        self.tableWidget.removeColumn(col)

        if os.path.basename(self.opened_file) == self.sender().parent().findChildren(QWidget)[0].toolTip():
            if self.tableWidget.columnCount():
                self.open_file(self.opened_files[0 if col != 0 else 1].text.toolTip())
            else:
                self.textEditor.setText('')
                self.update_status_bar('No file is currently opened', show_pos=False)
            
        del self.data['opened_files'][col]
        with open('data.json', 'w') as f:
            json.dump(self.data, f, indent=4)

        self.update_file_list()

    def open_file_from_list(self, row, col):
        self.open_file(self.data['opened_files'][col])

    def update_status_bar(self, text=None, show_pos=True):
        if text == None:
            text = self.status_bar.currentMessage().split(' ; ')[0]

        res = f'{text} ; Pos {self.textEditor.textEdit.textCursor().position()}' if show_pos else text
        self.status_bar.showMessage(res)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
