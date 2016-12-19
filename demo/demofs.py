import sys
from PyQt5.QtWidgets import QApplication, QSplitter, QFileSystemModel, QTreeView, QListView
from PyQt5.QtCore import QDir


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splitter = QSplitter()

    model = QFileSystemModel()
    model.setRootPath(QDir.currentPath())

    tree = QTreeView(splitter)
    tree.setModel(model)
    tree.setRootIndex(model.index(QDir.currentPath()))

    list = QListView(splitter)
    list.setModel(model)
    list.setRootIndex(model.index(QDir.currentPath()))

    splitter.setWindowTitle("Two views onto the same file system model")
    splitter.show()

    app.exec()
