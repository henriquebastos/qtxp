import sys
from datetime import datetime
from decimal import Decimal
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from table_ui import Ui_Form


ACCOUNT = [
    (datetime(2016, 12, 8), '', 'Salário Dezembro 2016', Decimal('100')),
    (datetime(2016, 12, 8), '', 'Almoço', Decimal('-10')),
    (datetime(2016, 12, 8), '', 'Cervejada', Decimal('-50'))
]


class TableWidget(QWidget):
    def __init__(self, parent=None, account=None):
        super().__init__(parent)

        self._account = account

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.table.setRowCount(len(self._account))

        for row, data in enumerate(self._account):
            for col, value in enumerate(data):
                self.ui.table.setItem(row, col, QTableWidgetItem(str(value)))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    table = TableWidget(account=ACCOUNT)
    table.show()

    sys.exit(app.exec_())
