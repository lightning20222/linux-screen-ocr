import sys
import io
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import Image
import pytesseract


class Snipper(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.3)

        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        # Cover all monitors
        screen = QtWidgets.QApplication.primaryScreen()
        self.setGeometry(screen.virtualGeometry())

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.is_snipping = False

    def paintEvent(self, event):

        if not self.is_snipping:
            return

        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor("red"), 2))
        painter.setBrush(QtGui.QColor(128, 128, 255, 128))

        rect = QtCore.QRect(self.begin, self.end).normalized()
        painter.drawRect(rect)

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.end = self.begin
            self.is_snipping = True
            self.update()

    def mouseMoveEvent(self, event):

        if self.is_snipping:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):

        if event.button() != QtCore.Qt.LeftButton:
            return

        self.is_snipping = False

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        rect = QtCore.QRect(x1, y1, x2 - x1, y2 - y1)

        # Ignore tiny selections
        if rect.width() < 5 or rect.height() < 5:
            self.close()
            return

        self.hide()
        QtWidgets.QApplication.processEvents()

        # Get correct monitor for capture
        screen = QtWidgets.QApplication.screenAt(rect.center())
        if screen is None:
            screen = QtWidgets.QApplication.primaryScreen()

        pixmap = screen.grabWindow(
            0,
            rect.x(),
            rect.y(),
            rect.width(),
            rect.height()
        )

        self.process_image(pixmap)

        self.close()

    def process_image(self, pixmap):

        if pixmap.isNull():
            return

        byte_array = QtCore.QByteArray()
        buffer = QtCore.QBuffer(byte_array)

        buffer.open(QtCore.QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        buffer.close()

        image = Image.open(io.BytesIO(byte_array.data()))

        # Improve OCR accuracy
        image = image.convert("L")

        try:
            text = pytesseract.image_to_string(
                image,
                lang="eng",
                config="--psm 6"
            ).strip()

        except Exception as e:
            text = f"OCR Error:\n{e}\n\nIs tesseract-ocr installed?"

        self.show_result_dialog(text)

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            QtWidgets.QApplication.quit()

    def show_result_dialog(self, text):

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("OCR Result")
        dialog.resize(500, 300)

        layout = QtWidgets.QVBoxLayout()

        text_edit = QtWidgets.QTextEdit()
        text_edit.setPlainText(text)

        layout.addWidget(text_edit)

        button_layout = QtWidgets.QHBoxLayout()

        copy_btn = QtWidgets.QPushButton("Copy to Clipboard")
        save_btn = QtWidgets.QPushButton("Save as .txt")
        cancel_btn = QtWidgets.QPushButton("Cancel")

        button_layout.addWidget(copy_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        def copy_text():

            QtWidgets.QApplication.clipboard().setText(
                text_edit.toPlainText()
            )
            dialog.accept()

        def save_text():

            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                dialog,
                "Save Text File",
                "",
                "Text Files (*.txt);;All Files (*)"
            )

            if file_name:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(text_edit.toPlainText())

            dialog.accept()

        copy_btn.clicked.connect(copy_text)
        save_btn.clicked.connect(save_text)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

        QtWidgets.QApplication.quit()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    snipper = Snipper()
    snipper.show()

    sys.exit(app.exec_())
