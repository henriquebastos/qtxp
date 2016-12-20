import sys
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QComboBox, QCompleter


class AccountCompleter(QCompleter):
    def splitPath(self, path):
        return path.split(':')

    def pathFromIndex(self, index):
        path = []
        while index.isValid():
            segment = self.model().data(index, Qt.DisplayRole)
            path.append(segment)
            index = index.parent()
        return ':'.join(reversed(path))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    accounts = open('accounts.txt').readlines()
    accounts.sort()

    w = QComboBox()
    w.setEditable(True)
    completer = AccountCompleter()

    #model = QStringListModel(accounts, completer)
    model = QStandardItemModel()


    completer.setModel(model)
    completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
    completer.setCaseSensitivity(Qt.CaseInsensitive)

    w.setCompleter(completer)
    w.show()

    sys.exit(app.exec_())
