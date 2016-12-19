import sys
from PyQt5.QtWidgets import QApplication, QListView
from PyQt5.QtCore import Qt, QStringListModel


if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = ['one', 'two', 'three', 'four', 'five']
    model = QStringListModel(data)

    view = QListView()
    view.setModel(model)

    view.show()
    app.exec()

    print(data)
