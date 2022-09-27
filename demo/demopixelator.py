import sys

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import qGray
from PyQt5.QtWidgets import QAbstractItemDelegate
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QStyleOptionViewItem
from PyQt5.uic import loadUiType

Ui_MainWindow, _ = loadUiType('demopixelator.ui')


class ImageModel(QAbstractTableModel):
    def __init__(self, *args):
        self.modelImage = QImage()

        super().__init__(*args)

    def setImage(self, image):
        self.beginResetModel()
        self.modelImage = image
        self.endResetModel()

    def rowCount(self, parent=None, *args, **kwargs):
        return self.modelImage.height()

    def columnCount(self, parent=None, *args, **kwargs):
        return self.modelImage.width()

    def data(self, index, role=None):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        return qGray(self.modelImage.pixel(index.column(), index.row()))

    def headerData(self, section, orientation, role=None):
        return QSize(1, 1) if role == Qt.SizeHintRole else QVariant


class PixelDelegate(QAbstractItemDelegate):
    def __init__(self, parent: QModelIndex = None):
        self.pixelSize = 12
        super().__init__(parent)

    def paint(self, painter: QPainter, option, index: QModelIndex):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        r = option.rect
        x, y, w, h = r.x(), r.y(), r.width(), r.height()

        size = min(w, h)
        brightness = index.model().data(index, Qt.DisplayRole)
        radius = (size / 2.0) - (brightness / 255.0 * size / 2.0)
        if radius == 0.0:
            return

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)

        if option.state & QStyle.State_Selected:
            painter.setBrush(option.palette.highlightedText())
        else:
            painter.setBrush(option.palette.text())

        painter.drawEllipse(QRectF(x + w / 2 - radius, y + h / 2.0 - radius, 2 * radius, 2 * radius))

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        return QSize(self.pixelSize, self.pixelSize)

    def setPixelSize(self, size):
        self.pixelSize = size


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.setupUi(self)

        self.currentPath = QDir.currentPath()
        self.model = ImageModel(self)

        self.view.setModel(self.model)

        self.delegate = PixelDelegate(self)
        self.view.setItemDelegate(self.delegate)

    def open_image(self, filename):
        image = QImage()

        if not image.load(filename):
            return

        self.model.setImage(image)
        self.currentPath = filename
        self.setWindowTitle(f'{filename} - Pixelator')

        self.updateView()

    def choose_image(self):
        dialog = QFileDialog(self)
        filename, _ = dialog.getOpenFileName(self, 'Choose an image', self.currentPath, '*')

        if not filename:
            return

        self.open_image(filename)

    def print_image(self):
        pass

    def show_about(self):
        title = 'About the Pixelator example'
        text = ('This example demonstrates how a standard view and a custom\n'
                'delegate can be used to produce a specialized representation\n'
                'of data in a simple custom model.')

        QMessageBox().about(self, title, text)

    def change_pixel_size(self, size):
        self.delegate.setPixelSize(size)
        self.updateView()

    def updateView(self):
        self.view.resizeColumnsToContents()
        self.view.resizeRowsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontUseNativeMenuBar)

    window = MainWindow()
    window.show()
    app.exec()
