'''
Description:
Version: 2.0
Autor: zxm
Date: 2021-11-16 00:57:57
LastEditors: zxm
LastEditTime: 2021-11-17 01:22:01
'''
import time
import math
from PyQt5.QtCore import QThread, QObject, QTimer, pyqtSignal, pyqtSlot
from serial import Serial
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import matchOnYolo3 as matchOnYolo2
class MainWindow(QWidget):
    def __init__(self):
        self.camera=0
        super(MainWindow,self).__init__()
        self.setWindowTitle("Serial Communication")
        self.setGeometry(330, 330, 1980, 1100)
        # self.frame=1

        self.pause=0

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
        self.close_button.setGeometry(560, 5, 200, 40)
        self.close_button.clicked.connect(self.close_serial_port)
        self.close_button.setEnabled(False)

        self.start_button = QPushButton("开始",self)
        self.start_button.setGeometry(780, 5, 200, 40)
        self.start_button.clicked.connect(self.createThread)
        self.start_button.setEnabled(False)

        self.back_button = QPushButton("复位", self)
        self.back_button.setGeometry(560, 60, 200, 40)
        self.back_button.clicked.connect(self.goback)
        self.back_button.setEnabled(False)

        self.video_capture=cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        self.video_label = QLabel("视频",self)
        self.video_label.setGeometry(100, 300,960, 540)
        # self.video_thread = VideoThread(self)
        # self.video_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # self.video_capture = cv2.VideoCapture(0)

        self.pcb_label=QLabel('pcb检测结果',self)
        self.elec_label = QLabel('elec检测结果', self)
        self.pcb_label.setGeometry(1100, 10,960, 540)
        self.elec_label.setGeometry(1100, 500, 960, 540)

        self.stop_button = QPushButton("停止", self)
        self.stop_button.setGeometry(780, 60, 200, 40)
        self.stop_button.clicked.connect(self.stop_thread)
        self.stop_button.setEnabled(False)

        self.gopcb_button = QPushButton("到达贴装点位区", self)
        self.gopcb_button.setGeometry(780, 120, 200, 40)
        self.gopcb_button.clicked.connect(self.gopcb)
        self.gopcb_button.setEnabled(False)

        self.goelec_button = QPushButton("到达元件识别区", self)
        self.goelec_button.setGeometry(780, 180, 200, 40)
        self.goelec_button.clicked.connect(self.goelec)
        self.goelec_button.setEnabled(False)
        graphpcb = cv2.imread('jiancepcb.jpg')
        graphelec = cv2.imread('jianceele.jpg')
        self.update_pic(graphpcb, graphelec)


        self.angle=1

        matchOnYolo2.match2()

    #到贴装点位区域
    def gopcb(self):
        self.serial_port.write("1,04500,06000,0000".encode())
        time.sleep(0.5)
        self.serial_port.read()

    #到电子元件区域
    def goelec(self):
        self.serial_port.write("1,09000,06000,0000".encode())
        time.sleep(0.5)
        self.serial_port.read()

    #创建新线程
    def createThread(self):
        self.detect_thread = DetectThread(self)
        self.detect_thread.start()
        self.open_button.setEnabled(False)
        self.close_button.setEnabled(False)
        self.start_button.setEnabled(False)
        self.back_button.setEnabled(False)
        self.go_button.setEnabled(False)
        self.gopcb_button.setEnabled(False)
        self.goelec_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    #停止线程
    def stop_thread(self):
        self.detect_thread.terminate()
        self.start_button.setEnabled(True)
        self.close_button.setEnabled(True)
        self.back_button.setEnabled(True)
        self.go_button.setEnabled(True)
        self.gopcb_button.setEnabled(True)
        self.goelec_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()

    #复位
    def goback(self):
        self.serial_port.write("0,00000,00000,0000".encode())
        time.sleep(0.5)
        self.serial_port.read()
        # print("sadsdasdasda")

    #到达指定位置
    def goposition(self):
        posi=self.position.text()
        self.serial_port.write(posi.encode())
        self.serial_port.read()

    #实时更新摄像头捕捉的画面
    def update_frame(self):
        # ret, self.frame = self.video_capture.read()
        self.frame = cv2.imread('needdetect/pcb1.jpg')
        ret = True
        if ret:
            self.frame2 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # 转换颜色通道顺序
            self.frame2 = matchOnYolo2.getRotImg(self.frame2,self.angle)  #旋转指定角度
            # self.frame2 = cv2.rotate(self.frame2, cv2.ROTATE_90_CLOCKWISE)
            image = QImage(self.frame2, self.frame2.shape[1], self.frame2.shape[0], QImage.Format_RGB888)
            # self.frame2 = cv2.imread('needdetect/pcb1.jpg')
            row,col=self.frame2.shape[:2]

            #在视频显示区域画线
            cv2.line(self.frame2, (int(col/2), 0), (int(col/2), int(row)), (255, 0, 0), 1)
            cv2.line(self.frame2, (0, int(row/2)), (int(col), int(row/2)), (255, 0, 0), 1)
            pixmap = QPixmap.fromImage(image)
            self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio))  #显示画面

    #将检测完的结果图片显示
    def update_pic(self,graphpcb,graphelec):
        graphpcb = cv2.cvtColor(graphpcb, cv2.COLOR_BGR2RGB)  # 转换颜色通道顺序
        # graphpcb = cv2.rotate(graphpcb, cv2.ROTATE_90_CLOCKWISE)
        graphpcb = QImage(graphpcb, graphpcb.shape[1], graphpcb.shape[0], QImage.Format_RGB888)
        pixmappcb = QPixmap.fromImage(graphpcb)
        graphelec = cv2.cvtColor(graphelec, cv2.COLOR_BGR2RGB)  # 转换颜色通道顺序
        # graphelec = cv2.rotate(graphelec, cv2.ROTATE_90_CLOCKWISE)
        graphelec = QImage(graphelec, graphelec.shape[1], graphelec.shape[0], QImage.Format_RGB888)
        pixmapelec = QPixmap.fromImage(graphelec)
        self.pcb_label.setPixmap(pixmappcb.scaled(self.pcb_label.size(), Qt.KeepAspectRatio))
        self.elec_label.setPixmap(pixmapelec.scaled(self.elec_label.size(), Qt.KeepAspectRatio))

    def open_serial_port(self):
        port_name = self.port_textbox.text()
        try:
            self.serial_port = Serial(port_name, baudrate=115200, timeout=5)
            self.open_button.setEnabled(False)
            self.port_textbox.setEnabled(False)
            self.close_button.setEnabled(True)
            self.start_button.setEnabled(True)
            self.back_button.setEnabled(True)
            self.gopcb_button.setEnabled(True)
            self.goelec_button.setEnabled(True)
            self.go_button.setEnabled(True)
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
            self.port_textbox.setEnabled(True)
            self.close_button.setEnabled(False)
            self.start_button.setEnabled(False)
            self.back_button.setEnabled(False)
            self.gopcb_button.setEnabled(False)
            self.goelec_button.setEnabled(False)
            self.go_button.setEnabled(False)

    def zuobiaochangge(self,lst,x,y,frame):
        zuobiao=[]
        zuobiaos=[]
        row, col = frame.shape[:2]
        x=int(x)
        y=int(y)
        for j in lst:
            for i in j:
                ycent=(i[0]+i[2])/2
                xcent=(i[1]+i[3])/2
                x1=(xcent-row/2)
                y1=(ycent-col/2)
                xb=x+int(x1*1000/302)
                xb=xb-2100

                yb=y+int(y1*1000/302)
                yb = yb - 125
                xb=str(xb).zfill(5)
                yb=str(yb).zfill(5)
                zuobiao.append('1,'+xb+','+yb+","+str(int((360-i[4])*3200/360)).zfill(4))
            zuobiaos.append(zuobiao)
            zuobiao=[]
        return zuobiaos


    def zuobiaochangge2(self,lst,x,y,frame):
        zuobiao=[]
        zuobiaos=[]
        row, col = frame.shape[:2]
        x=int(x)
        y=int(y)

        for j in lst:
            for i in j:
                ycent = (i[0] + i[2]) / 2
                xcent = (i[1] + i[3]) / 2
                x1 = (xcent - row / 2)
                y1 = (ycent - col / 2)
                radian=math.atan2(2620, 80)/180*math.pi

                xb = x + int(x1 * 1000/302)
                xb=xb-2100

                yb = y + int(y1 * 1000/302)
                yb = yb - 125
                xb = str(xb).zfill(5)
                yb = str(yb).zfill(5)
                zuobiao.append('1,' + xb + ',' + yb + "," + str(int((360 - i[4]) * 3200 / 360)).zfill(4))
            zuobiaos.append(zuobiao)
            zuobiao=[]
        return zuobiaos

    def start_detection(self):
        if self.serial_port:
            try:
                x="1,04500,06000,0000"
                self.serial_port.write(x.encode('UTF-8'))
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
            arrive='5'
            time.sleep(0.5)
            arrive=self.serial_port.read().decode()
            print('arrive:',arrive)
            x=4500  #X轴步数
            y=6000  #Y轴步数

            if arrive=='1':  #到达指定位置
                time.sleep(0.2)
                framepcb=self.frame
                framepcb = matchOnYolo2.getRotImg(framepcb, self.angle)
                cv2.imwrite('needdetect/pcb1.jpg',framepcb)

                self.serial_port.write("1,09000,06000,0000".encode('UTF-8'))
                self.serial_port.read()

                time.sleep(0.2)
                frameelec =self.frame
                frameelec = matchOnYolo2.getRotImg(frameelec, self.angle)
                # frameelec = cv2.rotate(frameelec, cv2.ROTATE_90_CLOCKWISE)
                cv2.imwrite('needdetect/elec1.jpg',frameelec)

                elecsumlst,pcbsumlst,graphpcb,graphelec=matchOnYolo2.match()
                self.update_pic(graphpcb, graphelec)
                pcbzuobiao = []
                eleczuobiao=[]
                pcbzuobiao=self.zuobiaochangge2(pcbsumlst, x, y, framepcb)

                x=9000
                y=6000
                eleczuobiao=self.zuobiaochangge(elecsumlst, x, y, frameelec)
                # self.zuobiaochangge(sumlstdz, x, y, dzzuobiao, frameelec)
                print("pcb",len(pcbzuobiao),"  elec",len(eleczuobiao))
                l=0
                count=0
                for (elec,pcb) in zip(eleczuobiao,pcbzuobiao):
                    for (i,j) in zip(elec,pcb):
                        temp=i[-4:]
                        i=i[:-4]+"0000"

                        self.serial_port.write(i.encode()) #到电子原件处吸住
                        time.sleep(0.25)
                        x=self.serial_port.read().decode()  #读取运动做完之后返回的指定
                        if count==0:
                            self.serial_port.write("3,00000,00000,0000".encode())   #控制吸嘴往下移动
                        elif count==1:
                            self.serial_port.write("5,00000,00000,0000".encode())
                        time.sleep(0.25)
                        x=self.serial_port.read().decode()
                        j=j[:-4]+temp
                        self.serial_port.write(j.encode())  #到电路板上放下
                        time.sleep(0.25)
                        x=self.serial_port.read().decode()
                        if count==0:
                            self.serial_port.write("4,00000,00000,0000".encode())
                        elif count==1:
                            self.serial_port.write("6,00000,00000,0000".encode())
                        time.sleep(0.25)
                        x=self.serial_port.read().decode()
                        i='8'+i[1:]
                        i=i[:-4]+temp
                        self.serial_port.write(i.encode())
                        time.sleep(0.25)
                        x=self.serial_port.read().decode()
                    count+=1


        else:
            QMessageBox.warning(self, "Error", "Serial port is not open.")

    def recive(self):
        pass


