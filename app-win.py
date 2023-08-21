import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from fb_view import createFBWidget

app = QApplication(sys.argv)
window = QMainWindow()
view = createFBWidget(window);

window.setWindowTitle("Fartenbuch")
window.setCentralWidget(view)
window.show()

app.exec()