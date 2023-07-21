from PyQt5 import QtWidgets
from ui import Ui_MainWindow  # импорт нашего сгенерированного файла
from threading import Thread
from time import sleep as wait
import sys
 
 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.device_name = None

        size = 20
        border = 2

        self.RX, self.TX = QtWidgets.QButtonGroup(self), QtWidgets.QButtonGroup(self)

        self.setStyleSheet('''
            #rb_rx::indicator, #rb_tx::indicator, #rb_conn::indicator {{
            
                border: {border}px solid #a35709; 
                height: {size}px;
                width: {size}px;
                border-radius: {radius}px;
                
                background: qradialgradient(
                    cx:.5, cy:.5, radius: {innerRatio},
                    fx:.5, fy:.5,
                    stop:0 {color}, 
                    stop:0.45 {color},
                    stop:0.5 transparent,
                    stop:1 transparent
                    );
            }}
            #rb_rx::indicator:checked, #rb_tx::indicator:checked, #rb_conn::indicator:checked {{
                background: qradialgradient(
                    cx:.5, cy:.5, radius: {innerRatio},
                    fx:.5, fy:.5,
                    stop:0 {checkColor}, 
                    stop:0.45 {checkColor},
                    stop:0.5 transparent,
                    stop:1 transparent
                    );
            }}
        '''.format(
            size=size - border * 2, 
            border=border, 
            radius=size // 2, 
            innerRatio=1 - (border * 2 + 1) / size, 
            color='#ff0000',
            checkColor='#bbff00',
        )) 

        self.RX.addButton(self.ui.rb_rx)
        self.TX.addButton(self.ui.rb_tx)

        self.ui.erx.clicked.connect(self.rx_emit)
        self.ui.etx.clicked.connect(self.tx_emit)

        self.ui.device.addItems(['[JIE] Seria JCMC', '[HNC] HV10', '[HNC] HV100', '[Drivetek] DT900-4T1.5G-C'])
        self.ui.device.currentTextChanged.connect(self.device_change)

        self.start_registers_map = {
            '[JIE] Seria JCMC': 8192,
            '[HNC] HV10': 8193,
            '[HNC] HV100': 8194,
            '[Drivetek] DT900-4T1.5G-C': 8192
        }

        self.forward_register = None
        self.reverse_register = None

        self.ui.forward_button.clicked.connect(self.forward_movement)
        self.ui.reverse_button.clicked.connect(self.reverse_movement)

        self.ui.connection_test.clicked.connect(self.test_connection)

    def test_connection(self):
        Thread(target=self.test_connection_thread).start()

    def test_connection_thread(self):
        self.tx_emit()
        wait(0.1)
        self.rx_emit()

    def device_change(self):
        new_device = self.ui.device.currentText()
        self.forward_register = self.start_registers_map.get(new_device, -1)
        self.reverse_register = self.forward_register + 1

    def forward_movement(self):
        if self.ui.rb_conn.isChecked():
            print(f'01 06 {self.forward_register} 01 CRC')
        else:
            print('Not connected')

    def reverse_movement(self):
        if self.ui.rb_conn.isChecked():
            print(f'01 06 {self.reverse_register} 01 CRC')
        else:
            print('Not connected')

    def rx_emit(self):
        Thread(target=self.rx).start()

    def tx_emit(self):
        Thread(target=self.tx).start()

    def rx(self):
        self.ui.rb_rx.setCheckable(True)
        self.ui.rb_rx.setChecked(True)
        self.update()
        wait(0.05)
        self.ui.rb_rx.setCheckable(False)
        application.ui.rb_rx.setChecked(False)
        self.update()

    def tx(self):
        self.ui.rb_tx.setCheckable(True)
        self.ui.rb_tx.setChecked(True)
        self.update()
        wait(0.1)
        self.ui.rb_tx.setCheckable(False)
        self.ui.rb_tx.setChecked(False)
        self.update()


app = QtWidgets.QApplication([])
application = mywindow()

application.ui.rb_rx.setChecked(False)
application.show()

sys.exit(app.exec())