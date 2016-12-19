from PyQt5.QtWidgets import QLineEdit


class QLineEval(QLineEdit):
    """
    QLineEdit that evaluates Python expressions.
    """
    def __init__(self, parent=None):
        super(QLineEval, self).__init__(parent)

        self.returnPressed.connect(self.eval)

    def eval(self):
        """
        Evaluate self.text() passing the resulting value to self.setText()

        Shows error message on tooltip when it occurs.
        """
        expression = str(self.text())

        try:
            value = str(eval(expression))

            self.setText(value)
            self.setToolTip('')
        except Exception as e:
            error = ': '.join((type(e).__name__, str(e)))
            self.setToolTip(error)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = QLineEval()
    w.show()
    sys.exit(app.exec_())