class DetectThread(QThread):
    change_pixmap_signal = pyqtSignal(bytes)

    def __init__(self, window):
        super(DetectThread, self).__init__()

    def pauseandconti(self):
        while(window.pause==1):
            pass

    def run(self):
        window.start_detection()
        # i=0
        # while(True):
        #     # pass
        #     print(i)
        #     i+=1
        # while True:
        #     window.ret, window.frame2 = window.video_capture.read()
        #
        #     if window.ret:
        #
        #         window.frame1 = cv2.cvtColor(window.frame2, cv2.COLOR_BGR2RGB)  # 转换颜色通道顺序
        #         window.frame = cv2.rotate(window.frame1, cv2.ROTATE_90_CLOCKWISE)
        #         image = QImage(window.frame, window.frame.shape[1], window.frame.shape[0], QImage.Format_RGB888)
        #         row, col = window.frame.shape[:2]
        #         cv2.line(window.frame, (int(col / 2), 0), (int(col / 2), int(row)), (255, 0, 0), 1)
        #         cv2.line(window.frame, (0, int(row / 2)), (int(col), int(row / 2)), (255, 0, 0), 1)
        #         pixmap = QPixmap.fromImage(image)
        #         time.sleep(0.02)
        #         window.video_label.setPixmap(pixmap.scaled(window.video_label.size(), Qt.KeepAspectRatio))
        #         print(1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())






