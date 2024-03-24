'''
Description:
Version: 2.0
Autor: zxm
Date: 2021-11-16 00:57:57
LastEditors: zxm
LastEditTime: 2021-11-17 01:22:01
'''
import time

"""
导入界面相关的模块和包
"""

from PyQt5.QtCore import QThread, QObject, QTimer, pyqtSignal, pyqtSlot
from serial import Serial
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import matchOnYolo
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Serial Communication")
        self.setGeometry(330, 330, 1000, 1000)
        # self.frame=1
        self.serial_port = None
        self.port_label = QLabel("串口端口:",self)
        self.port_label.setGeometry(0, 5, 120, 40)
        self.command_label = QLabel("指令端口:", self)
        self.command_label.setGeometry(0,60, 120, 40)
        self.port_textbox = QLineEdit(self)
        self.port_textbox.setGeometry(120,5,200,40)
        self.position = QLineEdit(self)
        self.position.setGeometry(120, 60, 200, 40)
        self.go_button = QPushButton("执行指令", self)
        self.go_button.setGeometry(340, 60, 200, 40)
        self.go_button.clicked.connect(self.goposition)
        self.go_button.setEnabled(False)

        self.open_button = QPushButton("打开串口",self)
        self.open_button.setGeometry(340, 5,200,40)
        self.open_button.clicked.connect(self.open_serial_port)

        self.close_button = QPushButton("关闭串口",self)
        self.close_button.setGeometry(780, 105, 200, 40)
        self.close_button.clicked.connect(self.close_serial_port)
        self.close_button.setEnabled(False)

        self.start_button = QPushButton("开始",self)
        self.start_button.setGeometry(560, 5, 200, 40)
        self.start_button.clicked.connect(self.start_detection)
        self.start_button.setEnabled(False)

        self.back_button = QPushButton("复位", self)
        self.back_button.setGeometry(560, 60, 200, 40)
        self.back_button.clicked.connect(self.goback)
        self.back_button.setEnabled(False)

        self.elec_button = QPushButton("元件位置", self)
        self.elec_button.setGeometry(780, 5, 200, 40)
        self.elec_button.clicked.connect(self.goELEC)
        self.elec_button.setEnabled(False)

        self.pcb_button = QPushButton("PCB位置", self)
        self.pcb_button.setGeometry(780, 60, 200, 40)
        self.pcb_button.clicked.connect(self.goPCB)
        self.pcb_button.setEnabled(False)


        self.video_capture=cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.video_label = QLabel("视频",self)
        self.video_label.setGeometry(200, 130,640, 780)
        self.video_thread = VideoThread(self)
        self.video_thread.start()

    def goback(self):
        self.serial_port.write("0,00000,00000,0000".encode())
        self.serial_port.read()

    def goPCB(self):
        self.serial_port.write("1,04500,06000,0000".encode())
        self.serial_port.read()

    def goELEC(self):
        self.serial_port.write("1,09000,06000,0000".encode())
        self.serial_port.read()

    def goposition(self):
        posi=self.position.text()
        self.serial_port.write(posi.encode())
        self.serial_port.read()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色通道顺序
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            row,col=frame.shape[:2]
            cv2.line(frame, (int(col/2), 0), (int(col/2), int(row)), (255, 0, 0), 1)
            cv2.line(frame, (0, int(row/2)), (int(col), int(row/2)), (255, 0, 0), 1)
            pixmap = QPixmap.fromImage(image)
            self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio))

    def open_serial_port(self):

        port_name = self.port_textbox.text()
        try:
            self.serial_port = Serial(port_name, baudrate=115200, timeout=5)
            self.open_button.setEnabled(False)
            self.close_button.setEnabled(True)
            self.start_button.setEnabled(True)
            self.back_button.setEnabled(True)
            self.go_button.setEnabled(True)
            self.pcb_button.setEnabled(True)
            self.elec_button.setEnabled(True)
            if (self.serial_port.isOpen()):
                print("打开成功")
            else:
                print("打开失败")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def close_serial_port(self):
        if self.serial_port:
            self.serial_port.close()
            self.serial_port = None
            self.open_button.setEnabled(True)
            self.close_button.setEnabled(False)
            self.start_button.setEnabled(False)
            self.pcb_button.setEnabled(True)
            self.elec_button.setEnabled(True)

    def zuobiaochangge(self,lst,x,y,pcbzuobiao,frame):
        row, col = frame.shape[:2]
        x=int(x)
        y=int(y)

        for i in lst:
            ycent = (i[0] + i[2]) / 2
            xcent = (i[1] + i[3]) / 2
            x1 = xcent - row / 2
            y1 = ycent - col / 2
            xb = x + int(x1 * (8.403) / 2)
            xb = xb - int(4390 / 2)

            yb = y + int(y1 * (8.403) / 2)
            yb = yb - 245
            xb = str(xb).zfill(5)
            yb = str(yb).zfill(5)
            pcbzuobiao.append('1,' + xb + ',' + yb + "," + str(int((360 - i[4]) * 3200 / 360)).zfill(4))

    def zuobiaochangge2(self,lst,x,y,pcbzuobiao,frame):
        row, col = frame.shape[:2]
        x=int(x)
        y=int(y)

        for i in lst:
            ycent=(i[0]+i[2])/2
            xcent=(i[1]+i[3])/2
            x1=xcent-row/2
            y1=ycent-col/2
            xb=x+int(x1*4.1)

            yb=y+int(y1*4.1)
            xb=str(xb).zfill(4)
            yb=str(yb).zfill(4)
            pcbzuobiao.append('1,'+xb+','+yb+","+str(int((360-i[4])*3200/360)).zfill(4))


    def start_detection(self):
        if self.serial_port:
            try:
                x="1,04500,06000,0000"
                self.serial_port.write(x.encode('UTF-8'))
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
            arrive='0'
            arrive=self.serial_port.read().decode()
            # time.sleep(0.5)
            x=4500  #X轴步数
            y=6000  #Y轴步数


            if arrive=='1':  #到达指定位置
                time.sleep(0.5)
                framepcb=self.frame2
                framepcb = cv2.rotate(framepcb, cv2.ROTATE_90_CLOCKWISE)
                cv2.imwrite('needdetect/pcb1.jpg')

                self.serial_port.write("1,09000,06000,0000".encode('UTF-8'))
                self.serial_port.read()

                time.sleep(0.5)
                frameelec = self.frame2
                frameelec = cv2.rotate(frameelec, cv2.ROTATE_90_CLOCKWISE)
                cv2.imwrite('needdetect/elec1.jpg')

                elecsumlst,pcbsumlst=matchOnYolo.match()
                pcbzuobiao = []
                eleczuobiao=[]
                self.zuobiaochangge(pcbsumlst, x, y, pcbzuobiao, framepcb)
                self.zuobiaochangge(elecsumlst, x, y, eleczuobiao, frameelec)
                x=9000
                y=6000
                # self.zuobiaochangge(sumlstdz, x, y, dzzuobiao, frameelec)
                print("pcb",len(pcbzuobiao),"  dz",len(eleczuobiao))
                l=0
                for (i,j) in zip(eleczuobiao,pcbzuobiao):
                    temp=i[-4:]
                    i=i[:-4]+"0000"
                    self.serial_port.write(i.encode()) #到电子原件处吸住
                    self.serial_port.read()  #读取运动做完之后返回的指定
                    self.serial_port.write("3,00000,00000,0000".encode())   #控制吸嘴往下移动
                    self.serial_port.read()
                    j=j[:-4]+temp
                    self.serial_port.write(j.encode())  #到电路板上放下
                    self.serial_port.read()
                    self.serial_port.write("4,00000,00000,0000".encode())
                    self.serial_port.read()
                    i='8'+i[1:]
                    i=i[:-4]+temp
                    self.serial_port.write(i.encode())
                    self.serial_port.read()

        else:
            QMessageBox.warning(self, "Error", "Serial port is not open.")

    def recive(self):
        pass


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(bytes)

    def __init__(self, window):
        super(VideoThread, self).__init__()

    def run(self):

        while True:
            window.ret, window.frame2 = window.video_capture.read()

            if window.ret:

                window.frame1 = cv2.cvtColor(window.frame2, cv2.COLOR_BGR2RGB)  # 转换颜色通道顺序
                window.frame = cv2.rotate(window.frame1, cv2.ROTATE_90_CLOCKWISE)
                image = QImage(window.frame, window.frame.shape[1], window.frame.shape[0], QImage.Format_RGB888)
                row, col = window.frame.shape[:2]
                cv2.line(window.frame, (int(col / 2), 0), (int(col / 2), int(row)), (255, 0, 0), 1)
                cv2.line(window.frame, (0, int(row / 2)), (int(col), int(row / 2)), (255, 0, 0), 1)
                pixmap = QPixmap.fromImage(image)
                time.sleep(0.02)
                window.video_label.setPixmap(pixmap.scaled(window.video_label.size(), Qt.KeepAspectRatio))
                print(1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())






