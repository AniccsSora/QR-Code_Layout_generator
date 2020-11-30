from PyQt5 import QtWidgets
from QR_layout_window import QRLayoutGeneratorWindow
import traceback

if __name__ == '__main__':

    try:
        app = QtWidgets.QApplication([])
        window = QRLayoutGeneratorWindow()
        app.exec_()

    except KeyboardInterrupt as err:
        print("============ End ============")
    except:
        print(traceback.print_exc())
