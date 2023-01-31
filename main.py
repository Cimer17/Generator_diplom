from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from fpdf import FPDF
import datetime
from qt_material import apply_stylesheet


class Ui_mainWindow(QtWidgets.QMainWindow):
    
    def setupUi(self, mainWindow):
        
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(300, 400)
        mainWindow.setMinimumSize(QtCore.QSize(300, 250))
        mainWindow.setMaximumSize(QtCore.QSize(300, 250))
        self.setFixedSize(self.size())
        
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 40, 201, 41))
        self.comboBox.setObjectName("comboBox")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(75, 150, 151, 61))
        
        self.checkpdf = QtWidgets.QCheckBox(mainWindow)
        self.checkpdf.setGeometry(QtCore.QRect(40, 100, 300, 41))
        
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        self.text_status = QtWidgets.QLabel(self.centralwidget)
        self.text_status.setGeometry(QtCore.QRect(110, 220, 171, 20))
        self.text_status.setObjectName("text_status")
        
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Генератор дипломов"))
        self.pushButton.setText(_translate("mainWindow", "Создать"))
        self.text_status.setText(_translate("mainWindow", "Жду задания!"))
        self.checkpdf.setText(_translate("mainWindow", "Создать pdf файл с дипломами"))
        list1 = [
            self.tr('VR'),
            self.tr('MR'),
            self.tr('PP'),
            self.tr('PR'),
            self.tr('KG'),
            self.tr('SA'),
        ]
        self.comboBox.addItems(list1)
        self.pushButton.clicked.connect(self.create_img)
        self.comboBox.activated.connect(self.clear_text)
        self.status_pdf = False
        self.checkpdf.stateChanged.connect(self.checked_pdf)

    def checked_pdf(self):
        self.status_pdf = self.checkpdf.isChecked()

    def clear_text(self):
        self.text_status.setText("Жду задания...")

    def create_img(self):
        
        imagelist = []
        pdf = FPDF(orientation = 'L', unit = 'mm', format='A4')
        napravlenie = self.comboBox.currentText()
        df = pd.read_csv(f"data/{napravlenie}_DB.csv")
        
        font_FIO = ImageFont.truetype("arial.ttf", 70, encoding='utf-8')
        font_year = ImageFont.truetype("arial.ttf", 45, encoding='utf-8')
        
        pathc = os.path.abspath('pictures')
        url_patch = f'{pathc}\{napravlenie}'.replace('\\', '/')
        
        now_year = f'{datetime.datetime.now().year} год'
        
        if os.path.exists(url_patch):
            pass 
        else:
            os.mkdir(url_patch)
        
        for index, j in df.iterrows():
            
            img = Image.open(f'tmp/{napravlenie}.png')
            draw = ImageDraw.Draw(img)
            
            name_img = (j['name'])
            name_size = len(name_img)
            
            if name_size > 25:
                draw.text(xy=(500, 610), text=f'{name_img}', fill=(0, 0, 0), font=font_FIO)
            elif name_size > 16:
                draw.text(xy=(649 - name_size * 4 , 610), text=f'{name_img}', fill=(0, 0, 0), font=font_FIO)
            else:
                draw.text(xy=(649, 610), text=f'{name_img}', fill=(0, 0, 0), font=font_FIO)

            draw.text(xy=(890, 1300), text=f'{now_year}', fill=(0, 0, 0), font=font_year)
            
            patch_name = f'pictures/{napravlenie}/{name_img}.png'.replace(' ', '_')
            img.save(patch_name) 
            imagelist.append(patch_name)
        
        if self.status_pdf == True:
            for image in imagelist:
                pdf.add_page()
                pdf.image(image, 0, 0, 297, 210)
            pdf.output(f"pdf/{napravlenie}.pdf", "F")
        self.text_status.setText("Готово!")


if __name__ == "__main__":
    import sys
    check = os.path.exists('pictures')
    if check == False:
        os.mkdir("pictures")
    check = os.path.exists('pdf')
    if check == False:
        os.mkdir("pdf")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    apply_stylesheet(app, theme='dark_blue.xml')
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())