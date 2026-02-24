import sys
import io
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import Image
import pytesseract

class Snipper(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0.3)
        
        # Crosshair cursor for snipping
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        
        # Get screen geometry to cover the whole screen
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.is_snipping = False

    def paintEvent(self, event):
        if self.is_snipping:
            qp = QtGui.QPainter(self)
            qp.setPen(QtGui.QPen(QtGui.QColor('red'), 2))
            qp.setBrush(QtGui.QColor(128, 128, 255, 128)) # Semi-transparent blue fill
            qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.is_snipping = True
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.is_snipping = False
        QtWidgets.QApplication.processEvents()
        
        # Calculate the rectangle coordinates
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        
        rect = QtCore.QRect(x1, y1, x2 - x1, y2 - y1)
        
        # Hide the overlay so it isn't in the screenshot
        self.hide()
        
        # Grab the specific region from the screen into memory
        screen = QtWidgets.QApplication.primaryScreen()
        pixmap = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
        
        self.process_image(pixmap)
        self.close()

    def process_image(self, pixmap):
        if pixmap.isNull():
            return
            
        # Convert QPixmap to PIL Image via memory buffer (no disk save)
        byte_array = QtCore.QByteArray()
        buffer = QtCore.QBuffer(byte_array)
        buffer.open(QtCore.QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        
        image = Image.open(io.BytesIO(byte_array.data()))
        
        # Run OCR
        try:
            extracted_text = pytesseract.image_to_string(image).strip()
        except Exception as e:
            extracted_text = f"OCR Error: {str(e)}\n\nIs tesseract-ocr installed?"

        self.show_result_dialog(extracted_text)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QtWidgets.QApplication.quit()

    def show_result_dialog(self, text):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("OCR Result")
        dialog.resize(500, 300)
        
        layout = QtWidgets.QVBoxLayout()
        
        # Text box so user can edit the OCR result if needed
        text_edit = QtWidgets.QTextEdit()
        text_edit.setPlainText(text)
        layout.addWidget(text_edit)
        
        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        
        copy_btn = QtWidgets.QPushButton("Copy to Clipboard")
        save_btn = QtWidgets.QPushButton("Save as .txt")
        cancel_btn = QtWidgets.QPushButton("Cancel")
        
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        
        # Button Actions
        def copy_text():
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(text_edit.toPlainText())
            dialog.accept()
            
        def save_text():
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                dialog, "Save Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_name:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(text_edit.toPlainText())
            dialog.accept()
            
        copy_btn.clicked.connect(copy_text)
        save_btn.clicked.connect(save_text)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec_()

        QtWidgets.QApplication.quit()        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    # Ensure application doesn't quit if the snipper closes before the dialog opens
    app.setQuitOnLastWindowClosed(False) 
    
    snipper = Snipper()
    snipper.show()
    
    sys.exit(app.exec_())

